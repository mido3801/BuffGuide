from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from buffguide.db import get_db, insert_classes

bp = Blueprint('map', __name__)


@bp.route('/')
def index():
    db = get_db()
    departments = db.execute('SELECT DISTINCT classDept from Classes').fetchall()
    return render_template('base.html', departments=departments)


# Route for obtaining list of classes with certain level and department.
@bp.route('/<string:dept>/<int:level>', methods=['POST'])
def course_level(dept, level):
    db = get_db()
    upper_level = int(level) + 999
    these_classes = []
    classes = db.execute(
        "SELECT classTitle, classDept, classCourseNum FROM Classes WHERE classDEPT=? and classCourseNum BETWEEN ? AND ?",
        (dept, level, upper_level)).fetchall()
    for row in classes:
        these_classes.append(
            {'classDept': row['classDept'], 'classCourseNum': row['classCourseNum'], "classTitle": row['classTitle']})
    return jsonify(these_classes)
