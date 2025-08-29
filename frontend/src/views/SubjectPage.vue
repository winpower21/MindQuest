<template>
    <div v-if="subject" class="container-fluid p-0">
        <Sidebar />
        <div class="hero-section d-flex">
            <div class="top-content">
                <div class="container-fluid">
                    <button @click="goBack" class="btn btn-dark" style="font-size: larger; margin: 0px 10px 10px 0px;"><i class="bi bi-skip-backward-fill"></i> Back</button>
                    <br>
                    <div class="row gx-5 gy-5">
                        <div class="col-12 col-lg-4">
                            <!-- Subject Card -->
                            <div class="card rounded-4 d-flex">
                                <div class="card-cover  overflow-hidden text-bg-dark rounded-4 shadow-lg" :style="{ backgroundImage: `url(${subject.image_url})`, minHeight: '250px',
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
                                    <!-- <div class="row"> -->
                                        <div class=" d-flex">
                                            <i class="icon bi bi-journal-text"></i><p style="font-size: 16px;">Chapters: {{ subject.chapters.length }}</p>
                                        </div>
                                        <!-- <div class="col justify-content-end d-flex"> -->
                                            <button class="btn btn-primary" @click="exportCSV" :disabled="isGenerating" style="max-width: fit-content;">{{ isGenerating ? 'Generating...' : 'Download Subject Report' }}</button>
                                            <button class="btn btn-warning" @click="showModifySubjectModal(subject)" v-if="role === 'admin'" style="margin: 10px; color: white">Modify Subject</button>
                                            <button class="btn btn-success" @click="showAddChapterModal" v-if="role === 'admin'" style="margin: 10px;">Add Chapter</button>
                                        <!-- </div> -->
                                    <!-- </div> -->
                                </div>
                            </div>
                        </div>
                        <div class="col-12 col-lg-8">
                            <h3>Chapters</h3>
                            <div v-if="subject.chapters.length > 0"  class="card">
                                <ul class="list-group">
                                    <li class="list-group-item" v-for="(chapter, index) in subject.chapters" :key="index" >
                                        <div class="justify-content-between align-items-center">
                                            <h4 class="line-bottom">{{ index+1 }}: {{ chapter.name }}</h4>
                                            <div class="row">
                                                <div class="col">
                                                    <h6>{{ chapter.description }}</h6>
                                                </div>
                                                <div class="col d-flex justify-content-end">
                                                    <div class="list-buttons">
                                                        <button class="btn btn-sm btn-danger" v-if="role === 'admin'" style="margin: 10px;" @click="showDeleteChapterModal(chapter)">Delete Chapter</button>
                                                        <button class="btn btn-sm btn-warning" v-if="role === 'admin'" style="margin: 10px; color: white;" @click="showModifyChapterModal(chapter)">Modify Chapter</button>
                                                        <router-link class="btn btn-sm btn-success" style="margin: 10px;" v-if="role === 'admin'" :to="`/${subject.id}/${chapter.id}/create_quiz`">Add Quiz</router-link>
                                                        <button @click="toggle(index)" class="btn btn-sm btn-dark"> Quizzes {{ expandedIndex === index ? ' ▼ ' : ' ▶ ' }} </button>
                                                    </div>
                                                </div>
                                            </div>                                            
                                        </div>
                                        <ul v-show="expandedIndex === index" class="list-group list-group-flush mt-2">
                                            <li v-if="chapter.quizzes.length === 0" class="list-group-item">
                                                <span>No quizzes for this chapter.</span>
                                            </li>
                                            <li v-else v-for="(quiz, quizIndex) in chapter.quizzes" :key="quizIndex" class="list-group-item">
                                                <div class="row">
                                                    <div class="col-lg-7">
                                                        <span v-if="chapter.quizzes.length > 0">{{ quiz.name }}: {{ quiz.description }}</span>
                                                    </div>                                                    
                                                    <div class="col-lg-5 d-flex align-items-end justify-content-end">
                                                        <button v-if="role === 'admin'" class="btn btn-sm btn-outline-danger" @click="showDeleteQuizModal(quiz)">Delete Quiz</button>
                                                        <router-link v-if="role === 'admin'"  :to="`/${subject.id}/${chapter.id}/${quiz.id}/view`" class="btn btn-sm btn-outline-warning">View & Modify Quiz</router-link>
                                                        <router-link :to="`/all-attempts?quiz_id=${quiz.id}`" class="btn btn-sm btn-outline-info">View Attempts</router-link>
                                                        <router-link v-if="role !== 'admin'" :to="`/${subject.id}/${chapter.id}/${quiz.id}/attempt`" class="btn btn-sm btn-outline-success">Attempt Quiz</router-link>
                                                        <i v-if="chapter.quizzes.length > 0 && quiz.time_limit > 0" class="bi bi-stopwatch-fill" style="border: 1px solid orange; border-radius: 4px; padding: 3px;"> {{ quiz.time_limit }} min</i><i v-else class="bi bi-infinity"> </i>
                                                    </div>
                                                    <!-- <div class="col-lg-2 d-flex align-items-end justify-content-end">
                                                        <i v-if="chapter.quizzes.length > 0 && quiz.time_limit > 0" class="bi bi-stopwatch-fill" style="border: 1px solid orange; border-radius: 4px; padding: 5px;"> {{ quiz.time_limit }} min</i><i v-else class="bi bi-infinity"> </i>
                                                    </div> -->
                                                </div>
                                            </li>
                                        </ul>
                                                                    </li>
                                </ul>
                            </div>
                            <h5 v-else>No chapters for this subject</h5>
                            <!-- Bootstrap Modal for Adding Chapter -->
                            <div ref="addChapter" class="modal fade" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Add New Chapter</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3">
                                                <label for="name" class="form-label">Name</label>
                                                <input type="text" v-model="chapter_name" class="form-control" id="name" placeholder="Chapter name">
                                            </div>
                                            <div class="mb-3">
                                                <label for="description" class="form-label">Description</label>
                                                <input type="text" v-model="chapter_description" class="form-control" id="description" placeholder="Chapter description">
                                            </div>
                                        </div>                                
                                        <div class="modal-footer">
                                            <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                            <button type="submit" @click="createChapter" class="btn btn-outline-success">Submit</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Bootstrap Modal for Modifying Subject -->
                            <div ref="modifySubject" class="modal fade" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Modify Subject</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3">
                                                <label for="name" class="form-label">Name</label>
                                                <input type="text" v-model="subjectForm.name" class="form-control" id="name" >
                                            </div>
                                            <div class="mb-3">
                                                <label for="description" class="form-label">Description</label>
                                                <input type="text" v-model="subjectForm.description" class="form-control" id="description" >
                                            </div>
                                            <div class="mb-3">
                                                <label for="search" class="form-label">Search Cover Image</label>
                                                <div class="d-flex">
                                                    <input v-model="search" type="text" class="form-control" id="coverImage" placeholder="Cover Image URL">
                                                    <button class="btn btn-outline-primary" @click="searchImage">Search</button>
                                                </div>
                                            </div>
                                            <div class="row g-2" v-if="imagePrevUrlList.length > 0">
                                                <!-- Repeat this col 9 times -->
                                                <div v-for="(image_url, index) in imagePrevUrlList" :key="index" class="col-12 col-sm-6 col-md-4">
                                                    <img :src="image_url" class="img-fluid rounded album-img" :class="{ 'selected-image': subjectForm.image_url === imageUrlList[index] }" @click="subjectForm.image_url = imageUrlList[index]" style="cursor: pointer; max-height: 200px; max-width: 100%; ">
                                                </div>
                                            </div>
                                        </div>                                
                                        <div class="modal-footer">
                                            <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                            <button @click="updateSubject" class="btn btn-outline-success">Update</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Bootstrap Modal for Modifying Chapter -->
                            <div ref="modifyChapter" class="modal fade" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Modify Chapter</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3">
                                                <label for="name" class="form-label">Name</label>
                                                <input type="text" v-model="chapterForm.name" class="form-control" id="name" >
                                            </div>
                                            <div class="mb-3">
                                                <label for="description" class="form-label">Description</label>
                                                <input type="text" v-model="chapterForm.description" class="form-control" id="description" >
                                            </div>
                                        </div>                                
                                        <div class="modal-footer">
                                            <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                            <button @click="modifyChapterFunc" class="btn btn-outline-success">Update</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Bootstrap Modal for Deleting Chapter -->
                            <div ref="deleteChapter" class="modal fade" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Delete chapter</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3 align-items-center">
                                                <h5>Are you sure you want to delete the following chapter:</h5>
                                                <h4 style="text-align: center;">{{ chapterForm.name }}</h4>
                                            </div>
                                        </div>                                
                                        <div class="modal-footer">
                                            <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                            <button @click="deleteChapterFunc(chapterForm.id)" class="btn btn-danger">Delete</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Bootstrap Modal for Deleting Chapter -->
                            <div ref="deleteSubject" class="modal fade" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Delete Subject</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3 align-items-center">
                                                <h5>Are you sure you want to delete the following chapters:</h5>
                                                <h4 style="text-align: center;">{{ subjectForm.name }}</h4>
                                            </div>
                                        </div>                                
                                        <div class="modal-footer">
                                            <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                            <button @click="deleteChapterFunc(subjectForm.id)" class="btn btn-danger">Delete</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Bootstrap Modal for Deleting Quiz -->
                            <div ref="deleteQuiz" class="modal fade" tabindex="-1">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Delete Quiz</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="mb-3 align-items-center">
                                                <h5>Are you sure you want to delete the following quiz:</h5>
                                                <h4 style="text-align: center;">{{ quizForm.name }}</h4>
                                            </div>
                                        </div>                                
                                        <div class="modal-footer">
                                            <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                            <button @click="deleteQuizFunc(quizForm.id)" class="btn btn-danger">Delete</button>
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
// Imports---------------------------------------------------------------------------------------
import { useRoute, useRouter } from 'vue-router';
import { ref, onMounted, nextTick } from 'vue';
import { useStore } from 'vuex';
import fetchWithAuth from '@/utils/api';
import { computed } from 'vue';
import { Modal } from "bootstrap";
import Sidebar from '@/components/Sidebar.vue';

