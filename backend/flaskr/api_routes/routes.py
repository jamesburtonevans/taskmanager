from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..db import create_task, get_tasks, get_task_by_id, delete_task, update_task

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/tasks')
def get_all_tasks():
    tasks = get_tasks()
    return jsonify(tasks)

@bp.route('/create', methods=['POST'])
def create_task_api():
    if request.method == 'POST':
        data = request.get_json()
        title = data['title']
        description = data['description']
        due_date = data['due_date']

        create_task(title, description, due_date)
        return redirect(url_for('tasks.index'))
    
    return jsonify({'message': 'Task created'}), 201

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_task_api(id):
    task = get_task_by_id(id)

    if request.method == 'POST': 
        data = request.get.json()
        title = data['title']
        description = data['description']
        due_date = data('due_date')
        status = data('status', task['status'])

        update_task(id, title, description, status, due_date)
        return redirect(url_for('tasks.index'))
    
    return jsonify({'message': 'Task updated'}), 200

@bp.route('/<int:id>/delete', methods=['DELETE'])
def delete_task_api(id):
    delete_task(id)
    return jsonify({'message': 'Task deleted'}), 200