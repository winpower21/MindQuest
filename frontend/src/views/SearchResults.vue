<template>
    <div class="container-fluid p-0" v-if="searchData">
        <Sidebar />
        <div class="hero-section">
            <div class="top-content">
                <div class="container-fluid">
                    <div class="row">
                        <div class="col col-8">
                            <button @click="goBack" class="btn btn-dark"
                                style="font-size: larger; margin: 0px 10px 10px 0px;"><i
                                    class="bi bi-skip-backward-fill"></i> Back to Dashboard</button>
                        </div>
                        <div class="col-4 align-content-end justify-content-end">
                            <div class="row mb-3" style="border-radius: 10px; padding: 5px; border: 2px grey dashed;">
                                <div class="input-group input-group-sm">
                                    <label class="col-4 col-form-label col-form-label-sm" style="font-weight: bold;"
                                        for="search"><i class="bi bi-search"></i> Search:</label>
                                    <input type="text" class="form-control" id="search" v-model="searchQuery"
                                        placeholder="Query" required />
                                    <button class="btn btn-outline-primary" type="button"
                                        @click="searchF">Search</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="subjects card mx-2 my-2 px-5 py-4 rounded-4" id="custom-cards"
                        style="box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);">
                        <h1>Subjects</h1>
                        <hr>
                        <h4 v-if="searchData['subjects'] === null">No subjects found</h4>
                        <div v-if="searchData['subjects'] !== null"
                            class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5">
                            <div v-for="(item, index) in searchData['subjects']" :key="item.id || index"
                                class="col h-100">
                                <div class="card rounded-4 d-flex flex-column h-100"
                                    :class="{ 'hovered': hoveredSubject === item.id }"
                                    @mouseover="hoveredSubject = item.id" @mouseleave="hoveredSubject = null">
                                    <div class="card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg"
                                        :class="{ 'hovered-cover': hoveredSubject === item.id }" :style="{
                                            backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(${item.image_url})`,
                                            backgroundSize: 'cover',
                                            backgroundRepeat: 'no-repeat',
                                            backgroundPosition: 'center',
                                            minHeight: '250px'
                                        }">
                                        <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                                            <h2 class="pt-5 mt-5 mb-4 lh-1 fw-bold line-clamp">{{ item.name }}</h2>
                                        </div>
                                    </div>
                                    <div class="card-body">
                                        <p class="card-text line-clamp" style="font-weight: 600; font-size: 18px;">{{
                                            item.description }}</p>
                                        <div class="row g-2">
                                            <div class="col-6 d-flex">
                                                <i class="icon bi bi-journal-text"></i>
                                                <p style="font-size: 16px;">Chapters: {{ item.chapters.length }}</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card-footer d-flex align-content-end justify-content-end">
                                        <button class="btn btn-outline-dark"
                                            @click="router.push(`/subject/${item.id}`)">View</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="chapters card mx-2 my-2 px-5 py-4 rounded-4" id="custom-cards"
                        style="box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);">
                        <h1>Chapters</h1>
                        <hr>
                        <h4 v-if="searchData['chapters'] === null">No chapters found</h4>
                        <div v-if="searchData['chapters'] !== null"
                            class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5">
                            <div v-for="(item, index) in searchData['chapters']" :key="item.id || index"
                                class="col h-100">
                                <div class="card rounded-4 d-flex flex-column h-100"
                                    :class="{ 'hovered': hoveredChapter === index }" @mouseover="hoveredChapter = index"
                                    @mouseleave="hoveredChapter = null">
                                    <div class="card-body">
                                        <h5 class="card-title">Chapter Name: {{ item.name }}</h5>
                                        <hr>
                                        <div class="card-text">
                                            <div>
                                                <span style="font-weight: bold;">Chapter description: </span>
                                                <span> {{ item.description }}</span>
                                            </div>
                                            <div>
                                                <span style="font-weight: bold;">Quiz Count: </span>
                                                <span> {{ item.quizzes.length }}</span>
                                            </div>
                                        </div>
                                        <br>
                                        <div class="card-footer d-flex align-content-end justify-content-end">
                                            <button class="btn btn-outline-dark"
                                                @click="router.push(`/subject/${item.subject_id}`)">View</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="chapters card mx-2 my-2 px-5 py-4 rounded-4" id="custom-cards"
                        style="box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);">
                        <h1>Quizzes</h1>
                        <hr>
                        <h4 v-if="searchData['quizzes'] === null">No quizzes found</h4>
                        <div v-if="searchData['quizzes'] !== null"
                            class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5">
                            <div v-for="(item, index) in searchData['quizzes']" :key="item.id || index"
                                class="col h-100">
                                <div class="card rounded-4 d-flex flex-column h-100"
                                    :class="{ 'hovered': hoveredQuiz === index }" @mouseover="hoveredQuiz = index"
                                    @mouseleave="hoveredQuiz = null">
                                    <div class="card-body">
                                        <h5 class="card-title">Quiz Name: {{ item.name }}</h5>
                                        <hr>
                                        <div class="card-text">
                                            <div>
                                                <span style="font-weight: bold;">Quiz description: </span>
                                                <span> {{ item.description }}</span>
                                            </div>
                                            <div>
                                                <span style="font-weight: bold;">Time Limit: </span>
                                                <span> {{ item.time_limit }} minutes</span>
                                            </div>
                                            <div>
                                                <span style="font-weight: bold;">Total Marks: </span>
                                                <span> {{ item.total_marks }}</span>
                                            </div>
                                            <div>
                                                <span style="font-weight: bold;">Start Date: </span>
                                                <span> {{ formatDateTime(item.start_date) }}</span>
                                            </div>
                                            <div>
                                                <span style="font-weight: bold;">Deadline: </span>
                                                <span> {{ formatDateTime(item.deadline) }}</span>
                                            </div>
                                        </div>
                                        <br>
                                        <div class="card-footer d-flex align-content-end justify-content-end">
                                            <button class="btn btn-outline-dark" v-if="userRole === 'user'"
                                                @click="router.push(`/${item.subject_id}/${item.chapter_id}/${item.id}/attempt`)">View</button>
                                            <button class="btn btn-outline-dark" v-if="userRole === 'admin'"
                                                @click="router.push(`/${item.subject_id}/${item.chapter_id}/${item.id}/view`)">View</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import fetchWithAuth from '@/utils/api';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import formatDateTime from '@/utils/formatDateTime';
import { useStore } from 'vuex';

const store = useStore();
const route = useRoute();
const router = useRouter();

const userRole = ref(store.state.user?.role)
const searchQuery = ref(route.query.query);
const searchData = ref({});
const searchMessage = ref("");
const hoveredSubject = ref(null);
const hoveredChapter = ref(null);
const hoveredQuiz = ref(null)
const searchFunc = async () => {
    if (searchQuery.value.length >= 3) {
        try {
            const response = await fetchWithAuth(`/api/search?query=${searchQuery.value}`, { method: "GET" })
            if (response.ok) {
                const data = await response.json();
                console.log(data)
                searchData.value["subjects"] = data["subjects"] !== null ? data["subjects"] : null;
                searchData.value["chapters"] = data["chapters"] !== null ? data["chapters"] : null;
                searchData.value["quizzes"] = data["quizzes"] !== null ? data["quizzes"] : null;
                if (data["subjects"] === data["chapters"] === data["quizzes"] === null) {
                    subjectMessage.value = "No search results found."
                }
            } else {
                const data = await response.json()
                searchMessage.value = data.message;
                console.log(data.message)
            }
        } catch (error) {
            console.error(error);
        }
    } else {
        searchMessage.value = "Query must have atleast 3 characters."
        console.log(searchQuery.value)
        console.log("Query must have atleast 3 characters.")
    }
}
onMounted(searchFunc)

// ============================================================================================================================================

// const searchQuery = ref("");
// const searchMessage = ref("")

const searchF = async () => {
    if (searchQuery.length < 3) {
        searchMessage = "Query must have atleast 3 characters"
    } else {
        router.push({ name: "SearchResults", query: { "query": searchQuery.value } })
        searchFunc()
    }
}

// ============================================================================================================================================


// Back link -------------------------------------------------------------------------------------
const goBack = () => {
    // router.go(-1);  // Goes back one step in history
    router.push({ name: "Dashboard" })
};
//------------------------------------------------------------------------------------------------

</script>

<style scoped>
.fixed-button {
    position: fixed;
    right: 40px;
    bottom: 40px;
    z-index: 1050;
    /* Above most content, below modals */
    border-radius: 40px;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
}

.box {
    padding: 50px;
    border-radius: 30px;
    background: rgba(0, 0, 0, 0.5);
    color: #faebd7;
    position: relative;
    z-index: 1;
}

.line-clamp {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    min-height: 3em;
    /* roughly 2 lines' height depending on font-size and line-height */
}

.icon {
    font-size: 16x;
    margin: 0 4px 6px 0;
}

.alternative-section {
    padding-left: 80px;
    padding-right: 20px;
    display: flex;
    flex-direction: column;
    height: 80vh;
}



.fade-line {
    height: 2px;
    width: 100%;
    /* Adjust width as needed */
    background: linear-gradient(to right, #000, transparent);
    opacity: 0.8;
    /* Optional: to make it soft */
}


.selected-image {
    border: 4px solid #007bff;
    box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
}

.hovered {
    background-color: antiquewhite;
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.6);
    cursor: pointer;
}

.hovered-cover {
    margin: 5px;
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.6);
}

.card,
.card-cover {
    transition: all 0.3s ease;
    /* <-- THIS adds smoothness */
}
</style>