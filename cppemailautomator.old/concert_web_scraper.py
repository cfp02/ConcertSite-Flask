from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import datetime
import os.path

from header import website_html_keys, boston_venues_list, worcester_venues_list, ticketliqidator_queries_boston, ticketliqidator_queries_worcester

def get_page_source(url):
    '''
    Gets the page source of the provided URL using Selenium and ChromeDriver
    '''
    # Set up the Selenium web driver
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Load the webpage
    driver.get(url)

    # Wait for the JavaScript to render
    time.sleep(5)  # Adjust the sleep time as necessary

    # Get the page source and close the browser
    page_source = driver.page_source
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

def scrape_concert_info_ticketliquidator(soup: BeautifulSoup):
        
    # Find all the concerts on the webpage
    concerts = soup.find_all('div', class_ = 'geo-event', recursive=True)

    # Initialize lists to store the scraped information
    concert_list = []

    # Loop through each concert and scrape the information

    for concert in concerts:
        this_concert = {}
        # Get the band name
        band_name = concert.find(website_html_keys['ticketliquidator']['tour-name'][0], class_=website_html_keys['ticketliquidator']['tour-name'][1]).text
        this_concert['Band Name - Unclean'] = band_name

        # Get the concert venue
        concert_venue = concert.find(website_html_keys['ticketliquidator']['tour-venue'][0], class_=website_html_keys['ticketliquidator']['tour-venue'][1]).text
        this_concert['Venue - Unclean'] = concert_venue

        # Get the concert date out of the first input tag
        concert_date = concert.find('input', class_=website_html_keys['ticketliquidator']['tour-date'][1]).get('value')
        # Currently in the format "February 01, 2024", reduce down to February 1, 2024
        num = concert_date.split(' ')[1].strip()
        if num[0] == '0':
            num = num[1]
            concert_date = concert_date.split(' ')[0].strip() + ' ' + num + ', ' + concert_date.split(' ')[2].strip()
        # Convert to a datetime object
        concert_date_datetime = datetime.datetime.strptime(concert_date, '%B %d, %Y')
        # Convert to string in the format 12/31/2024
        concert_date = concert_date_datetime.strftime('%m/%d/%Y')

        this_concert['Concert Date'] = concert_date

        # Get the concert openers
        this_concert['Openers'] = ''

        concert_list.append(this_concert)
        
    return concert_list

def scrape_concert_info_crossroadspresents(soup: BeautifulSoup):
    
    # Find all the concerts on the webpage
    concerts = soup.find_all(website_html_keys['crossroadspresents.com']['container-tag-name'][0], class_=website_html_keys['crossroadspresents.com']['container-tag-name'][1], recursive=True)

    # Initialize lists to store the scraped information
    concert_list = []

    # Loop through each concert and scrape the information

    for concert in concerts:
        this_concert = {}
        # Get the band name
        band_name = concert.find(website_html_keys['crossroadspresents.com']['tour-name'][0], class_=website_html_keys['crossroadspresents.com']['tour-name'][1]).text
        this_concert['Band Name - Unclean'] = band_name

        # Get the concert venue
        concert_venue = concert.find(website_html_keys['crossroadspresents.com']['tour-venue'][0], class_=website_html_keys['crossroadspresents.com']['tour-venue'][1]).text
        this_concert['Venue - Unclean'] = concert_venue

        # Get the concert date
        concert_date = concert.find(website_html_keys['crossroadspresents.com']['tour-date'][0], class_=website_html_keys['crossroadspresents.com']['tour-date'][1]).text
        # Currently in the format "Saturday, January 20, 2024 • 6:30 PM", reduce down to January 20, 2024
        concert_date = concert_date.split('•')[0].strip()
        # Still contains the day of the week, remove that
        concert_date = concert_date.split(',')[1].strip() + ', ' + concert_date.split(',')[2].strip()
        # Convert to a datetime object
        concert_date_datetime = datetime.datetime.strptime(concert_date, '%B %d, %Y')
        # Convert to string in the format 12/31/2024
        concert_date = concert_date_datetime.strftime('%m/%d/%Y')
        this_concert['Concert Date'] = concert_date

        # Get the concert openers
        concert_openers = concert.find(website_html_keys['crossroadspresents.com']['tour-openers'][0], class_=website_html_keys['crossroadspresents.com']['tour-openers'][1]).text
        this_concert['Openers'] = concert_openers

        concert_list.append(this_concert)
        
    return concert_list

def remove_duplicate_concerts(concerts: list[dict]) -> list[dict]:
    # Remove duplicate concerts
    unique_concerts = []
    print(str(len(concerts)) + ' with duplicates')
    for concert in concerts:
        if concert not in unique_concerts:
            unique_concerts.append(concert)
    print(str(len(unique_concerts)) + ' without duplicates')
    return unique_concerts

