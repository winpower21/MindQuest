<template>
    <div class="container-fluid p-0">
        <!-- Hero Section -->
        <div class="hero-section text-center text-light d-flex align-items-center justify-content-center">
            <div class="overlay"></div>
            <div class="container top-content">
                <div class="row gx-5 gy-5">
                    <div class="col-md-8 gx-5 gy-5">
                        <h1 class="display-3 fw-bold">MindQuest</h1>
                        <p class="lead">Challenge your mind, master new skills, and track your progress.</p>
                        <router-link class="btn btn-primary btn-lg" :to="buttonRoute">Get Started</router-link>
                    </div>
                    <div class="col-6 col-md-4 gx-5 gy-5">
                        <i class="fas fa-envelope feature-icon"></i>
                        <h3>Daily Reminders & Reports</h3>
                        <p>Stay on track with daily email reminders and performance reports to help you improve.</p>
                    </div>
                    
                </div>
                <div class="row">
                    <div class="col-6 col-md-4 gx-5 gy-5">
                        <i class="fas fa-brain feature-icon"></i>
                        <h3>Engaging Quizzes</h3>
                        <p>Experience interactive and fun quizzes across multiple subjects.</p>
                    </div>
                    <div class="col-6 col-md-4 gx-5 gy-5">
                        <i class="fas fa-chart-bar feature-icon"></i>
                        <h3>Track Progress</h3>
                        <p>Monitor your performance and improve with detailed analytics.</p>
                    </div>
                    <div class="col-6 col-md-4 gx-5 gy-5">
                        <i class="fas fa-stopwatch feature-icon"></i>
                        <h3>Time-based Challenges</h3>
                        <p>Compete against the clock to test your knowledge.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from "vue";;
import { useStore } from 'vuex';
defineOptions({ name: "Home" });

const store = useStore();
const isLoggedin = store.getters.login_status;
const buttonRoute = computed(() => isLoggedin ? "/dashboard" : "/login")



</script>

<style scoped>
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
</style>