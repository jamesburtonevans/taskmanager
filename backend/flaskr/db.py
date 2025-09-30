import sqlite3

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
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
def init_db_command():
    #Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# Task management

def create_task(title, description, due_date=None):
    db = get_db()

    from datetime import datetime
    if due_date:
        due_date = datetime.strptime(due_date, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
    else:
        due_date = None


    db.execute(
        "INSERT INTO tasks (title, description, created_at, due_date, status) VALUES (?, ?, ?, ?, ?)",
        (title, description, datetime.now(), due_date, "pending")
    )
    db.commit()

def get_tasks():
    db = get_db()
    tasks = db.execute(
        "SELECT * FROM tasks"
    ).fetchall()
    return tasks 

def get_task_by_id(task_id):
    db = get_db()
    task = db.execute(
        "SELECT id, title, description, created_at, due_date, status FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    return task

def delete_task(task_id):
    db = get_db()
    db.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
        )
    db.commit()

    def update_task(title, description, status, task_id):
        db = get_db()
        db.execute(
            "UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
            (title, description, status, task_id)
        )
    db.commit