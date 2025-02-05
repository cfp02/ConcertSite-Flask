import sqlite3

import click
from flask import current_app, g
from datetime import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
def get_concerts(date_filter, order, limit, offset):
    db = get_db()
    return db.execute(
        'SELECT c.id, c.artist, c.venue_id, v.name AS venue, c.date, c.mgmt_email, c.mgmt_name, c.emailed, c.user_id, u.username '
        'FROM concert c '
        'JOIN user u ON c.user_id = u.id '
        'JOIN venue v ON c.venue_id = v.id '
        'WHERE c.date ' + date_filter + ' ? '
        'ORDER BY c.date ' + order + ' '
        'LIMIT ? OFFSET ?',
        (datetime.today().date(), limit, offset)
    ).fetchall()

def count_concerts(date_filter):
    db = get_db()
    return db.execute(
        f'SELECT COUNT(*) FROM concert WHERE date {date_filter} ?',
        (datetime.today().date(),)
    ).fetchone()[0]

def insert_concert(artist, venue_name, date, mgmt_email, mgmt_name, user_id):
    db = get_db()

    venue_id = None

    # See if the passed venue_name is an alias, fetch one venue that maches
    venue = db.execute(
        "SELECT venue_id FROM venue_alias WHERE alias = ?",
        (venue_name,)
    ).fetchone()

    if venue:
        venue_id = venue['venue_id']
    else:
        # Check if the venue substring exists in the venue name
        venue = db.execute(
            "SELECT id FROM venue WHERE ? LIKE '%' || minimal_substring || '%'",
            (venue_name,)
        ).fetchone()

        if venue:
            venue_id = venue['id']
        else:
            # Check if the venue_name is the title of the venue
            venue = db.execute(
                "SELECT id FROM venue WHERE name = ?",
                (venue_name,)
            ).fetchone()

            if venue:
                venue_id = venue['id']
            else:
                # Venue does not exist, insert it with a temporary name
                db.execute(
                    "INSERT INTO venue (name, minimal_substring) VALUES (?, ?)",
                    (venue_name, venue_name)
                )
                db.commit()
                # Fetch the new venue ID
                venue = db.execute(
                    "SELECT id FROM venue WHERE name = ?",
                    (venue_name,)
                ).fetchone()
                venue_id = venue['id']

            # Insert the alias for the newly created venue
            db.execute(
                "INSERT INTO venue_alias (alias, venue_id) VALUES (?, ?)",
                (venue_name, venue_id)
            )
            db.commit()

    if venue_id is None:
        raise ValueError("Failed to determine venue ID")
    
    # Check for duplicate concert
    duplicate_concert = db.execute(
        'SELECT id FROM concert WHERE artist = ? AND venue_id = ? AND date = ?',
        (artist, venue_id, date)
    ).fetchone()

    if duplicate_concert:
        print(f"Duplicate concert found: Artist: {artist}, Venue ID: {venue_id}, Date: {date}")
        return

    # Insert the concert with the venue_id
    db.execute(
        'INSERT INTO concert (artist, venue_id, date, mgmt_email, mgmt_name, emailed, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (artist, venue_id, date, mgmt_email, mgmt_name, False, user_id)
    )
    db.commit()



# def insert_concert(artist, date, mgmt_email, mgmt_name, user_id, venue_id=None, venue_name=None):
#     db = get_db()
    
#     if venue_id is None and venue_name is not None:
#         # Check if the venue already exists
#         venue = db.execute(
#             "SELECT id FROM venue WHERE name = ?",
#             (venue_name,)
#         ).fetchone()

#         if venue is None:
#             # Venue does not exist, insert it
#             db.execute(
#                 "INSERT INTO venue (name) VALUES (?)",
#                 (venue_name,)
#             )
#             db.commit()
#             # Fetch the new venue ID
#             venue = db.execute(
#                 "SELECT id FROM venue WHERE name = ?",
#                 (venue_name,)
#             ).fetchone()
        
#         venue_id = venue['id']

#     if venue_id is None:
#         raise ValueError("Either venue_id or venue_name must be provided.")

