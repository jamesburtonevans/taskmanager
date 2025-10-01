import sqlite3
import click
from flask import current_app, g
from datetime import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE']
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
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# Task management

def create_task(title, description, due_date=None):
    db = get_db()

    created_at = datetime.now().strftime('%Y-%m-%d')
    
    db.execute(
        "INSERT INTO tasks (title, description, created_at, due_date, status) VALUES (?, ?, ?, ?, ?)",
        (title, description, created_at, due_date, "incomplete")
    )
    db.commit()

def get_tasks():
    db = get_db()
    tasks = db.execute(
         "SELECT id, title, description, created_at, due_date, status FROM tasks ORDER BY created_at DESC"
    ).fetchall()
    return [dict(task) for task in tasks]

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

def update_task(title, description, status, due_date, task_id):
    db = get_db()
    db.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ?, due_date = ? WHERE id = ?",
        (title, description, status, due_date, task_id)
    )
    db.commit()