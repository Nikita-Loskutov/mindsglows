<script setup>
import { ref } from 'vue'


const sections = ref([
  'Релиз',
  '?',
  '?',
  '?',
  '?',
  '?',
  '?',
  '?',
  '?',
  '?',
  '?',
  'Listing?'
])
</script>

<template>
  <div class="container">
    <div class="head">
      <h1>MMMCoin</h1>
      <h2>Airdrop</h2>
    </div>
    <div v-for="(item, index) in sections" :key="index" class="new">
      <h3>{{ item }}</h3>
    </div>
  </div>
</template>

<style scoped>
    .container {
        display:block;
        margin:0 auto;
        margin-bottom:100px;
        justify-content: center;
        align-items: center;
        height:78%;
        background: #1e1e1e;
        border-radius: 30px 30px 30px 30px;
        padding: 20px;
        padding-bottom:15px;
        box-shadow: 0px 0px 8px #6366F1;
        text-align: center;
        overflow-y: auto; 
        overflow-x: hidden;
    }


    .new {
        margin:0 auto;
        margin-bottom: 15px;
        display:flex;
        height:60px;
        background: #1e1e1e;
        border-radius: 40px;
        box-shadow: 0px 0px 8px #6366F1;
        justify-content: center;
        align-items: center;
    }
</style>
