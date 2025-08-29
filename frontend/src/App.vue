<template>
  <div class="app-container">
    <Topbar />
    <div class="main-content">
      <router-view v-slot="{ Component }">
        <Suspense>
          <template #default>
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </template>
          <template #fallback>
            <div class="loading-screen">Loading...</div>
          </template>
        </Suspense>
      </router-view>

      <AlertMessage />
    </div>
  </div>
</template>


<!-- <template>
    <div class="app-container">
        <Topbar />
        <div class="main-content">
            <transition name="fade" mode="out-in">
                <router-view />
            </transition>            
            <AlertMessage />
        </div>
    </div>
</template> -->

<script setup>
import AlertMessage from './components/AlertMessage.vue';
import Topbar from './components/Topbar.vue';
import { useStore } from 'vuex';

const store = useStore()
const storedUser = localStorage.getItem('user');
if (storedUser) {
    store.commit('setUser', JSON.parse(storedUser));
}

</script>

<style>
.app-container {
    display: flex;
}
.main-content {
    flex-grow: 1;
    /*margin-left: 60px;  Adjust for sidebar width */   
    /*width: calc(100% - 70px);  Ensures it does not overlap */
}
/* .fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
} */
 .fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.loading-screen {
  padding: 2rem;
  text-align: center;
  font-size: 1.2rem;
  color: #555;
}
</style>