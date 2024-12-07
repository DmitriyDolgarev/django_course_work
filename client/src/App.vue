<script setup>
import useUserProfileStore from '@/stores/UserProfileStore'
const userPorfileStore = useUserProfileStore()
</script>

<template>

<div class="container main">
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Машины</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/marks">Марки</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/classes">Классы</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/body-types">Типы кузовов</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/countries">Страны</router-link>
          </li>
        </ul>

        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Пользователь
            </a>
            <ul class="dropdown-menu">
              <li>
                <router-link class="dropdown-item" to="/userPage">Личный кабинет</router-link>
              </li>
              <li><a class="dropdown-item" href="/admin">Админка</a></li>
            </ul>
          </li>
        </ul>

      </div>
    </div>
  </nav>

  <div>
    <router-view/>
  </div>
</div>
</template>

<style scoped>

</style>
