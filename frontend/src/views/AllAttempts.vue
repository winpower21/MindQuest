<template>
    <div class="container-fluid p-0">
        <Sidebar />
        <div class="hero-section d-flex">
            <div class="top-content">
                <div class="row">
                    <div>
                        <button @click="goBack" class="btn btn-dark" style="font-size: larger; margin: 0px 10px 10px 0px;"><i class="bi bi-skip-backward-fill"></i> Back</button>
                        
                    </div>
                    <!-- <div class="col-4 align-content-end justify-content-end">
                        <div class="row mb-3" style="border-radius: 10px; padding: 5px; border: 2px grey dashed;">                            
                            <div class="input-group input-group-sm">
                                <label class="col-4 col-form-label col-form-label-sm" style="font-weight: bold;" for="search"><i class="bi bi-search"></i> Search:</label>
                                <input type="text" class="form-control" id="search" v-model="searchQuery" placeholder="Query" required/>
                                <button class="btn btn-outline-primary" type="button" @click="searchFunc">Search</button>
                            </div>
                        </div>
                    </div> -->
                </div>                                
                <div class="fade-line "></div>
                <br>
                <div class="content-container">
                    <h1 class="display-6 fw-bold">All Quiz Attempts</h1>
                    <div class="px-4 py-5" v-if="userActivity === true">
                        <div class="row text-center"> 
                            <div class="col-lg-3" v-for="(subject, index) in userActivityAll" :key="index"> 
                                <div class="card px-5 py-5" style="border-radius: 10px; ">
                                    <div class="image-wrapper mb-3">
                                        <img :src="subject.subject_image_url" alt="" class="img-left rounded-circle shadow">
                                        <img :src="avatars[subject.user_id]" alt="" class="img-right rounded-circle shadow">
                                    </div>
                                    <h2 class="fw-normal">Subject: {{ subject.subject_name }}</h2> 
                                    <p>Chapter: {{ subject.chapter_name }} | Quiz: {{ subject.quiz_name }}</p>
                                    <p v-if="userRole === 'admin'">User - {{ subject.user_name }}</p> 
                                    <p>Score: {{ scorePercent(subject.score,subject.total_marks) }}%</p> 
                                    <p>Submission date - {{ formatDateTime(subject.submitted_at) }}</p> 
                                    <router-link class="btn btn-primary" :to="{ name: 'ViewUserAnswers', query: {'attempt_id':subject.attempt_id, 'user_name':subject.user_name} }">View Answers</router-link>
                                </div>
                            </div><!-- /.col-lg-4 -->                             
                        </div>
                        <br>
                    </div>
                    <div class="px-4 py-5 text-center" v-else-if="userActivity === false">
                        <h3>No user attempts</h3>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import Sidebar from "@/components/Sidebar.vue";
import fetchWithAuth from "@/utils/api";
import generateAvatarSvg from '@/utils/avatargenerator';
import formatDateTime from "@/utils/formatDateTime";
// ============================================================================================================================================
const store = useStore();
const router = useRouter();
const route = useRoute();

const quizId = ref(route.query.quiz_id)
const userRole = store.state.user?.role
const userName = store.state.user?.name;


const avatars = ref({})
// ============================================================================================================================================


// ============================================================================================================================================
const goBack = () => {
    router.go(-1);  // Goes back one step in history
};
// ============================================================================================================================================


// ============================================================================================================================================
// Get recent activity:

const userActivityAll = ref(null);
const userActivity = ref(true);
const recentActivity = async() => {
    if(quizId.value){
        try{
            const response = await fetchWithAuth(`/api/attempts/${quizId.value}`, {method:"GET"})
        
            if(response.ok){
                const data = await response.json()
                userActivityAll.value = data.all_attempts
                for (const user of userActivityAll.value){
                    const svg = await generateAvatarSvg(user.avatar_seed, user.avatar_style);
                    avatars.value[user.user_id] = `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
                }
            } else {
                const data = await response.json()
                userActivity.value = false;
            }
        } catch (error){
            console.error(error)
        }
    } else {
        try{
            const response = await fetchWithAuth(`/api/attempts`, {method:"GET"})
        
            if(response.ok){
                const data = await response.json()
                userActivityAll.value = data.all_attempts
                for (const user of userActivityAll.value){
                    const svg = await generateAvatarSvg(user.avatar_seed, user.avatar_style);
                    avatars.value[user.user_id] = `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
                }
            } else {
                const data = await response.json()
                userActivity.value = false;
            }
        } catch (error){
            console.error(error)
        }
    }
}

onMounted(() => {
    recentActivity();
})
// ============================================================================================================================================



// ============================================================================================================================================

const searchQuery = ref("");
const searchMessage = ref("")

const searchFunc = async () => {
    if (searchQuery.length < 3) {
        searchMessage.value = "Query must have atleast 3 characters"
    } else {
        router.push({name: "SearchResults", query: {"query": searchQuery.value}})
    }
}

// ============================================================================================================================================

// ============================================================================================================================================
const scorePercent = (score, fullScore) => {
    const scorePercentage = (score/fullScore)*100;
    return scorePercentage;
}
// ============================================================================================================================================
</script>

<style scoped>
.bi{
    font-size: 18px;
    margin: 0 4px 6px 0;
}
.content-container{
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
}

.subheading {
    color: #555;
}


.hero-section {
    padding-top: 80px;
    padding-left: 80px;
    padding-right: 20px;
}
.fade-line {
    height: 2px;
    width: 100%; /* Adjust width as needed */
    background: linear-gradient(to right, #000, transparent);
    opacity: 0.8; /* Optional: to make it soft */
}

.image-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0; /* Ensure no default spacing */
  position: relative;
}

.img-left,
.img-right {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f5f5f5;
}


/* Overlap the right image onto the left image */
.img-right {
  margin-left: -50px; /* Adjust this value for more/less overlap */
  z-index: 1; /* Ensure it appears above the left image */
}
.btn{
    font-weight: 600;
    min-width: 170px;
}
</style>