from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
)
from werkzeug.exceptions import abort
import logging
from datetime import datetime
from flask_mail import Mail, Message

from concert_mailer.auth import login_required
from concert_mailer.db import get_concerts, count_concerts, insert_concert, update_concert, get_concert, delete_concert, get_venue_by_id, get_all_venues
from concert_mailer.email_helpers import generate_email, generate_concert_email, send_email, date_manipulation, email_subject_2, template_html_1
# from concert_mailer import mail_obj as mail

bp = Blueprint('concert', __name__)

logging.basicConfig(level=logging.DEBUG)


@bp.route('/')
@login_required
def index():
    # db = get_db()
    today = datetime.today().date()
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Number of concerts per page
    offset = (page - 1) * per_page


    # Fetch future concerts
    future_concerts = get_concerts('>=', 'ASC', per_page, offset)

    # Fetch past concerts
    past_concerts = get_concerts('<', 'DESC', per_page, offset)

    # Fetch all venues
    venues = get_all_venues()

    # Count total future and past concerts for pagination
    total_future = count_concerts('>=')
    total_past = count_concerts('<')

    # Calculate total pages for future and past concerts
    total_pages_future = (total_future + per_page - 1) // per_page
    total_pages_past = (total_past + per_page - 1) // per_page

    return render_template(
        'concert/index.html',
        future_concerts=future_concerts,
        past_concerts=past_concerts,
        venues = venues,
        page=page,
        total_pages_future=total_pages_future,
        total_pages_past=total_pages_past
    )

@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    if request.method == "POST":
        artist = request.form["artist"]
        venue_id = request.form["venue_id"]
        date = request.form["date"]
        mgmt_email = request.form["mgmt_email"]
        mgmt_name = request.form["mgmt_name"]
        error = None

        if not artist:
            error = "Artist is required."

        if not venue_id:
            error = "Venue is required."

        if not date:
            error = "Date is required."

        if error is not None:
            flash(error)
        else:
            print("Venue id: ", venue_id)
            insert_concert(artist, venue_id, date, mgmt_email, mgmt_name, g.user["id"])
            return redirect(url_for("concert.index"))
    
    venues = get_all_venues()

    return render_template("concert/add.html", venues = venues)

@bp.route('/update_management/<int:concert_id>', methods=['POST'])
@login_required
def update_management(concert_id):
    data = request.json
    concert = get_concert(concert_id)
    
    if concert is None:
        return jsonify({'success': False, 'message': 'Concert not found'}), 404
    
    # Handle nullable fields
    # mgmt_email = data.get('email') if data.get('email') is not None else concert['mgmt_email']
    # mgmt_name = data.get('name') if data.get('name') is not None else concert['mgmt_name']
    # print(mgmt_email, mgmt_name)
    logging.debug(f"Incoming data: id: {concert_id} {data}")
    # logging.debug(f"Updating concert ID {concert_id} with mgmt_email: {mgmt_email}, mgmt_name: {mgmt_name}")

    try:
        update_concert(
            concert_id,
            data.get('date', concert['date']), # Looks for date in the incoming data, if not found, uses the existing date from the concert database call
            data.get('artist', concert['artist']),
            data.get('venue_id', concert['venue_id']), # Takes venue ID from the concert database call
            data.get('mgmt_email', concert['mgmt_email']),
            data.get('mgmt_name', concert['mgmt_name'])
        )
        print('success')
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error updating concert ID {concert_id}: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/delete/<int:concert_id>', methods=['POST'])
@login_required
def delete(concert_id):
    delete_concert(concert_id)
    return redirect(url_for('concert.index'))


@bp.route('/send_email/<int:concert_id>', methods=['POST'])
@login_required
def send_concert_email(concert_id):
    data = request.json
    
    concert = get_concert(concert_id)
    if concert is None:
        return jsonify({'success': False, 'message': 'Concert not found'}), 404
    
    print("Sending email for concert ID ", concert_id)
    
    mail_obj, message = generate_concert_email(concert_id)

    try:
        send_email(mail_obj, message)
        update_concert(concert_id, concert['date'], concert['artist'], concert['venue_id'], concert['mgmt_email'], concert['mgmt_name'], emailed=True)
        email_content = message.html or message.body
        return jsonify({'success': True, 'email_content': email_content})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    

@bp.route('/fetch_email_content/<int:concert_id>', methods=['GET'])
@login_required
def fetch_email_content(concert_id):
    concert = get_concert(concert_id)
    
    if concert is None:
        return jsonify({'success': False, 'message': 'Concert not found'}), 404
    print(concert['artist'])
    try:
        # Generate the email content for the given concert
        mail_obj, message = generate_concert_email(concert_id)
        email_content = message.html or message.body
        email_subject = message.subject
        email_address = concert['mgmt_email']
        
        return jsonify({'success': True, 'email_content': email_content, 'email_subject': email_subject, 'email_address': email_address})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/delete_concert/<int:concert_id>', methods=['POST'])
def delete_concert_route(concert_id):
    try:
        delete_concert(concert_id)
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Failed to delete concert'})
