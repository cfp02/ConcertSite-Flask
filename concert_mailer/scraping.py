from flask import Blueprint, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
from flask import g
from concert_mailer.db import insert_concert
from concert_mailer.scraping_helpers import website_html_keys, ticketliqidator_queries_boston, ticketliqidator_queries_worcester

bp = Blueprint('scraping', __name__)

def get_page_source(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # Adjust the sleep time as necessary

    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

def scrape_concert_info_ticketliquidator(soup: BeautifulSoup):
    concerts = soup.find_all('div', class_='geo-event', recursive=True)
    concert_list = []

    for concert in concerts:
        this_concert = {}
        band_name = concert.find(website_html_keys['ticketliquidator']['tour-name'][0], class_=website_html_keys['ticketliquidator']['tour-name'][1]).text
        this_concert['artist'] = band_name

        concert_venue = concert.find(website_html_keys['ticketliquidator']['tour-venue'][0], class_=website_html_keys['ticketliquidator']['tour-venue'][1]).text
        this_concert['venue'] = concert_venue

        concert_date = concert.find('input', class_=website_html_keys['ticketliquidator']['tour-date'][1]).get('value')
        num = concert_date.split(' ')[1].strip()
        if num[0] == '0':
            num = num[1]
            concert_date = concert_date.split(' ')[0].strip() + ' ' + num + ', ' + concert_date.split(' ')[2].strip()
        concert_date_datetime = datetime.datetime.strptime(concert_date, '%B %d, %Y')
        concert_date = concert_date_datetime.strftime('%Y-%m-%d')

        this_concert['date'] = concert_date
        this_concert['mgmt_email'] = ''  # Add logic to get email if available
        this_concert['mgmt_name'] = ''  # Add logic to get name if available

        concert_list.append(this_concert)
    return concert_list

def scrape_concert_info_crossroadspresents(soup: BeautifulSoup):
    concerts = soup.find_all(website_html_keys['crossroadspresents.com']['container-tag-name'][0], class_=website_html_keys['crossroadspresents.com']['container-tag-name'][1], recursive=True)
    concert_list = []

    for concert in concerts:
        this_concert = {}
        band_name = concert.find(website_html_keys['crossroadspresents.com']['tour-name'][0], class_=website_html_keys['crossroadspresents.com']['tour-name'][1]).text
        this_concert['artist'] = band_name

        concert_venue = concert.find(website_html_keys['crossroadspresents.com']['tour-venue'][0], class_=website_html_keys['crossroadspresents.com']['tour-venue'][1]).text
        this_concert['venue'] = concert_venue

        concert_date = concert.find(website_html_keys['crossroadspresents.com']['tour-date'][0], class_=website_html_keys['crossroadspresents.com']['tour-date'][1]).text
        concert_date = concert_date.split('•')[0].strip()
        concert_date = concert_date.split(',')[1].strip() + ', ' + concert_date.split(',')[2].strip()
        concert_date_datetime = datetime.datetime.strptime(concert_date, '%B %d, %Y')
        concert_date = concert_date_datetime.strftime('%Y-%m-%d')

        this_concert['date'] = concert_date
        this_concert['mgmt_email'] = ''  # Add logic to get email if available
        this_concert['mgmt_name'] = ''  # Add logic to get name if available

        concert_list.append(this_concert)
    return concert_list

@bp.route('/scrape_concerts', methods=['POST'])
def scrape_concerts():
    all_concerts = []

    # Add logic to get URLs and scrape data
    urls = [
        ('ticketliquidator', ticketliqidator_queries_boston),
        # ('ticketliquidator', ticketliqidator_queries_worcester),
        # ('crossroadspresents.com', [website_html_keys['crossroadspresents.com']['url']])
    ]

    for source, query_list in urls:
        for query in query_list:
            url = website_html_keys[source]['url'] + query
            soup = get_page_source(url)

            if source == 'ticketliquidator':
                concerts = scrape_concert_info_ticketliquidator(soup)
            elif source == 'crossroadspresents.com':
                concerts = scrape_concert_info_crossroadspresents(soup)

            all_concerts.extend(concerts)

    # Remove duplicates
    unique_concerts = remove_duplicate_concerts(all_concerts)

    # Save concerts to the database
    for concert in unique_concerts:
        insert_concert(
            artist=concert['artist'],
            venue_name=concert['venue'],
            date=concert['date'],
            mgmt_email=concert['mgmt_email'],
            mgmt_name=concert['mgmt_name'],
            user_id=g.user['id']  # Assuming you have user authentication
        )

    return jsonify({'message': 'Concerts scraped and stored successfully!', 'concerts': unique_concerts})

def remove_duplicate_concerts(concerts):
    unique_concerts = []
    seen_concerts = set()
    for concert in concerts:
        concert_tuple = (concert['artist'], concert['venue'], concert['date'])
        if concert_tuple not in seen_concerts:
            unique_concerts.append(concert)
            seen_concerts.add(concert_tuple)
    return unique_concerts
