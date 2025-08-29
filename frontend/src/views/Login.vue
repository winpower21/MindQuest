<template>
    <div class="container-fluid p-0">
        <!-- Hero Section -->
        <div class="hero-section text-center text-light d-flex align-items-center justify-content-center">
            <div class="overlay"></div>
            <div class="box">
                <div class="login-content">
                    <h1>Login</h1>
                    <div class="row">
                        <label for="email" class="col-sm-2 col-form-label">Email</label>
                        <div class="col-sm-10">
                            <input type="email" class="form-control" id="email" v-model="email">
                        </div>
                    </div>
                    <div class="row">
                        <label for="password" class="col-sm-2 col-form-label">Password</label>
                        <div class="col-sm-10">
                            <input type="password" class="form-control" id="password" v-model="password">
                        </div>
                    </div>
                    <div class="pb-2" style="margin-top: 10px; margin-bottom: 10px;">
                        <button class="btn btn-primary w-100 font-weight-bold mt-2" @click="login">Login</button>
                    </div>
                    <div class="text-center">
                        <p>Don't have an account? <router-link to="/register">Register</router-link></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineOptions({ name: "Login" });

import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const email = ref(null);
const password = ref(null);
const store = useStore();
const router = useRouter();


const login = () => {
    store.dispatch('login', {email: email.value, password: password.value});
}

// Clear message when user visits the login page (ensures it only shows once)
onMounted(() => {
    if (store.state.alertMessage != null) {
        setTimeout(() => {
            console.log("clearing message!!")
            store.commit("clearAlertMessage");
        }, 4000); // Clears message after 2 seconds
    }
});



</script>

<style scoped>
.form-control {
    background-color: transparent;
    color: antiquewhite;
}

.btn{
    font-weight: 600;
}

.row{
    margin-top: 50px;
    margin-bottom: 50px;
}

.hero-section {
    position: relative;
    height: 100vh;
    /* width: calc(100vw - 60px); */
    background: url('../assets/home_res.jpeg') no-repeat center center/cover;
}
.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
}
.top-content {
    margin-top: 90px;
    position: relative;
    z-index: 1;
    color: 	#faebd7;
}
.features-section {
    background: black;/*antiquewhite;*/
}
.feature-icon {
    font-size: 3rem;
    margin-bottom: 10px;
}
.box{
    color: #faebd7;
    position: relative;
    z-index: 1;
}
.login-content{
    padding: 50px;
    text-align: center;
    background-color: rgba(0, 0, 0, 0.4);
    border-radius: 10px;
    width: 800px;
}

</style>