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
        'SELECT c.id, c.artist, v.name AS venue, c.date, c.mgmt_email, c.mgmt_name, c.emailed, c.user_id, u.username '
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

def insert_concert(artist, date, mgmt_email, mgmt_name, user_id, venue_id=None, venue_name=None):
    db = get_db()
    
    if venue_id is None and venue_name is not None:
        # Check if the venue already exists
        venue = db.execute(
            "SELECT id FROM venue WHERE name = ?",
            (venue_name,)
        ).fetchone()

        if venue is None:
            # Venue does not exist, insert it
            db.execute(
                "INSERT INTO venue (name) VALUES (?)",
                (venue_name,)
            )
            db.commit()
            # Fetch the new venue ID
            venue = db.execute(
                "SELECT id FROM venue WHERE name = ?",
                (venue_name,)
            ).fetchone()
        
        venue_id = venue['id']

    if venue_id is None:
        raise ValueError("Either venue_id or venue_name must be provided.")

    # Insert the concert with the venue_id
    db.execute(
        'INSERT INTO concert (artist, venue_id, date, mgmt_email, mgmt_name, emailed, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (artist, venue_id, date, mgmt_email, mgmt_name, False, user_id)
    )
    db.commit()


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
    return db.execute('SELECT * FROM venue').fetchall()

def get_venue_by_id(venue_id):
    db = get_db()
    return db.execute('SELECT * FROM venue WHERE id = ?', (venue_id,)).fetchone()

def insert_venue(venue_name, city = None, address = None, rating = None):
    db = get_db()
    db.execute(
        'INSERT INTO venue (name, city, address, rating) VALUES (?, ?, ?, ?)',
        (venue_name, city, address, rating)
    )
    db.commit()

def update_venue(venue_id, venue_name, city, address, rating):
    db = get_db()
    db.execute(
        'UPDATE venue SET name = ?, city = ?, address = ?, rating = ? WHERE id = ?',
        (venue_name, city, address, rating, venue_id)
    )
    db.commit()

def delete_venue(venue_id):
    db = get_db()
    db.execute('DELETE FROM venue WHERE id = ?', (venue_id,))
    db.commit()