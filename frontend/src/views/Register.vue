<template>
    <div class="container-fluid p-0">
        <!-- Hero Section -->
        <div class="hero-section text-center text-light d-flex align-items-center justify-content-center">
            <div class="overlay"></div>
            <div class="box">
                <div class="register-content">
                    <h1>Register</h1>
                    <div class="row">
                        <label for="name" class="col-sm-2 col-form-label">Name</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" id="name" v-model="name">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 col-sm-12">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" v-model="email">
                        </div>
                        <div class="col-md-6 ">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" v-model="password">
                        </div>
                    </div>
                    <div class="avatar-grid">
                    <img
                        v-for="(avatar, index) in avatars"
                        :key="index"
                        :src="`data:image/svg+xml;utf8,${encodeURIComponent(avatar.svg)}`"
                        class="avatar-option"
                        :class="{ 'selected-avatar': avatar.seed === selectedSeed }"
                        @click="selectAvatar(avatar.seed, avatar.style)"
                    />
                    <button class="btn btn-sm btn-outline-info" @click="generateAvatars">Reload Images</button>
                    </div>
                    <div class="pb-2">
                        <button class="btn btn-primary w-100 font-weight-bold mt-2" @click="register">Register</button>
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

const name = ref(null);
const email = ref(null);
const password = ref(null);
const store = useStore();
const router = useRouter();



// -----------------------------------------------------------------------------------------------------------

import generateAvatarSvg from '@/utils/avatargenerator';

const avatars = ref([]);
const selectedSeed = ref(null);
const selectedStyle = ref(null);
const availableStyles = [
    'micah',
    'bottts',
    'adventurer',  
    'pixelArt',
    'croodles',
    'notionists',
]
const generateAvatars = async () => {
    const temp = [];
    for (let i = 0; i < 10; i++) {
        const seed = Math.random().toString(4).substring(2, 10)
        const style = availableStyles[Math.floor(Math.random() * availableStyles.length)];
        const svg = await generateAvatarSvg(seed, style);
        temp.push({ seed, style, svg });
    }
    avatars.value = temp;
}
onMounted(generateAvatars);

function selectAvatar(seed, style) {
    selectedSeed.value = seed;
    selectedStyle.value = style;
  // Save selected avatar seed to user profile or state
}

// -----------------------------------------------------------------------------------------------------------




const register = async() => {
    try{
        const response = await fetch('/api/register', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name.value,
                email: email.value,
                password: password.value,
                avatar_seed: selectedSeed.value,
                avatar_style: selectedStyle.value
            })  
        });
        if (response.ok){
            const data = await response.json();
            store.dispatch('alertMessage', "Registration successful. Redirecting to login page.");
            setTimeout(() => {
                router.push({ name: 'Login' });
            }, 3000); // Redirect after 3 seconds
        } else {
            const errorData = await response.json();
            store.dispatch('alertMessage', errorData.message);
        }
    } catch (error) {
        console.error("Error during registration:", error);
        store.dispatch('alertMessage', "Registration failed. Please try again.");
        return;
    }
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
.register-content{
    margin-top: 60px;
    padding: 50px;
    text-align: center;
    background-color: rgba(0, 0, 0, 0.4);
    border-radius: 10px;
    width: 800px;
}


/* ================================================================================================================ */
.avatar-option svg {
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    /* object-fit: contain; */
    display: block;
}

.avatar-svg svg {
    width: 128px;
    height: 128px;
}
.avatar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(128px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.avatar-option {
  cursor: pointer;
  padding: 4px;
  transition: transform 0.2s, border-color 0.2s;
  border-radius: 10px;
  border: 2px solid transparent;
}

.avatar-option:hover {
  transform: scale(1.05);
  border-color: #007bff;
}


.selected-avatar {
    border: 4px solid #007bff;
    box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
}
</style>