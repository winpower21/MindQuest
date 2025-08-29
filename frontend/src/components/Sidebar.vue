<template>
    <div class="sidebar">
        <nav>
            <ul>
                <li class="nav-item" v-if="isLoggedin" @mouseenter="showTooltip('Dashboard')" @mouseleave="hideTooltip">
                    <router-link class="nav-link" to="/dashboard">
                        <i class="nav-icon bi bi-house-fill"></i>
                    </router-link>
                    <span v-if="tooltip === 'Dashboard'" class="tooltip">Dashboard</span>
                </li>
                <li class="nav-item" v-if="isLoggedin" @mouseenter="showTooltip('All Subjects')" @mouseleave="hideTooltip">
                    <router-link class="nav-link" to="/subjects">
                        <i class="nav-icon bi bi-book-half"></i>
                    </router-link>
                    <span v-if="tooltip === 'All Subjects'" class="tooltip">All Subjects</span>
                </li>
                <li class="nav-item" v-if="isLoggedin && isAdmin" @mouseenter="showTooltip('Manage Users')" @mouseleave="hideTooltip">
                    <router-link class="nav-link" to="/users">
                        <i class="nav-icon bi bi-people-fill"></i>
                    </router-link>
                    <span v-if="tooltip === 'Manage Users'" class="tooltip">Manage Users</span>
                </li>
                <li class="nav-item" v-if="isLoggedin && isAdmin" @mouseenter="showTooltip('Statistics')" @mouseleave="hideTooltip">
                    <router-link class="nav-link" to="/statistics">
                        <i class="nav-icon bi bi-clipboard2-data-fill"></i>
                    </router-link>
                    <span v-if="tooltip === 'Statistics'" class="tooltip">Statistics</span>
                </li>
                <li class="nav-item" v-if="isLoggedin" @mouseenter="showTooltip('User Profile')" @mouseleave="hideTooltip">
                    <img :src="`data:image/svg+xml;utf8,${encodeURIComponent(avatar_svg)}`" alt="" style="height: 30px; width: 30px; border-radius: 5px; border: 2px solid antiquewhite;" @click="router.push('/user-profile')">
                    <span v-if="tooltip === 'User Profile'" class="tooltip">User Profile</span>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import generateAvatarSvg from "@/utils/avatargenerator";

const store = useStore();
const router = useRouter();
const tooltip = ref(null);

const avatar_svg = ref(null)

const getAvatar = async() => {
    const svg = await generateAvatarSvg(store.state.user.avatar_seed, store.state.user.avatar_style);
    avatar_svg.value = svg
}

const isLoggedin = computed(() => store.getters.login_status);
const isAdmin = computed(() => store.state.user?.role === 'admin');
const showTooltip = (name) => {
    tooltip.value = name;
};

const hideTooltip = () => {
    tooltip.value = null;
};

const logout = () => {
    store.dispatch('logout');
}

onMounted(getAvatar)

</script>

<style scoped>
.sidebar {
    position: fixed;
    left: 0;
    top: 60px;
    width: 60px;
    height: 100vh;
    background-image: linear-gradient(rgba(27, 23, 19), #b67a5d);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

nav li {
    width: 100%;
    text-align: center;
    padding: 15px 0;
    position: relative;
    cursor: pointer;
}

.nav-icon {
    font-size: 24px;
    color: #b67a5d;
}

nav li:hover .nav-icon {
    color: #7D3318;
}

.tooltip {
    position: absolute;
    left: 65px;
    top: 50%;
    transform: translateY(-50%);
    background: black;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    white-space: nowrap;
    font-size: 12px;
    opacity: 1;
    visibility: visible; /* Always show when v-if is true */
}

.router-link-active .nav-icon, .router-link-exact-active .nav-icon {
        color: #ff7300 !important; /* Highlight active item */
        font-weight: bold;
    }

</style>
