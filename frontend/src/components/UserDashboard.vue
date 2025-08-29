<template>
    <div class="container-fluid p-0">
        <Sidebar />
        <div class="hero-section d-flex">
            <div class="top-content">
                <div class="row">
                    <div class="col col-9">
                        <h1 class="display-4 fw-bold">User Dashboard</h1>
                    </div>
                    <div class="col-3 align-content-end justify-content-end">
                        <div class="row mb-3" style="border-radius: 10px; padding: 5px; border: 2px grey dashed;">                            
                            <div class="input-group input-group-sm">
                                <label class="col-4 col-form-label col-form-label-sm" style="font-weight: bold;" for="search"><i class="bi bi-search"></i> Search:</label>
                                <input type="text" class="form-control" id="search" v-model="searchQuery" placeholder="Query" required/>
                                <button class="btn btn-outline-primary" type="button" @click="searchFunc">Search</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="fade-line"></div>
                <br>
                <div class="content-container" v-if="userSubjects.length > 0">
                    <div class="icon-grid px-2 py-2">
                        <h2 class="border-bottom">Your Subjects</h2> 
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 ">
                            <div class="col" v-for="(subject, index) in userSubjects.slice(0,4)" :key="subject.id" >
                                <div class="card rounded-4 d-flex" :class="{ 'hovered': hoveredCard === index }" @mouseover="hoveredCard = index" @mouseleave="hoveredCard = null" @click="router.push(`/subject/${subject.id}`)">
                                    <div class="card-cover  overflow-hidden text-bg-dark rounded-4 shadow-lg" :class="{ 'hovered-cover' : hoveredCard === index }" :style="{ backgroundImage: `url(${subject.image_url})`, minHeight: '250px',
                                    backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(${subject.image_url})`,
                                    backgroundSize: 'cover',
                                    backgroundRepeat: 'no-repeat',
                                    backgroundPosition: 'center'}">
                                        <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                                            <h2 class="pt-5 mt-5 mb-4 lh-1 fw-bold line-clamp">{{ subject.name }}</h2>
                                        </div>
                                    </div>
                                    <div class="card-body">
                                        <p class="card-text line-clamp" style="font-weight: 600; font-size: 18px;">{{ subject.description }}</p>
                                        <div class="row">
                                            <div class="col-4 d-flex">
                                                <i class="icon bi bi-journal-text"></i><p style="font-size: 16px;">Chapters: {{ subject.chapters.length }}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex justify-content-end">
                            <router-link to="/subjects" class="btn btn-primary mt-3">Explore More Subjects</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

import { useStore } from "vuex";
import Sidebar from "@/components/Sidebar.vue";
import fetchWithAuth from "@/utils/api";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import generateAvatarSvg from "@/utils/avatargenerator";


const store = useStore();
const hoveredCard = ref(null)
const userRole = store.state.user?.role
const userName = store.state.user?.name;
const router = useRouter();
console.log("User role:", userRole);


// ============================================================================================================================================

const searchQuery = ref("");
const searchMessage = ref("")

const searchFunc = async () => {
    if (searchQuery.length < 3) {
        searchMessage = "Query must have atleast 3 characters"
    } else {
        router.push({name: "SearchResults", query: {"query": searchQuery.value}})
    }
}

// ============================================================================================================================================


// ============================================================================================================================================
const avatar_svg = ref(null)

const getAvatar = async() => {
    const svg = await generateAvatarSvg(store.state.user.avatar_seed, store.state.user.avatar_style);
    avatar_svg.value = svg
}

const userSubjects = ref([]);
// ============================================================================================================================================



// ============================================================================================================================================
const fetchUserSubjects = async () => {
    try {
        const response = await fetchWithAuth("/api/my-subjects", {methods: "GET"});
        if (response.ok) {
            const subjects = await response.json();
            console.log("User's subjects:", subjects);
            userSubjects.value = subjects;
        } else {
            router.push({name: "Subjects"})
        }
    } catch (error) {
        console.error("Error fetching user's subjects:", error);
    }
}
// ============================================================================================================================================
onMounted(() => {
    fetchUserSubjects();
    getAvatar();
});
// ============================================================================================================================================
</script>

<style scoped>
.hero-section {
    padding-top: 80px;
    padding-left: 80px;
    padding-right: 20px;
}
.subheading {
    color: #555;
}
.fade-line {
    height: 2px;
    width: 100%; /* Adjust width as needed */
    background: linear-gradient(to right, #000, transparent);
    opacity: 0.8; /* Optional: to make it soft */
}
.content-container{
    padding: 30px;
    background-color: #cacaca   33;
    border-radius: 8px;
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
}

.line-clamp {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    min-height: 3em; /* roughly 2 lines' height depending on font-size and line-height */
}

.hovered{
    background-color: antiquewhite;
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.6);
    cursor: pointer;
}
.hovered-cover{
    margin: 5px;
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.6);
}

.card, .card-cover {
    transition: all 0.3s ease; /* <-- THIS adds smoothness */
}
</style>