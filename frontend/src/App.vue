<script setup>
  import axios from 'axios'
  import {ref, onMounted} from 'vue'
  const tasks = ref([])

  async function fetchTasks() {
    const response = await axios.get('http://localhost:5000/tasks')
    tasks.value = response.data
  }
  
  onMounted(() => {
    fetchTasks()
  })
</script>

<template>
  <h1>Here are your tasks!</h1>
  <p>
    <li v-for="name in tasks">
      {{ task.name }}
    </li>
  </p>
</template>

<style scoped></style>