//-----------------------------------------------------------------------------------------------
defineOptions({ name: "SubjectPage" });

// Definitions ----------------------------------------------------------------------------------
const store = useStore();
const route = useRoute();
const router = useRouter();
const subjectId = computed(() => route.params.subjectId);
const subject = ref(null);
const message = ref(null);
const role = computed(() => store.state.user?.role);
const chapter_name = ref(null);
const chapter_description = ref(null);
const unsplashAccessKey = import.meta.env.VITE_UNSPLASH_ACCESS_KEY;
const search = ref(null);
const imageUrlList = ref([]);
const imagePrevUrlList = ref([]);
//-----------------------------------------------------------------------------------------------

// Search Images on Unsplash --------------------------------------------------------------------
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
//-----------------------------------------------------------------------------------------------

// Fetch Subject Data ---------------------------------------------------------------------------
const fetchSubjectData = async() => {
    try{
        const response = await fetchWithAuth(`/api/subject/${subjectId.value}`, {method: "GET"})
        if (!response.ok){
            const data = await response.json();
            message.value = data.message;
            console.log(message);
        }
        else{
            subject.value = await response.json();
        }
    } catch (error) {
        console.error("error", error)
    }
}
onMounted(fetchSubjectData);
// -----------------------------------------------------------------------------------------------


