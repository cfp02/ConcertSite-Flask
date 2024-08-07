from flask import Blueprint, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
from flask import g, render_template
from concert_mailer.db import insert_concert, get_db, get_websites, get_scrape_queries, get_scrape_queries_by_website, insert_scrape_query, delete_scrape_query
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

def scrape_concert_info(soup: BeautifulSoup, website):
    container_tag_name = tuple(website['container_tag_tuple'].split(','))
    tour_name_tag = tuple(website['tour_name_tag_tuple'].split(','))
    tour_venue_tag = tuple(website['tour_venue_tag_tuple'].split(','))
    tour_date_tag = tuple(website['tour_date_tag_tuple'].split(','))

    # print("Tag names: ", container_tag_name, tour_name_tag, tour_venue_tag, tour_date_tag)

    # # Debug: Print HTML length and some content
    # print(f"HTML length: {len(soup)}")
    # print(soup.prettify()[:500])  # Print first 500 characters of the HTML for inspection


    if len(container_tag_name) == 2:
        concerts = soup.find_all(*container_tag_name, recursive=True)
    else:
        concerts = soup.find_all(container_tag_name[0], recursive=True)


    # print(f"Number of concert containers found: {len(concerts)}")
    # time.sleep(2)

    concert_list = []

    for concert in concerts:
        # print("Processing concert")
        # print(concert)
        this_concert = {}
        band_name = concert.find(tour_name_tag[0], tour_name_tag[1]).text
        this_concert['artist'] = band_name

        concert_venue = concert.find(tour_venue_tag[0], tour_venue_tag[1]).text
        this_concert['venue'] = concert_venue

        concert_date = concert.find(tour_date_tag[0], tour_date_tag[1]).get('value')


        if website['name'] == 'ticketliquidator':
            # print("Processing ticketliquidator concert")
            # print("Concert Date: ", concert_date)
            # print("Concert Venue: ", concert_venue)
            # print("Band Name: ", band_name)
            num = concert_date.split(' ')[1].strip()
            if num[0] == '0':
                num = num[1]
                concert_date = concert_date.split(' ')[0].strip() + ' ' + num + ', ' + concert_date.split(' ')[2].strip()
            concert_date_datetime = datetime.datetime.strptime(concert_date, '%B %d, %Y')
            concert_date = concert_date_datetime.strftime('%Y-%m-%d')

            this_concert['date'] = concert_date
            this_concert['mgmt_email'] = ''  # Add logic to get email if available
            this_concert['mgmt_name'] = ''  # Add logic to get name if available

        else:

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

    websites = get_websites()

    for website in websites:
        queries = get_scrape_queries_by_website(website['id'])
        for query in queries:
            if website['name'] == 'ticketliquidator':
                # Construct the query string dynamically
                query_string = f"{query['city']}+concerts+{query['month']}&allLoadMore=20"
                url = website['base_url'] + query_string
            else:
                url = website['base_url']

            soup = get_page_source(url)
            concerts = scrape_concert_info(soup, website)
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
            user_id=g.user['id']
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


@bp.route('/add_scrape_query', methods=['POST'])
def add_scrape_query():
    data = request.json
    website_id = data['website_id']
    # query = data['query']
    city = data['city']
    month = data['month']

    insert_scrape_query(website_id, city, month)
    return jsonify({'message': 'Scrape query added successfully!'})

@bp.route('/delete_scrape_query/<int:query_id>', methods=['POST'])
def delete_scrape_query_route(query_id):
    delete_scrape_query(query_id)
    return jsonify({'message': 'Scrape query deleted successfully!'})

@bp.route('/scraping')
def scraping():
    websites = get_websites()
    scrape_queries = get_scrape_queries()
    return render_template('scraping/index.html', websites=websites, scrape_queries=scrape_queries)