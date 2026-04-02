<template>
  <div id="app">
    <!-- 动态风背景 -->
    <div class="wind-background">
      <!-- 大型风波纹 -->
      <div class="wind-wave"></div>
      <div class="wind-wave"></div>
      <div class="wind-wave"></div>
      <!-- 流动线条 -->
      <div class="wind-line"></div>
      <div class="wind-line"></div>
      <div class="wind-line"></div>
      <div class="wind-line"></div>
      <div class="wind-line"></div>
      <!-- 横向飘动粒子 -->
      <div class="wind-particle"></div>
      <div class="wind-particle"></div>
      <div class="wind-particle"></div>
      <div class="wind-particle"></div>
      <div class="wind-particle"></div>
      <div class="wind-particle"></div>
    </div>

    <!-- 页面内容 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* 全局样式已在 global.css 中定义 */
#app {
  width: 100%;
  height: 100vh;
  position: relative;
}
</style>
