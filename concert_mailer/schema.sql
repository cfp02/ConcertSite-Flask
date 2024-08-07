DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS concert;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE concert (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT NOT NULL,
    venue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    mgmt_email TEXT,
    mgmt_name TEXT,
    emailed BOOLEAN DEFAULT FALSE,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (venue_id) REFERENCES venue(id)
);

CREATE TABLE venue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT,
    address TEXT,
    rating INTEGER,
    minimal_substring TEXT,
    venue_email_text TEXT
);

CREATE TABLE venue_alias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alias TEXT NOT NULL,
    venue_id INTEGER NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venue (id) ON DELETE CASCADE
);

CREATE TABLE website (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    base_url TEXT NOT NULL,
    container_tag_tuple TEXT NOT NULL,
    tour_name_tag_tuple TEXT NOT NULL,
    tour_venue_tag_tuple TEXT NOT NULL,
    tour_date_tag_tuple TEXT NOT NULL,
    tour_openers_tag_tuple TEXT
);

CREATE TABLE scrape_query (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website_id INTEGER NOT NULL,
    query TEXT NOT NULL,
    city TEXT NOT NULL,
    month TEXT NOT NULL,
    FOREIGN KEY (website_id) REFERENCES website (id)
);

INSERT INTO website (name, base_url, container_tag_tuple, tour_name_tag_tuple, tour_venue_tag_tuple, tour_date_tag_tuple, tour_openers_tag_tuple) 
VALUES 
('crossroadspresents.com', 'https://crossroadspresents.com/pages/events', 'div,edit-tour-container', 'div,edit-tour-name', 'div,edit-tour-venue', 'div,edit-tour-date', 'div,edit-tour-namesubs'),
('ticketliquidator', 'https://www.ticketliquidator.com/search?q=', 'div,geo-event', 'span,event-name', 'span,venue-name', 'input,event-date', 'span,event-city');