#     # Insert the concert with the venue_id
#     db.execute(
#         'INSERT INTO concert (artist, venue_id, date, mgmt_email, mgmt_name, emailed, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
#         (artist, venue_id, date, mgmt_email, mgmt_name, False, user_id)
#     )
#     db.commit()


def update_concert(concert_id, date, artist, venue_id, mgmt_email, mgmt_name, emailed = None):
    db = get_db()
    if emailed is not None:
        db.execute(
            'UPDATE concert SET date = ?, artist = ?, venue_id = ?, mgmt_email = ?, mgmt_name = ?, emailed = ? WHERE id = ?',
            (date, artist, venue_id, mgmt_email, mgmt_name, emailed, concert_id)
        )
    else:
        db.execute(
            'UPDATE concert SET date = ?, artist = ?, venue_id = ?, mgmt_email = ?, mgmt_name = ? WHERE id = ?',
            (date, artist, venue_id, mgmt_email, mgmt_name, concert_id)
        )
    db.commit()

def get_concert(concert_id):
    db = get_db()
    return db.execute(
        'SELECT * FROM concert WHERE id = ?', (concert_id,)
    ).fetchone()

def delete_concert(concert_id):
    db = get_db()
    db.execute('DELETE FROM concert WHERE id = ?', (concert_id,))
    db.commit()

def get_all_venues():
    db = get_db()
    venues = db.execute('SELECT * FROM venue').fetchall()
    
    venue_list = []
    for venue in venues:
        venue_dict = dict(venue)
        venue_dict['minimal_substring'] = venue_dict['minimal_substring'] or ''
        venue_dict['venue_email_text'] = venue_dict['venue_email_text'] or ''
        venue_dict['aliases'] = get_aliases_by_venue_id(venue['id'])
        venue_list.append(venue_dict)

    return venue_list


def get_venue_by_id(id):
    db = get_db()
    return db.execute('SELECT * FROM venue WHERE id = ?', (id,)).fetchone()

def get_aliases_by_venue_id(venue_id):
    db = get_db()
    aliases = db.execute('SELECT * FROM venue_alias WHERE venue_id = ?', (venue_id,)).fetchall()
    return [dict(alias) for alias in aliases]

def insert_venue(name, city, address, rating):
    db = get_db()
    db.execute(
        'INSERT INTO venue (name, city, address, rating) VALUES (?, ?, ?, ?)',
        (name, city, address, rating)
    )
    db.commit()

def update_venue(id, name, city, address, rating, minimal_substring, venue_email_text):
    db = get_db()
    db.execute(
        'UPDATE venue SET name = ?, city = ?, address = ?, rating = ?, minimal_substring = ?, venue_email_text = ? WHERE id = ?',
        (name, city, address, rating, minimal_substring, venue_email_text, id)
    )
    db.commit()


def delete_venue(id):
    db = get_db()
    db.execute('DELETE FROM venue WHERE id = ?', (id,))
    db.commit()

def insert_alias(alias, venue_id):
    db = get_db()
    cursor = db.execute(
        'INSERT INTO venue_alias (alias, venue_id) VALUES (?, ?)',
        (alias, venue_id)
    )
    db.commit()
    return cursor.lastrowid

def delete_alias(id):
    db = get_db()
    db.execute('DELETE FROM venue_alias WHERE id = ?', (id,))
    db.commit()

def get_websites():
    db = get_db()
    return db.execute('SELECT * FROM website').fetchall()

def get_scrape_queries():
    db = get_db()
    return db.execute('SELECT * FROM scrape_query').fetchall()

def get_scrape_queries_by_website(website_id):
    db = get_db()
    return db.execute('SELECT * FROM scrape_query WHERE website_id = ?', (website_id,)).fetchall()

def insert_scrape_query(website_id, city, month):
    db = get_db()
    db.execute(
        'INSERT INTO scrape_query (website_id, city, month, query) VALUES (?, ?, ?, ?)',
        (website_id, city, month, '')
    )
    db.commit()

def delete_scrape_query(query_id):
    db = get_db()
    db.execute('DELETE FROM scrape_query WHERE id = ?', (query_id,))
    db.commit()