// Expand list -----------------------------------------------------------------------------------
const expandedIndex = ref(null);

const toggle = (index) => {
    expandedIndex.value = expandedIndex.value === index ? null : index;
};
//------------------------------------------------------------------------------------------------


// Back link -------------------------------------------------------------------------------------
const goBack = () => {
    router.go(-1);  // Goes back one step in history
};
//------------------------------------------------------------------------------------------------


// Modals ----------------------------------------------------------------------------------------
const subjectForm = ref({
    id: '',
    name: '',
    description: '',
    image_url: ''
});

const chapterForm = ref({
    id: '',
    name: '',
    description: ''
})

const quizForm = ref({
    id:'',
    name:''
})


const addChapter = ref(null);
const modifySubject = ref(null);
const modifyChapter = ref(null);
const deleteChapter = ref(null);
const deleteQuiz = ref(null);

let addChapterModal = null;
let modifySubjectModal = null;
let modifyChapterModal = null;
let deleteChapterModal = null;
let deleteQuizModal = null;

onMounted(async () => {
    await nextTick();

    if (addChapter.value) {
        addChapterModal = new Modal(addChapter.value);
    }
    if (modifySubject.value) {
        modifySubjectModal = new Modal(modifySubject.value);
    }

    if (modifyChapter.value) {
        modifyChapterModal = new Modal(modifyChapter.value)
    }

    if (deleteChapter.value) {
        deleteChapterModal = new Modal(deleteChapter.value)
    }

    if (deleteQuiz.value) {
        deleteQuizModal = new Modal(deleteQuiz.value)
    }
});


