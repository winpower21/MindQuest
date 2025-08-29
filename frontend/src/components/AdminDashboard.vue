sear<template>
    <div class="container-fluid p-0">
        <Sidebar />
        <div class="hero-section d-flex">
            <div class="top-content">
                <div class="row">
                    <div class="col col-8">
                        <h1 class="display-4 fw-bold">Admin Panel</h1>
                    </div>
                    <div class="col-4 align-content-end justify-content-end">
                        <div class="row mb-3" style="border-radius: 10px; padding: 5px; border: 2px grey dashed;">
                            <div class="input-group input-group-sm">
                                <label class="col-4 col-form-label col-form-label-sm" style="font-weight: bold;"
                                    for="search"><i class="bi bi-search"></i> Search:</label>
                                <input type="text" class="form-control" id="search" v-model="searchQuery"
                                    placeholder="Query" required />
                                <button class="btn btn-outline-primary" type="button"
                                    @click="searchFunc">Search</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="fade-line "></div>
                <br>
                <div class="content-container">
                    <h2>Quick Actions</h2>
                    <div class="px-4 py-5 text-center">
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5">
                            <div class="col">
                                <div class="align-items-center justify-content-center">
                                    <i class="bi bi-journal-album" style="font-size:50px;"></i>
                                    <h5>Create Subjects</h5>
                                </div>
                                <p>Create new subjects.</p>
                                <button @click="showModal" v-if="userRole === 'admin'"
                                    class="fixed-button btn btn-primary">Add Subject</button>
                            </div>
                            <div class="col">
                                <div class="align-items-center justify-content-center">
                                    <i class="bi bi-journal-plus" style="font-size:50px;"></i>
                                    <h5>Manage Subjects</h5>
                                </div>
                                <p>Modify or delete existing subjects.</p>
                                <router-link to="/subjects" class="btn btn-primary">Manage Subjects</router-link>
                            </div>
                            <div class="col">
                                <div class="align-items-center justify-content-center">
                                    <i class="bi bi-people-fill" style="font-size:50px;"></i>
                                    <h5>Manage Users</h5>
                                </div>
                                <p>Manage user access to the platform.</p>
                                <router-link to="/users" class="btn btn-primary">Manage Users</router-link>
                            </div>
                            <div class="col">
                                <div class="align-items-center justify-content-center">
                                    <i class="bi bi-graph-up" style="font-size:50px;"></i>
                                    <h5>View Statistics</h5>
                                </div>
                                <p>View recent statistics.</p>
                                <router-link to="/statistics" class="btn btn-primary">View Statistics</router-link>
                            </div>
                        </div>
                    </div>
                    <hr>
                    <h2>Recent Quiz Attempts</h2>
                    <div class="px-4 py-5" v-if="userActivity === true">
                        <div class="row text-center">
                            <div class="col-lg-3" v-for="(subject, index) in userActivityAll.slice(0, 4)" :key="index">
                                <div class="card px-5 py-5" style="border-radius: 10px; ">
                                    <div class="image-wrapper mb-3">
                                        <img :src="subject.subject_image_url" alt=""
                                            class="img-left rounded-circle shadow">
                                        <img :src="avatars[subject.user_id]" alt=""
                                            class="img-right rounded-circle shadow">
                                    </div>
                                    <h2 class="fw-normal">{{ subject.subject_name }}</h2>
                                    <p>{{ subject.chapter_name }} : {{ subject.quiz_name }}</p>
                                    <p>User - {{ subject.user_name }}</p>
                                    <p>Submission date - {{ formatDateTime(subject.submitted_at) }}</p>
                                    <router-link class="btn btn-primary"
                                        :to="{ name: 'ViewUserAnswers', query: { 'attempt_id': subject.attempt_id, 'user_name': subject.user_name } }">View
                                        Answers</router-link>
                                </div>
                            </div><!-- /.col-lg-4 -->
                        </div>
                        <br>
                        <div class="d-flex align-items-end justify-content-end">
                            <button class="btn btn-outline-primary" @click="router.push({name:'AllAttempts'})">View More Responses</button>
                        </div>
                        <hr>
                    </div>
                    <div class="px-4 py-5 text-center" v-else-if="userActivity === false">
                        <h3>No user attempts</h3>
                    </div>
                </div>
                <br>
                <div ref="newSubjectModal" class="modal fade" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Create Subject</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <h3>Add new Subject</h3>
                                <div class="mb-3">
                                    <label for="subjectName" class="form-label">Name</label>
                                    <input v-model="subjectName" type="text" class="form-control" id="subjectName"
                                        placeholder="Subject Name">
                                </div>
                                <div class="mb-3">
                                    <label for="subjectDescription" class="form-label">Descirption</label>
                                    <input v-model="subjectDescription" type="text" class="form-control"
                                        id="subjectDescription" placeholder="Subject Description">
                                </div>
                                <div class="mb-3">
                                    <label for="search" class="form-label">Search Cover Image</label>
                                    <div class="d-flex">
                                        <input v-model="search" type="text" class="form-control" id="coverImage">
                                        <button class="btn btn-primary" @click="searchImage">Search</button>
                                    </div>
                                </div>
                                <div>
                                <div class="row g-2" v-if="imagePrevUrlList.length > 0">
                                    <div v-for="(image_url, index) in imagePrevUrlList" :key="index" class="col-12 col-sm-6 col-md-4">
                                        <img :src="image_url" class="img-fluid rounded album-img" :class="{ 'selected-image': coverImage === imageUrlList[index] }" @click="coverImage = imageUrlList[index]" style="cursor: pointer; max-height: 200px; max-width: 100%; ">
                                    </div>
                                </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                <button @click="createSubject" class="btn btn-primary">Submit</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { Modal } from "bootstrap";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import Sidebar from "@/components/Sidebar.vue";
