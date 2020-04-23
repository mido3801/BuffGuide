from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,current_app, session
)
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)
import requests
import os
import json
import googlemaps

from app.db import get_db
import functools

from app.db import get_db

from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('map', __name__)


@bp.route('/')
def index(user=None,classes=None):
    db = get_db()
    departments = db.execute('SELECT DISTINCT classDept from Classes').fetchall()
    if g.user:
        userid = g.user['userID']
        classes = db.execute("SELECT userClass.classID,Classes.classTitle,Classes.classDept,Classes.classID,Classes.classCourseNum from userClass INNER JOIN Classes on userClass.classID=Classes.ClassID WHERE userClass.userID=?", (userid,)).fetchall()

    return render_template('base.html', departments=departments, user=user, classes=classes,)


@bp.route('/direct/<string:class1>/<string:class2>',methods=("POST",))
def direct(class1,class2):
    db = get_db()
    map = get_map()
    these_coords=[]
    if class1 and class2:
        coords1 = db.execute("Select Locations.locationLatitude,Locations.locationLongitude from Locations inner join locationAbbrev on Locations.locationName=locationAbbrev.locationName WHERE locationAbbrev.abbrev= ?",(class1,)).fetchone()
        coords2 = db.execute("Select Locations.locationLatitude,Locations.locationLongitude from Locations inner join locationAbbrev on Locations.locationName=locationAbbrev.locationName WHERE locationAbbrev.abbrev= ?",(class2,)).fetchone()

        these_coords.append({"lat":coords1['locationLatitude'],"lng":coords1['locationLongitude']})
        these_coords.append({"lat": coords2['locationLatitude'], "lng": coords2['locationLongitude']})

        these_directions = map.directions(these_coords[0],these_coords[1],mode="walking")

       # for x in these_directions[0]['legs']:
        #    print(x)

        legs = these_directions[0]['legs']
       # print(legs[0]['steps'])

        directions_list = [these_coords[0]]

        for x in legs[0]['steps']:
            directions_list.append(x['end_location'])

        print(directions_list)


    return jsonify(directions_list)


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


@bp.route('/add/<int:classID>', methods=['POST'])
def add_class(classID):
    db = get_db()
    class_id = classID
    this_class = db.execute("SELECT classCourseNum,classTitle,classBuilding,classRoom from Classes Where classID = ?",
                            (class_id,)).fetchall()
    if g.user:
        this_user = g.user['userID']
        this_class=classID
        db.execute('INSERT INTO UserClass (userID,classID) Values (?,?);',(this_user,this_class))
        db.commit()

    class_title = this_class[0]['classTitle']
    class_num = this_class[0]['classCourseNum']
    class_building = this_class[0]['classBuilding']
    class_room = this_class[0]['classRoom']
    print(class_building)
    return {'classTitle':class_title,"classNum":class_num,"classBuilding":class_building,"classRoom":class_room,"classID":class_id}

@bp.route('/remove/<int:classid>',methods=['POST'])
def remove_class(classid):
    db = get_db()
    if g.user:
        db.execute('delete from userClass where classID=? and userID=?',(classid,g.user['userID']))
        db.commit()
    return {"success":"true"}


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


def get_map():
    if 'map' not in g:
        g.map = googlemaps.Client(key="AIzaSyD3CjphaJ3JHXHFK9pgOppj-LQClA1KxIk")
    return g.map
