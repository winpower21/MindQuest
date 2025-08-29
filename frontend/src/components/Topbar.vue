<template>
    <div class="nav-container">
<nav class="navbar navbar-expand-lg fixed-top">
        <div class="container-fluid">
            <router-link class="navbar-brand" :to="buttonRoute" >
                <img src="@/assets/brain_ico_small.png" alt="Logo" width="40" height="30" class="d-inline-block align-text-top brand-image">
                MindQuest
            </router-link>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <!-- <div class="d-flex me-auto" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </div> -->
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item" v-if="!isLoggedin">
                        <router-link to='/' class="nav-link"><i class="nav-icon bi bi-house-fill"></i>Home</router-link>
                    </li>
                    <li class="nav-item" v-if="!isLoggedin">
                        <router-link to='/login' class="nav-link"><i class="nav-icon bi bi-door-open-fill"></i>Login</router-link>
                    </li>
                    <li class="nav-item" v-if="!isLoggedin">
                        <router-link to='/register' class="nav-link"><i class="nav-icon bi bi-box-arrow-in-right"></i>Register</router-link>
                    </li>
                    <li class="nav-item" v-if="isLoggedin">
                        <router-link class="nav-link" to="/dashboard"><i class="nav-icon bi bi-house-fill"></i>Dashboard</router-link>
                    </li>
                    <li class="nav-item" v-if="isLoggedin">
                        <a href="#" class="nav-link" @click.prevent="logout"><i class="nav-icon bi bi-door-closed-fill"></i>Logout</a>
                        <!-- <i @click.prevent="logout" class="nav-link fas fa-sign-out feature-icon"></i> -->
                    </li>
                </ul>       
            </div>
        </div>
    </nav>
    </div>
</template>

<script setup>
defineOptions({ name: "Navbar" });

import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();
const isLoggedin = computed(() => store.getters.login_status);
const isAdmin = computed(() => store.state.user?.role === 'admin');
const buttonRoute = computed(() => isLoggedin ? "/" : "/dashboard");

const logout = () => {
    store.dispatch('logout');
}
</script>


<style scoped>
.brand-image {
    margin-left: 10px;
    margin-right: 10px;
}

nav {
    background-image: linear-gradient(to right, rgba(27, 23, 19), #b67a5d);
}



a {
    color: antiquewhite;
    text-decoration: none;
}
li{
    padding-left: 10px;
    padding-right: 10px;
}
a:hover, a:focus {
    color: #f79b65; /* Same as antiquewhite but ensures it applies */
    text-decoration: underline;
}

.router-link-active, .router-link-exact-active {
    color: #ffcc00; /* Highlight active item */
    font-weight: bold;
}
.navbar-brand{
    color: antiquewhite !important; 
    font-weight: bold;
}

.nav-icon {
    font-size: 24px;
    padding-right: 10px;
}
</style>
