<template>
  <div class="min-h-screen bg-grayLight">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
export default {
  components: {
    Navbar
  }
}
</script>

<style>
/* global styles can go here */
</style>