const showAddChapterModal = () => {
    if (!addChapterModal && addChapter.value) {
        addChapterModal = new Modal(addChapter.value);
    }
    addChapterModal?.show();
};

const showModifySubjectModal = (subject) => {
    subjectForm.value.id = subject.id
    subjectForm.value.name = subject.name;
    subjectForm.value.description = subject.description;
    subjectForm.value.image_url = subject.image_url; // or subject.coverImage
    if (!modifySubjectModal && modifySubject.value) {
        modifySubjectModal = new Modal(modifySubject.value);
    }
    modifySubjectModal?.show();
};

const showModifyChapterModal = (chapter)  => {
    chapterForm.value.id = chapter.id;
    chapterForm.value.name = chapter.name;
    chapterForm.value.description = chapter.description;
    if (!modifyChapterModal && modifyChapter.value) {
        modifyChapterModal = new Modal(modifyChapter.value);
    }
    modifyChapterModal?.show();
};

const showDeleteChapterModal = (chapter) => {
    chapterForm.value.id = chapter.id;
    chapterForm.value.name = chapter.name;
    if (!deleteChapterModal && deleteChapter.value) {
        deleteChapterModal = new Modal(deleteChapter.value);
    }
    deleteChapterModal?.show();
};
const showDeleteQuizModal = (quiz) => {
    quizForm.value.id = quiz.id;
    quizForm.value.name = quiz.name;
    if (!deleteQuizModal && deleteQuiz.value) {
        deleteQuizModal = new Modal(deleteQuiz.value);
    }
    deleteQuizModal?.show();
};

//------------------------------------------------------------------------------------------------

// Button Functions ------------------------------------------------------------------------------

// Modify Subject
const updateSubject = async () => {
    try{
        const response = await fetchWithAuth(`/api/subject/${subjectId.value}`, {
            method: "PUT",
            body: JSON.stringify(subjectForm.value)
        })
        if(response.ok){
            const data = await response.json();
            modifySubjectModal.hide();
            await fetchSubjectData();
            store.dispatch('alertMessage', `${data.message}`)
        } else {
            const errorData = await response.json();
            store.dispatch('alertMesssage', `${errorData.message}`)
            modifySubjectModal.hide();  //Close modal after successful submission
        }
    } catch (error) {
        console.error("Error updating subject:", error);
    }
}

// Create Chapter
const createChapter = async () => {
    const data = {
                name: chapter_name.value,
                description: chapter_description.value
            }
    try{
        const response = await fetchWithAuth(`/api/subject/${subjectId.value}/chapters`, {
            method: "POST",
            body: JSON.stringify(data)
        });
        if (response.ok){
            const data = await response.json();
            console.log(data.message);
            addChapterModal.hide();  //Close modal after successful submission
            await fetchSubjectData();
            chapter_name.value = null
            chapter_description.value = null
        } else {
            const errorMessage = await response.json();
            addChapterModal.hide();  //Close modal after successful submission
            store.dispatch('alertMessage', `Error creating subject: ${errorMessage.message}`)
            chapter_name.value = null
            chapter_description.value = null
        }
    } catch (error){
        console.log(error)
    }
}
//------------------------------------------------------------------------------------------------


