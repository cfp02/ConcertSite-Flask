from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
)
from werkzeug.exceptions import abort
import logging
from datetime import datetime
from flask_mail import Mail, Message

from concert_mailer.auth import login_required
from concert_mailer.db import get_concerts, count_concerts, insert_concert, update_concert, get_concert, delete_concert
from concert_mailer.email_helpers import send_email, date_manipulation, email_subject_2, template_html_1
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
            insert_concert(artist, venue, date, mgmt_email, mgmt_name, g.user['id'])
            return redirect(url_for("concert.index"))

    return render_template("concert/add.html")

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
    logging.debug(f"Incoming data: {data}")
    # logging.debug(f"Updating concert ID {concert_id} with mgmt_email: {mgmt_email}, mgmt_name: {mgmt_name}")

    try:
        update_concert(
            concert_id,
            data.get('date', concert['date']),
            data.get('artist', concert['artist']),
            data.get('venue', concert['venue']),
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
    
    mail_obj: Mail = current_app.extensions['mail']

    # concert['date'] is in the format 'YYYY-MM-DD'
    date_datetime = datetime.strptime(concert['date'], '%Y-%m-%d')

    date_subject, date = date_manipulation(date_datetime)

    placeholders = {
        'mgmt_name': concert['mgmt_name'],
        'artist': concert['artist'],
        'venue': concert['venue'],
        'location': '',
        'date': date,
        'date_subject': date_subject
    }

    try:
        ret = send_email(
            mail_obj,
            [concert['mgmt_email']],
            template_html_1,
            placeholders,
            sender='Cole Parks Photography',
            subject=email_subject_2
        )
        update_concert(concert_id, concert['date'], concert['artist'], concert['venue'], concert['mgmt_email'], concert['mgmt_name'], emailed=True)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


    # try:
    #     print('\n\n Sending email to', concert["mgmt_email"], ' with body: ', message)
    #     mail = current_app.extensions['mail']
    #     msg = Message(subject='Concert Information',
    #                   sender=current_app.config['MAIL_USERNAME'],
    #                   recipients=[concert['mgmt_email']],
    #                   body=message)
    #     mail.send(msg)
    #     logging.debug(f"Email sent to {concert['mgmt_email']} with message: {message}")
    #     # Optionally, update the emailed status
    #     update_concert(concert_id, concert['date'], concert['artist'], concert['venue'], concert['mgmt_email'], concert['mgmt_name'], emailed=True)
    #     return jsonify({'success': True})
    # except Exception as e:
    #     print(e)
    #     return jsonify({'success': False, 'message': str(e)}), 500