def write_scraped_to_csv(concerts: list[dict], filename):
    # Write the scraped information to a CSV file
    # if it already exists, append a number to the end
    i = 1
    filename = 'output_data/' + filename
    while os.path.isfile(filename):
        filename = filename[:-4] + '_' + str(i) + '.csv'
        i += 1

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(concerts[0].keys())
        for concert in concerts:
            writer.writerow(concert.values())

# Function that reads a csv and returns a list of unique concert venues
def get_unique_venues_from_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        venues = []
        for row in reader:
            if row[1] not in venues:
                venues.append(row[1])
    return venues

def replace_venue_name(venue_name: str) -> str:
    # Replace the venue name with the one in the dictionary
    for key in boston_venues_list.keys():
        if key in venue_name.lower():
            return boston_venues_list[key]
    for key in worcester_venues_list.keys():
        if key in venue_name.lower():
            return worcester_venues_list[key]
    return venue_name

def replace_all_venue_names(concerts: list[dict]) -> list[dict]:
    # Replace all the venue names with the ones in the dictionary
    for concert in concerts:
        concert['Venue - Unclean'] = replace_venue_name(concert['Venue - Unclean'])
    return concerts

def construct_all_csvs(website_html_keys, filename):

    ### Get all lists of URLs
    all_urls : list[dict,list]= []

    # ticketliquidator Boston concerts
    tl_bos_urls = (website_html_keys['ticketliquidator'], [])
    for url in ticketliqidator_queries_boston:
        tl_bos_urls[1].append(website_html_keys['ticketliquidator']['url'] + url)

    # ticketliquidator Worcester concerts
    tl_worc_urls = (website_html_keys['ticketliquidator'], [])
    for url in ticketliqidator_queries_worcester:
        tl_worc_urls[1].append(website_html_keys['ticketliquidator']['url'] + url)

    # crossroads Boston concerts
    cr_bos_urls = (website_html_keys['crossroadspresents.com'] ,[website_html_keys['crossroadspresents.com']['url']])

    # Get all urls
    all_urls.extend([tl_bos_urls, tl_worc_urls, cr_bos_urls])

    # Print each URL
    for url_tuple in all_urls:
        print(url_tuple[1])


    ### Scrape all webpages
    all_concerts = []
    # Loop through the websites
    for url_tuple in all_urls:
        if url_tuple[0]['which-website'] == 'ticketliquidator':
            # Loop through the ticketliquidator urls
            for url in url_tuple[1]:
                all_concerts.extend(scrape_concert_info_ticketliquidator(get_page_source(url)))
                print("\n\nScraped ", url + '\n  ' + str(len(all_concerts)) + ' concerts so far')
        elif url_tuple[0]['which-website'] == 'crossroadspresents.com':
            # Loop through the crossroads urls (just one)
            for url in url_tuple[1]:
                all_concerts.extend(remove_duplicate_concerts(scrape_concert_info_crossroadspresents(get_page_source(url))))
                print("\n\nScraped ", url)
        
    
    ### Replace all venue names with the ones in the dictionary
    all_concerts_clean = replace_all_venue_names(all_concerts)

    ### Write all concerts to a CSV file
    write_scraped_to_csv(all_concerts_clean, filename)


def main():

    # # Get the page source of the website
    # crossroads_source = get_page_source(website_html_keys['crossroadspresents.com']['url'])
    # # Save the data to an HTML file
    # with open("soup_crossroads.html", "w") as file:
    #     file.write(str(crossroads_source))
    
    # crossroads_concerts = remove_duplicate_concerts(scrape_concert_info_crossroadspresents(get_page_source(website_html_keys['crossroadspresents.com']['url'])))
    # ticketliquidator_concerts = remove_duplicate_concerts(scrape_concert_info_ticketliquidator(get_page_source(website_html_keys['ticketliquidator-march']['url'])))

    with open("soup_crossroads.html", "r") as file:
        crossroads_soup = BeautifulSoup(file.read(), 'html.parser')

    with open("soup_ticketliquidator.html", "r") as file:
        ticketliquidator_soup = BeautifulSoup(file.read(), 'html.parser')

    crossroads_concerts = remove_duplicate_concerts(scrape_concert_info_crossroadspresents(crossroads_soup))
    ticketliquidator_concerts = (scrape_concert_info_ticketliquidator(ticketliquidator_soup))
    crossroads_concerts_cleanvenue = replace_all_venue_names(crossroads_concerts)
    ticketliquidator_concerts_cleanvenue = replace_all_venue_names(ticketliquidator_concerts)
    # Write the scraped information to a CSV file
    write_scraped_to_csv(crossroads_concerts_cleanvenue, "concerts_crossroads.csv")
    write_scraped_to_csv(ticketliquidator_concerts_cleanvenue, "concerts_ticketliquidator.csv")

    print("Done!")

if __name__ == "__main__":
    construct_all_csvs(website_html_keys, 'concerts_all.csv')




