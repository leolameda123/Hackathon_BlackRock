import sqlite3
from datetime import datetime

import click
from flask import current_app, g


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
    """Clear the existing data and create new tables."""
    init_db()
    postData(datetime.now(), "/blackrock/challenge/v1/performance")
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def postData(elapsedTime, path):
    db = get_db()
    db.execute("INSERT INTO timer (elapsedTime, lastEndpointUsed) VALUES (?,?)",
    (elapsedTime, path),
    )
    db.commit()

def updateData(elapsedTime, path):
    print("commiting:", elapsedTime, path)
    db = get_db()
    db.execute("UPDATE timer set elapsedTime = ?, lastEndpointUsed = ?",
    (elapsedTime, path),
    )
    db.commit()
        
def retrieveData():
    db = get_db()
    timer = db.execute(
        'SELECT * FROM timer'
    ).fetchone()

    return timer