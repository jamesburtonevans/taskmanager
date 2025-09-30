from flask import Blueprint, render_template, request, redirect, url_for
from ..db import create_task, get_tasks, get_task_by_id, delete_task, update_task

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('/')
def index():
    tasks = get_tasks()
    return render_template('tasks/index.html', tasks=tasks)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form.get('due_date')

        create_task(title, description, due_date)
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/create.html')

@bp.route('/<string:id>/update', methods=['GET', 'POST'])
def update(id):
    task = get_task_by_id(id)

    if request.method == 'POST': 
        title = request.form['title']
        description = request.form['description']
        due_date = request.form.get('due_date')
        status = request.form.get('status', task['status'])

        update_task(title, description, status, due_date, id)
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/update.html', task=task)

@bp.route('/<string:id>/delete', methods=['POST'])
def delete(id):
    delete_task(id)
    return redirect(url_for('tasks.index'))