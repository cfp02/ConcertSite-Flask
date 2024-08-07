import sqlite3

def alter_database():
    conn = sqlite3.connect('instance/concert_mailer.sqlite')
    cursor = conn.cursor()

    # Put some commands here
    '''
    '''
    # cursor.execute("ALTER TABLE venue ADD COLUMN venue_email_text TEXT")

    # CREATE TABLE website (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT NOT NULL,
    #     base_url TEXT NOT NULL,
    #     container_tag_tuple TEXT NOT NULL,
    #     tour_name_tag_tuple TEXT NOT NULL,
    #     tour_venue_tag_tuple TEXT NOT NULL,
    #     tour_date_tag_tuple TEXT NOT NULL,
    #     tour_openers_tag_tuple TEXT
    # );

    # CREATE TABLE scrape_query (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     website_id INTEGER NOT NULL,
    #     query TEXT NOT NULL,
    #     city TEXT NOT NULL,
    #     month TEXT NOT NULL,
    #     FOREIGN KEY (website_id) REFERENCES website (id)
    # );

    # INSERT INTO website (name, base_url, container_tag_tuple, tour_name_tag_tuple, tour_venue_tag_tuple, tour_date_tag_tuple, tour_openers_tag_tuple) 
    # VALUES 
    # ('crossroadspresents.com', 'https://crossroadspresents.com/pages/events', 'div,edit-tour-container', 'div,edit-tour-name', 'div,edit-tour-venue', 'div,edit-tour-date', 'div,edit-tour-namesubs'),
    # ('ticketliquidator', 'https://www.ticketliquidator.com/search?q=', 'div,geo-event', 'span,event-name', 'span,venue-name', 'input,event-date', 'span,event-city');

    # Commands:
    cursor.execute("CREATE TABLE website (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, base_url TEXT NOT NULL, container_tag_tuple TEXT NOT NULL, tour_name_tag_tuple TEXT NOT NULL, tour_venue_tag_tuple TEXT NOT NULL, tour_date_tag_tuple TEXT NOT NULL, tour_openers_tag_tuple TEXT)")
    cursor.execute("CREATE TABLE scrape_query (id INTEGER PRIMARY KEY AUTOINCREMENT, website_id INTEGER NOT NULL, query TEXT NOT NULL, city TEXT NOT NULL, month TEXT NOT NULL, FOREIGN KEY (website_id) REFERENCES website (id))")
    cursor.execute("INSERT INTO website (name, base_url, container_tag_tuple, tour_name_tag_tuple, tour_venue_tag_tuple, tour_date_tag_tuple, tour_openers_tag_tuple) VALUES ('crossroadspresents.com', 'https://crossroadspresents.com/pages/events', 'div,edit-tour-container', 'div,edit-tour-name', 'div,edit-tour-venue', 'div,edit-tour-date', 'div,edit-tour-namesubs'), ('ticketliquidator', 'https://www.ticketliquidator.com/search?q=', 'div,geo-event', 'span,event-name', 'span,venue-name', 'input,event-date', 'span,event-city')")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    alter_database()
