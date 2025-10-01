<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const API_BASE_URL = 'http://127.0.0.1:5000/api/tasks'

const tasks = ref([])
// State for the new task form
const newTask = ref({
  title: '',
  description: '',
  due_date: ''
})

async function fetchTasks() {
  try {
    const response = await axios.get(API_BASE_URL)
    tasks.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error('Failed to fetch tasks:', error)
  }
}

async function createTask() {
  // Simple validation check
  if (!newTask.value.title) {
    alert('Title is required.')
    return
  }
  
  try {
    // Send data as JSON
    await axios.post('http://127.0.0.1:5000/api/tasks/create', newTask.value)
    
    // Clear the form and refresh the task list
    newTask.value = { title: '', description: '', due_date: '' }
    await fetchTasks()
    
  } catch (error) {
    console.error('Failed to create task:', error.response ? error.response.data : error)
    alert('Failed to create task. Check Flask console for traceback.')
  }
}

async function deleteTask(id) {
  if (!confirm('Are you sure you want to delete this task?')) {
    return
  }
  
  try {
    // Use the DELETE method
    await axios.delete(`http://127.0.0.1:5000/api/tasks/${id}/delete`)
    
    // Refresh list to show task is gone
    await fetchTasks()
  } catch (error) {
    console.error('Failed to delete task:', error.response ? error.response.data : error)
    alert('Failed to delete task.')
  }
}

onMounted(() => {
  fetchTasks()
})
</script>

<template>
  <div id="app" class="container">
    <h1 class="header">Your Task Manager (Testing API)</h1>
    
    <!-- === CREATE FORM === -->
    <div class="create-form-container">
      <h2>New Task</h2>
      <form @submit.prevent="createTask" class="create-form">
        <input v-model="newTask.title" placeholder="Title (required)" required class="form-input">
        <textarea v-model="newTask.description" placeholder="Description" class="form-input"></textarea>
        <input v-model="newTask.due_date" type="date" class="form-input">
        <button type="submit" class="create-button">Add Task</button>
      </form>
    </div>

    <!-- === TASK LIST === -->
    <h2 class="list-header">Existing Tasks</h2>
    
    <div v-if="tasks.length === 0" class="empty-message">
      No tasks found. Add a new one above.
    </div>
    
    <ul class="task-list">
      <li v-for="task in tasks" :key="task.id" class="task-item">
        <div class="task-content">
            <h2 class="task-title">{{ task.title }}</h2>
            <p class="task-description">{{ task.description }}</p>
            <div class="task-meta">
                <span :class="['status-tag', task.status]">{{ task.status }}</span>
                <span class="date-info">Due: {{ task.due_date ? task.due_date.substring(0, 10) : 'N/A' }}</span>
            </div>
        </div>
        
        <button @click="deleteTask(task.id)" class="delete-button">Delete</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* Basic styling */
.container {
  max-width: 800px;
  margin: 40px auto;
  font-family: 'Arial', sans-serif;
  padding: 0 20px;
}
.header {
  text-align: center;
  color: #2c3e50;
  padding-bottom: 10px;
  border-bottom: 3px solid #42b983;
}
.list-header {
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
    margin-top: 30px;
}
.empty-message {
  text-align: center;
  color: #7f8c8d;
  padding: 20px;
  border: 1px dashed #ccc;
  border-radius: 6px;
  margin-top: 15px;
}
/* Task List */
.task-list {
  list-style: none;
  padding: 0;
  margin-top: 15px;
}
.task-item {
  background: #f7f9fb;
  border: 1px solid #eee;
  padding: 15px;
  margin-bottom: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.task-content {
    flex-grow: 1;
}
.task-title {
  margin: 0 0 5px 0;
  color: #34495e;
  font-size: 1.2em;
}
.task-description {
  margin: 0 0 10px 0;
  color: #555;
}
.task-meta {
    display: flex;
    gap: 15px;
    font-size: 0.9em;
}
.status-tag {
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: bold;
    color: white;
}
.pending {
    background-color: #f39c12; 
}
.completed {
    background-color: #27ae60; 
}
.date-info {
    color: #7f8c8d;
}
/* Form Styling */
.create-form-container {
    padding: 20px;
    border: 1px solid #42b983;
    border-radius: 8px;
    margin-bottom: 20px;
    background-color: #e8f5e9;
}
.create-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.form-input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1em;
}
.create-button {
    background-color: #42b983;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}
.create-button:hover {
    background-color: #369c67;
}
.delete-button {
    background-color: #e74c3c;
    color: white;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.85em;
    transition: background-color 0.3s;
}
.delete-button:hover {
    background-color: #c0392b;
}
</style>
