<template>
  <div>
    <h1>My Tasks</h1>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} | {{ task.description }} | {{  task.status }} | {{ task.due_date }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tasks: []
    };
  },
  created() {
    this.fetchTasks();
  },
  methods: {
    async fetchTasks() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/tasks');
        this.tasks = response.data;
      } catch (error) {
        console.error('There was an error fetching the tasks:', error);
      }
    }
  }
};
</script>