import fetchWithAuth from "@/utils/api";
import generateAvatarSvg from '@/utils/avatargenerator';
import formatDateTime from "@/utils/formatDateTime";
// ============================================================================================================================================

const unsplashAccessKey = import.meta.env.VITE_UNSPLASH_ACCESS_KEY;
const store = useStore();
const router = useRouter();
const subjectName = ref(null);
const subjectDescription = ref(null);
const coverImage = ref(null);

const userRole = store.state.user?.role
const userName = store.state.user?.name;
console.log("User role:", userRole);

const newSubjectModal = ref(null);
let modalInstance = null;
const avatars = ref({})
// ============================================================================================================================================



// ============================================================================================================================================
// Get recent activity:
const userActivityToday = ref([]);
const userActivityAll = ref([]);
const userActivity = ref(true);
const recentActivity = async () => {
    try {
        const response = await fetchWithAuth("/api/attempts", { method: "GET" })

        if (response.ok) {
            const data = await response.json()
            userActivityAll.value = data.all_attempts
            userActivityToday.value = data.attempts_today
            for (const user of userActivityAll.value) {
                const svg = await generateAvatarSvg(user.avatar_seed, user.avatar_style);
                avatars.value[user.user_id] = `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
            }
        } else {
            const data = await response.json()
            userActivity.value = false;
        }
    } catch (error) {
        console.error(error)
    }
}

onMounted(() => {
    recentActivity();
})
// ============================================================================================================================================



// ============================================================================================================================================
const search = ref(null);
const imageUrlList = ref([]);
const imagePrevUrlList = ref([]);

const searchImage = async () => {
    try {
        const response = await fetch(`https://api.unsplash.com/search/photos?client_id=${unsplashAccessKey}&page=1&query=${search.value}&orientation=landscape&per-page=9`, {method: "GET"});
        if (response.ok) {
            const data = await response.json();
            imageUrlList.value = data.results.map(image => image.urls.regular);
            imagePrevUrlList.value = data.results.map(image => image.urls.small);
            console.log(imageUrlList.value);
        } else {
            const errorData = await response.json();
            store.dispatch('alertMessage', errorData.message);
        }
    } catch (error) {
        console.error("Error searching images:", error);
    }
}
// ============================================================================================================================================



// ============================================================================================================================================

const searchQuery = ref("");
const searchMessage = ref("")

const searchFunc = async () => {
    if (searchQuery.length < 3) {
        searchMessage = "Query must have atleast 3 characters"
    } else {
        router.push({ name: "SearchResults", query: { "query": searchQuery.value } })
    }
}

// ============================================================================================================================================



// ============================================================================================================================================
const createSubject = async () => {
    try {
        const response = await fetchWithAuth('/api/subject', {
            method: "POST",
            body: JSON.stringify({
                "name": subjectName.value,
                "description": subjectDescription.value,
                "image_url": coverImage.value
            })
        })
        if (response.ok) {
            const data = await response.json();
            store.dispatch("alertMessage", data.message)
            console.log(data.message);
            modalInstance.hide();  //Close modal after successful submission
        } else {
            const data = await response.json();
            store.dispatch("alertMessage", data.message);
            console.log(data.message);
            modalInstance.hide();  //Close modal after successful submission
        }
    } catch (error) {
        console.log(error)
        modalInstance.hide();  //Close modal after successful submission
    }
}
// ============================================================================================================================================





// ============================================================================================================================================
// Add subject modal
onMounted(async () => {
    await nextTick(); // Ensures the DOM is fully rendered before initializing modal
    if (newSubjectModal.value) {
        modalInstance = new Modal(newSubjectModal.value);
    }
});

const showModal = () => {
    if (!modalInstance && modalRnewSubjectModalef.value) {
        modalInstance = new Modal(newSubjectModal.value);
    }
    modalInstance?.show();
};
// ============================================================================================================================================
</script>

<style scoped>
.bi {
    font-size: 18px;
    margin: 0 4px 6px 0;
}

.content-container {
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
    width: 100%;
    /* Adjust width as needed */
    background: linear-gradient(to right, #000, transparent);
    opacity: 0.8;
    /* Optional: to make it soft */
}

.image-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    /* Ensure no default spacing */
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
    margin-left: -50px;
    /* Adjust this value for more/less overlap */
    z-index: 1;
    /* Ensure it appears above the left image */
}

.btn {
    font-weight: 600;
    min-width: 170px;
}
</style>