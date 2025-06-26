<script setup>
  defineProps(['userId', 'username'])
</script>

<template>
  <div class="nav">
    <router-link :to="`/?user_id=${userId}&username=${username}`" class="nav-button">Exchange</router-link>
    <router-link :to="`/mine?user_id=${userId}&username=${username}`" class="nav-button">Mine</router-link>
    <router-link :to="`/friends?user_id=${userId}&username=${username}`" class="nav-button">Friends</router-link>
    <router-link :to="`/earn?user_id=${userId}&username=${username}`" class="nav-button">Earn</router-link>
    <router-link :to="`/airdrop?user_id=${userId}&username=${username}`" class="nav-button">Airdrop</router-link>
  </div>
</template>

<style scoped>
  .nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    padding-top: 20px;
    padding-bottom: 20px;
    user-select: none;
    background: #1e1e1e;
    z-index: 10;
    text-decoration: none;
  }

  .nav-button {
    flex: 1;
    margin: 0 5px;
    text-decoration: none;
    color: #ffffff;
    padding: 10px 0;
    background: #292929;
    border-radius: 8px;
    transition: background-color 0.3s;
    text-align: center;
    font-size: 0.9em;
    -webkit-tap-highlight-color: transparent;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .nav-button:hover {
    background-color: #383838;
    text-decoration: none;
  }
  .nav-button:active {
    outline: none; /* Убираем контур */
    background-color: #535454; /* Если нужно, можно задать другой стиль при активации */
    color: #ffffff; /* Сохраняем цвет текста */
  }

  .nav-button:focus {
    outline: none; /* Убираем контур */
    background-color: #444444; /* Если нужно, можно задать другой стиль при активации */
    color: #ffffff; /* Сохраняем цвет текста */
  }
</style>