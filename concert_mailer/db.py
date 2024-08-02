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
        f'SELECT c.id, artist, venue, date, mgmt_email, mgmt_name, user_id, username'
        f' FROM concert c JOIN user u ON c.user_id = u.id'
        f' WHERE date {date_filter} ?'
        f' ORDER BY date {order}'
        f' LIMIT ? OFFSET ?',
        (datetime.today().date(), limit, offset)
    ).fetchall()

def count_concerts(date_filter):
    db = get_db()
    return db.execute(
        f'SELECT COUNT(*) FROM concert WHERE date {date_filter} ?',
        (datetime.today().date(),)
    ).fetchone()[0]

def insert_concert(artist, venue, date, mgmt_email, mgmt_name, user_id):
    db = get_db()
    db.execute(
        'INSERT INTO concert (artist, venue, date, mgmt_email, mgmt_name, emailed, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (artist, venue, date, mgmt_email, mgmt_name, False, user_id)
    )
    db.commit()

def update_concert(concert_id, date, artist, venue, mgmt_email, mgmt_name, emailed = None):
    db = get_db()
    if emailed is not None:
        db.execute(
            'UPDATE concert SET date = ?, artist = ?, venue = ?, mgmt_email = ?, mgmt_name = ?, emailed = ? WHERE id = ?',
            (date, artist, venue, mgmt_email, mgmt_name, emailed, concert_id)
        )
    else:
        db.execute(
            'UPDATE concert SET date = ?, artist = ?, venue = ?, mgmt_email = ?, mgmt_name = ? WHERE id = ?',
            (date, artist, venue, mgmt_email, mgmt_name, concert_id)
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
