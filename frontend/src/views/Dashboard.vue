<template>
    <component v-if="store.state.user && store.state.user?.role" :is="dashboardComponent" :role="role"/>
</template>

<script setup>
import { computed, defineAsyncComponent } from "vue";
import { useStore } from "vuex";

const role = computed(() => store.state.user?.role || "")
const UserDashboard = defineAsyncComponent(() => import("@/components/UserDashboard.vue"))
const AdminDashboard = defineAsyncComponent(() => import("@/components/AdminDashboard.vue"))

defineOptions({ name: "Dashboard" });
const store = useStore();
const dashboardComponent = computed(() => {
    if (store.state.user?.role){
        return store.state.user?.role === "admin" ? AdminDashboard : UserDashboard;
    }
})

</script>

<style scoped>
/* div {
    margin-top: 100px;
} */
</style>