const modifyChapterFunc = async () => {
    try{
        console.log("Sending data:", JSON.stringify(chapterForm.value));

        const response = await fetchWithAuth(`/api/chapter/${chapterForm.value.id}`, {
            method: "PUT",
            body: JSON.stringify(chapterForm.value)
        })
        if (response.ok) {
            const data = await response.json();
            modifyChapterModal.hide();  //Close modal after successful submission
            store.dispatch('alertMessage', `${data.message}`)
            await fetchSubjectData();
        } else {
            const errorMessage = await response.json();
            store.dispatch('alertMessage', `${errorMessage.message}`)
            modifyChapterModal.hide();  //Close modal after successful submission
            await fetchSubjectData();
        }
    } catch (error) {
        console.error(error)
    }
}

const deleteChapterFunc = async (chapterId) => {
    try{
        const response = await fetchWithAuth(`/api/chapter/${chapterId}`, {
            method: "DELETE"
        })
        if (response.ok){
            const data = await response.json();
            store.dispatch('alertMessage', `${data.message}`)
            deleteChapterModal.hide();
            await fetchSubjectData();
        } else {
            const errorMessage = await response.json();
            store.dispatch('alertMessage', `${errorMessage.message}`)
            deleteChapterModal.hide();
            await fetchSubjectData();
        }
    } catch (error) {
        console.error(error)
    }
}

const deleteQuizFunc = async (quizId) => {
    try{
        const response = await fetchWithAuth(`/api/quiz/${quizId}`, {
            method: "DELETE"
        })
        if (response.ok){
            const data = await response.json();
            store.dispatch('alertMessage', `${data.message}`)
            deleteQuizModal.hide();
            await fetchSubjectData();
        } else {
            const errorMessage = await response.json();
            store.dispatch('alertMessage', `${errorMessage.message}`)
            deleteQuizModal.hide();
            await fetchSubjectData();
        }
    } catch (error) {
        console.error(error)
    }
}


// =================================================================================================================================================
const isGenerating = ref(false)
let pollInterval = null

const exportCSV = async () => {
    isGenerating.value = true
    try {
    // Step 1: Trigger export task
        const res = await fetchWithAuth(`/api/export_attempt_csv/${subjectId.value}`)
        const data = await res.json()
        const taskId = data.id

    // Step 2: Start polling for file
        pollInterval = setInterval(async () => {
            try {
                const resultRes = await fetchWithAuth(`/api/csv_result/${taskId}`)
                if (resultRes.status === 200) {
                    const blob = await resultRes.blob()
                    const contentDisposition = resultRes.headers.get('Content-Disposition')
                    let filename = 'report.csv'

                    if (contentDisposition && contentDisposition.includes('filename=')) {
                        filename = contentDisposition.split('filename=')[1].replaceAll('"', '').trim()
                    }
                    downloadFile(blob, `${filename}.csv`)
                    clearInterval(pollInterval)
                    isGenerating.value = false
                }
            } catch (err) {
                console.error('Polling error:', err)
            }
        }, 3000)
    } catch (err) {
        console.error('Error triggering CSV export:', err)
        isGenerating.value = false
    }
}

const downloadFile = (blobData, filename) => {
    const url = window.URL.createObjectURL(blobData)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
}

// =================================================================================================================================================
</script>


<style scoped>
.icon {
    font-size: 20px;
    margin-right: 5px;
    margin-left: 5px;
}

small {
    font-size: 18px;
}
/* .chapter-btn {
    
} */
.btn {
    margin-left: 10px;
    margin-right: 10px;
}
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
}
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
.btn{
    font-weight: 600;
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