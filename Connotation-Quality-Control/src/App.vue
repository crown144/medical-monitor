<template>
  <div id="app" class="app-container">
    <!-- 这里放置页面内容 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  width: 100%;
  height: 100%;
  background-color: rgb(225, 225, 225);
  font-family: 'PingFang';
  display: flex;  
  /* justify-content: center;  */
  align-items: center;
  display: flex;
  flex-direction: column;
}
</style>
