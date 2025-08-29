<template>
    <div class="container-fluid p-0">
        <Sidebar />
        <div class="hero-section d-flex">
            <div class="top-content">
                <h1 class="display-4 fw-bold">All Subjects</h1>
                <div class="fade-line"></div>
                <div v-if="items.length > 0" id="custom-cards">
                    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 py-5">
                        <div v-for="(item, index) in items" :key="item.id || index" class="col h-100">
                            <div class="card rounded-4 d-flex flex-column h-100" :class="{ 'hovered': hoveredCard === index }" @mouseover="hoveredCard = index" @mouseleave="hoveredCard = null">
                                <div class="card-cover h-100 overflow-hidden text-bg-dark rounded-4 shadow-lg" :class="{ 'hovered-cover' : hoveredCard === index }"
                                    :style="{
                                    backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(${item.image_url})`,
                                    backgroundSize: 'cover',
                                    backgroundRepeat: 'no-repeat',
                                    backgroundPosition: 'center',
                                    minHeight: '250px'}">
                                    <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                                        <h2 class="pt-5 mt-5 mb-4 lh-1 fw-bold line-clamp">{{ item.name }}</h2>
                                    </div>
                                </div>
                                <div class="card-body">
                                    <p class="card-text line-clamp" style="font-weight: 600; font-size: 18px;">{{ item.description }}</p>
                                    <div class="row g-2">
                                        <div class="col-4 d-flex">
                                            <i class="icon bi bi-journal-text"></i><p style="font-size: 16px;">Chapters: {{ item.chapters.length }}</p>
                                        </div>
                                        <div class="col-8 text-end">
                                            <router-link :to="`subject/${item.id}`" class="btn btn-sm btn-primary" style="margin: 2px;">Go to subject</router-link>
                                            <button @click="showDeleteSubjectModal(item)" v-if="userRole === 'admin'" class="btn btn-sm btn-danger" style="margin: 2px;">Delete Subject</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button @click="showNewSubjectModal" v-if="userRole === 'admin'" class="fixed-button btn btn-dark btn-lg" style="margin: 10px; border-radius: 40px; font-weight: 600;">Create Subject</button>
                </div>
                <div v-else class="alternative-section  text-center text-light d-flex align-items-center justify-content-center">
                    <div class="box">
                        <h3>No Subjects have been Created</h3>
                        <button @click="showNewSubjectModal" v-if="userRole === 'admin'" class="btn btn-dark btn-lg" style="margin: 10px; border-radius: 40px; font-weight: 600;">Create Subject</button>
                    </div>
                </div>
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
                                    <input v-model="subjectName" type="text" class="form-control" id="subjectName" placeholder="Subject Name">
                                </div>
                                <div class="mb-3">
                                    <label for="subjectDescription" class="form-label">Descirption</label>
                                    <input v-model="subjectDescription" type="text" class="form-control" id="subjectDescription" placeholder="Subject Description">
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
                                <button @click="createSubject" class="btn btn-primary">Submit</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div ref="deleteSubjectModal" class="modal fade" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Delete Subject</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3 align-items-center">
                                    <h5>Are you sure you want to delete the following subject:</h5>
                                    <h4 style="text-align: center;">{{ delSubjectName }}</h4>
                                </div>
                            </div>                                
                            <div class="modal-footer">
                                <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                <button @click="deleteSubjectFunc(delSubjectId)" class="btn btn-danger">Delete</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
defineOptions({ name: "Subjects" });

import { ref, onMounted, nextTick } from "vue";
import { Modal } from "bootstrap";
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import fetchWithAuth from '@/utils/api';

const unsplashAccessKey = import.meta.env.VITE_UNSPLASH_ACCESS_KEY;
const store = useStore();
const router = useRouter();
const items = ref([]);

const userRole = store.state.user?.role;
const hoveredCard = ref(null)

const subjectName = ref(null);
const subjectDescription = ref(null);
const coverImage = ref(null);
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



const fetchData = async () => {
    try{
        const response = await fetchWithAuth('/api/subject', {method: "GET"});
        if (response.ok) {
            const data = await response.json();
            items.value = data;
            console.log(items);
        } else {
            const errorData = await response.json();
            store.dispatch('alertMessage', errorData.message);
        }
    } catch (error) {
        console.error("Error fetching subjects:", error);
    }
}

const createSubject = async () => {
    try{
        const response = await fetchWithAuth('/api/subject',{
            method: "POST",
            body: JSON.stringify({
                "name" : subjectName.value,
                "description" : subjectDescription.value,
                "image_url": coverImage.value
            })
        })
        if (response.ok){
            const data = await response.json();
            store.dispatch("alertMessage", data.message)
            console.log(data.message);
            newSubject.hide();  //Close modal after successful submission
            await fetchData();
        } else {
            const data = await response.json();
            store.dispatch("alertMessage", data.message);
            console.log(data.message);
            newSubject.hide();  //Close modal after successful submission
            await fetchData();
        }
    } catch (error) {
        console.log(error)
        newSubject.hide();  //Close modal after successful submission
    }
}



// Delete Subject
const deleteSubjectFunc = async (subjectId) => {
    try {
        const response = await fetchWithAuth(`/api/subject/${subjectId}`, {
            method: "DELETE"
        });
        if (response.ok) {
            const data = await response.json();            
            console.log(data.message);
            deleteSubject.hide();  //Close modal after successful submission
            window.location.reload();  // Reload the page to reflect changes
            store.dispatch('alertMessage', data.message);            
        } else {
            const errorData = await response.json();
            store.dispatch('alertMessage', errorData.message);
            console.log(errorData.message);
        }
    } catch (error) {
        console.error("Error deleting subject:", error);
        store.dispatch('alertMessage', 'An error occurred while deleting the subject.');
    }
}




// Add subject modal-----------------------------------------------------------------------------
const newSubjectModal = ref(null);
const deleteSubjectModal = ref(null);

let newSubject = null;
let deleteSubject = null;

const delSubjectName = ref('');
const delSubjectId = ref('');

onMounted(async () => {
    await nextTick(); // Ensures the DOM is fully rendered before initializing modal
    if (newSubjectModal.value) {
        newSubject = new Modal(newSubjectModal.value);
    }
    if (deleteSubjectModal.value) {
        deleteSubject = new Modal(deleteSubjectModal.value);
    }
});

const showNewSubjectModal = () => {
    if (!newSubject && newSubjectModal.value) {
        newSubject = new Modal(newSubjectModal.value);
    }
    newSubject?.show();
};

const showDeleteSubjectModal = (subject) => {
    delSubjectName.value = subject.name;
    delSubjectId.value = subject.id;
    if (!deleteSubject && deleteSubjectModal.value) {
        deleteSubject = new Modal(deleteSubjectModal.value);
    }
    deleteSubject?.show();
};
//------------------------------------------------------------------------------------------------




onMounted(() => {
    fetchData();
});

</script>


<style scoped>
.fixed-button{
    position: fixed;
    right: 40px;
    bottom: 40px;
    z-index: 1050; /* Above most content, below modals */
    border-radius: 40px;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
}
.box{
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
    min-height: 3em; /* roughly 2 lines' height depending on font-size and line-height */
}
.icon{
    font-size: 16x;
    margin: 0 4px 6px 0;
}

.alternative-section{    
    padding-left: 80px;
    padding-right: 20px;    
    display: flex;
    flex-direction: column;
    height: 80vh;
}



.fade-line {
    height: 2px;
    width: 100%; /* Adjust width as needed */
    background: linear-gradient(to right, #000, transparent);
    opacity: 0.8; /* Optional: to make it soft */
}


.selected-image {
    border: 4px solid #007bff;
    box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
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