<template>
  <div class="app">
    <header>
      <nav>
        <h1>像素画色号标注工具</h1>
        <ul>
          <li><a href="#" @click.prevent="navigate('main')" :class="{ active: currentView === 'main' }">主页</a></li>
          <li><a href="#" @click.prevent="navigate('about')" :class="{ active: currentView === 'about' }">关于</a></li>
          <li><a href="#" @click.prevent="navigate('donate')" :class="{ active: currentView === 'donate' }">打赏</a></li>
        </ul>
      </nav>
    </header>
    
    <main>
      <PixelArtTool v-if="currentView === 'main'" />
      <AboutPage v-else-if="currentView === 'about'" />
      <DonatePage v-else-if="currentView === 'donate'" />
    </main>
    
    <footer>
      <p>&copy; 2024 像素画色号标注工具 - 制作像素画更简单</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AboutPage from './components/AboutPage.vue'
import DonatePage from './components/DonatePage.vue'
import PixelArtTool from './components/PixelArtTool.vue'

const currentView = ref('main')

const navigate = (view: string) => {
  currentView.value = view
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #333;
  color: white;
  padding: 1rem;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

nav h1 {
  margin: 0;
  font-size: 1.5rem;
}

nav ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

nav li {
  margin-left: 1rem;
}

nav a {
  color: white;
  text-decoration: none;
  padding: 0.5rem;
  border-radius: 4px;
}

nav a:hover, nav a.active {
  background-color: #555;
}

main {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
}

footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1rem;
}
</style>