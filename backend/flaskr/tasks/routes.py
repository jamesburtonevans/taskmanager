from flask import Blueprint, render_template, request, redirect, url_for
from ..db import create_task, get_tasks, get_task_by_id, delete_task 

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

        print(f'Due date before create_task: {due_date}')

        create_task(title, description, due_date)
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/create.html')
