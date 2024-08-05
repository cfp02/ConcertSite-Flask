
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from concert_mailer.auth import login_required
from concert_mailer.db import get_all_venues, get_venue_by_id, insert_venue, update_venue, delete_venue

bp = Blueprint('venue', __name__)

@bp.route('/venue')
@login_required
def index():
    venues = get_all_venues()
    return render_template('venue/index.html', venues=venues)

@bp.route('/venue/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        address = request.form['address']
        rating = request.form['rating']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            insert_venue(name, city, address, rating)
            return redirect(url_for('venue.index'))

    return render_template('venue/add.html')

@bp.route('/venue/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    venue = get_venue_by_id(id)

    if venue is None:
        abort(404)

    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        address = request.form['address']
        rating = request.form['rating']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            update_venue(id, name, city, address, rating)
            return redirect(url_for('venue.index'))

    return render_template('venue/edit.html', venue=venue)

@bp.route('/venue/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    delete_venue(id)
    return redirect(url_for('venue.index'))
