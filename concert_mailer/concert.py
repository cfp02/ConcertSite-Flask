from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import logging
from datetime import datetime

from concert_mailer.auth import login_required
from concert_mailer.db import get_db

bp = Blueprint('concert', __name__)

logging.basicConfig(level=logging.DEBUG)

@bp.route('/')
@login_required
def index():
    db = get_db()
    today = datetime.today().date()
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Number of concerts per page
    offset = (page - 1) * per_page

    # Fetch future concerts
    future_concerts = db.execute(
        'SELECT c.id, artist, venue, date, mgmt_email, mgmt_name, user_id, username'
        ' FROM concert c JOIN user u ON c.user_id = u.id'
        ' WHERE date >= ?'
        ' ORDER BY date ASC'
        ' LIMIT ? OFFSET ?',
        (today, per_page, offset)
    ).fetchall()

    # Fetch past concerts
    past_concerts = db.execute(
        'SELECT c.id, artist, venue, date, mgmt_email, mgmt_name, user_id, username'
        ' FROM concert c JOIN user u ON c.user_id = u.id'
        ' WHERE date < ?'
        ' ORDER BY date DESC'
        ' LIMIT ? OFFSET ?',
        (today, per_page, offset)
    ).fetchall()

    # Count total future and past concerts for pagination
    total_future = db.execute(
        'SELECT COUNT(*) FROM concert WHERE date >= ?',
        (today,)
    ).fetchone()[0]

    total_past = db.execute(
        'SELECT COUNT(*) FROM concert WHERE date < ?',
        (today,)
    ).fetchone()[0]

    # Calculate total pages for future and past concerts
    total_pages_future = (total_future + per_page - 1) // per_page
    total_pages_past = (total_past + per_page - 1) // per_page

    return render_template(
        'concert/index.html',
        future_concerts=future_concerts,
        past_concerts=past_concerts,
        page=page,
        total_pages_future=total_pages_future,
        total_pages_past=total_pages_past
    )

@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    if request.method == "POST":
        artist = request.form["artist"]
        venue = request.form["venue"]
        date = request.form["date"]
        mgmt_email = request.form["mgmt_email"]
        mgmt_name = request.form["mgmt_name"]
        error = None

        if not artist:
            error = "Artist is required."

        if not venue:
            error = "Venue is required."

        if not date:
            error = "Date is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO concert (artist, venue, date, mgmt_email, mgmt_name, user_id)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (artist, venue, date, mgmt_email, mgmt_name, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("concert.index"))

    return render_template("concert/add.html")

@bp.route('/update_management/<int:concert_id>', methods=['POST'])
@login_required
def update_management(concert_id):
    data = request.json
    db = get_db()
    
    concert = db.execute(
        'SELECT * FROM concert WHERE id = ?', (concert_id,)
    ).fetchone()
    
    if concert is None:
        return jsonify({'success': False, 'message': 'Concert not found'}), 404
    
    # Handle nullable fields
    # mgmt_email = data.get('email') if data.get('email') is not None else concert['mgmt_email']
    # mgmt_name = data.get('name') if data.get('name') is not None else concert['mgmt_name']
    # print(mgmt_email, mgmt_name)
    logging.debug(f"Incoming data: {data}")
    # logging.debug(f"Updating concert ID {concert_id} with mgmt_email: {mgmt_email}, mgmt_name: {mgmt_name}")

    try:
        db.execute(
            'UPDATE concert SET date = ?, artist = ?, venue = ?, mgmt_email = ?, mgmt_name = ? WHERE id = ?',
            (
                data.get('date', concert['date']),
                data.get('artist', concert['artist']),
                data.get('venue', concert['venue']),
                data.get('mgmt_email', concert['mgmt_email']),
                data.get('mgmt_name', concert['mgmt_name']),
                concert_id
            )
        )
        db.commit()
        print('success')
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error updating concert ID {concert_id}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
