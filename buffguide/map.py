from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,current_app, session
)
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)
import requests
import os
import json

from buffguide.db import get_db
import functools

from buffguide.db import get_db

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('map', __name__)


@bp.route('/')
def index(user=None):
    db = get_db()
    departments = db.execute('SELECT DISTINCT classDept from Classes').fetchall()
    return render_template('base.html', departments=departments, user=user)


# Route for obtaining list of classes with certain level and department.
@bp.route('/<string:dept>/<int:level>', methods=['POST'])
def course_level(dept, level):
    db = get_db()
    upper_level = int(level) + 999
    these_classes = []
    classes = db.execute(
        "SELECT classID,classTitle, classDept, classCourseNum FROM Classes WHERE classDEPT=? and classCourseNum BETWEEN ? AND ?",
        (dept, level, upper_level)).fetchall()
    for row in classes:
        these_classes.append(
            {'classDept': row['classDept'], 'classCourseNum': row['classCourseNum'], "classTitle": row['classTitle'], "classID": row['classID']})
    return jsonify(these_classes)


@bp.route('/add/<string:classInfo>/<int:classID>', methods=['POST'])
def add_class(classInfo,classID):
    db = get_db()
    if g.user:
        this_user = g.user['userID']
        this_class=classID
        db.execute('INSERT INTO UserClass (userID,classID) Values (?,?);',(this_user,this_class))
        db.commit()
    return {'classInfo':classInfo}


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT userID FROM users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO users (userName, userPass) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return render_template('base.html')

        flash(error)

    return render_template('register.html')


@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['userPass'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userID']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE userID = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))