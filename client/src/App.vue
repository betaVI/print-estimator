<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <div class="d-flex mx-auto">
        <RouterLink to="/prints" v-if="$route.fullPath != '/prints'" class="btn btn-outline-info my-2 my-sm-0">Prints</RouterLink>
        <RouterLink to="/" v-if="$route.fullPath != '/'" class="btn btn-outline-info my-2 my-sm-0">Estimates</RouterLink>
        <RouterLink to="/filaments" v-if="$route.fullPath != '/filaments'" class="btn btn-outline-info my-2 my-sm-0">Filaments</RouterLink>
        <RouterLink to="/customers" v-if="$route.fullPath != '/customers'" class="btn btn-outline-info my-2 my-sm-0">Customers</RouterLink>
        <RouterLink to="/settings" class="btn btn-outline-info my-2 my-sm-0">Settings</RouterLink>
      </div>
    </div>
  </nav>
  <RouterView />
</template>

<style>
.container {
  margin-top: 20px;
}
</style>