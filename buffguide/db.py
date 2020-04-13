import sqlite3
import buffguide.parse as parse
import click
from flask import current_app, g
from flask.cli import with_appcontext
from buffguide.parse import *


# Called when app is made to add command line commands
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(insert_classes_command)


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    # clear existing data and create new tables
    init_db()
    click.echo('Initialized the database')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('insert-classes')
@with_appcontext
def insert_classes_command():
    insert_classes()
    click.echo('Inserted Classes')


# Insert classes into database from text file.
def insert_classes():
    db = get_db()
    classesFrame = parse.text_to_dataframe()
    classesFrame.to_sql('Classes', db, if_exists='replace')
    return db
