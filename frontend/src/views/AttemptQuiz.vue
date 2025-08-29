<template>
    <div v-if="quizData" class="container-fluid p-0">
        <div class="hero-section">
            <div class="top-content">
                <div class="container-fluid">
                    <button v-if="quizStarted === false" @click="goBack" class="btn btn-dark" style="font-size: larger; margin: 0px 10px 10px 0px;"><i class="bi bi-skip-backward-fill"></i> Back</button>
                    <br v-if="quizStarted === false">
                    <div class="row gx-5 gy-5">
                        <div class="col-lg-4 col-sm-12">
                            <div style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h2 class="display-7 text-decoration-underline" style="margin-bottom: 15px;">{{ quizData.name }}</h2>
                                <h5>Description: {{ quizData.description }}</h5>
                                <h5>Total Marks: {{ quizData.total_marks }}</h5>
                                <h5>Time Limit: {{ quizData.time_limit }} minutes</h5>
                                <h5>Start Date: {{ startDate }}</h5>
                                <h5>Deadline: {{ deadlineDate }}</h5>
                                <button class="btn btn-success" v-if="quizStarted === true" @click="showSubmitQuizModal">Submit Quiz</button>
                                <button v-if="quizStarted === false && isQuizAvailable === true" class="btn btn-outline-primary" @click="quizStarted = !quizStarted, startTimer">Start Quiz</button>
                            </div>
                            <hr>
                            <div v-if="attempts && quizStarted === false" style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h2>Attempts:</h2>
                                <h5>Last Attempt At: {{ formatDateTime(attempts[0].submitted_at) }}</h5>
                                <h5>Score: {{ scorePercent(attempts[0].score,quizData.total_marks) }}%</h5>
                                <hr>
                                <router-link  v-if="attempts.length && store.state.user.name" class="btn btn-primary" :to="{ name: 'ViewUserAnswers', query: {'attempt_id':attempts[0].attempt_id, 'user_name':store.state.user.name} }">View Latest Attempt</router-link>
                                <button class="btn btn-outline-primary mx-3" v-if="attempts.length > 0" @click="router.push({ name: 'AllAttempts', query: { quiz_id: `${quizData.id}` } })">View All Attempts</button>
                            </div>
                            <div v-else-if="attemptMessage !== null" style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h3>No user attmpts for this quiz.</h3>
                            </div>
                        </div>
                        <div class="col-lg-8 col-sm-12" v-if="quizStarted === true && isQuizAvailable === true">
                            <div class="progress" style="height: 30px;">
                                <div 
                                    class="progress-bar progress-bar-striped progress-bar-animated"
                                    role="progressbar"
                                    :class="progressColor"
                                    :style="{ width: `${progressPercent}%` }"
                                    :aria-valuenow="progressPercent"
                                    aria-valuemin="0"
                                    aria-valuemax="100"
                                >
                                    {{ formattedTime }}
                                </div>
                            </div>
                            <div v-for="(question, index) in quizData.questions" :key="index" class="question" style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <p><strong>{{ index+1 }}: {{ question.question_statement }}</strong></p>
                                <!-- Single choice (Radio) -->
                                <div v-if="question.ans_type === 'mcq'">
                                    <div v-for="(option, opIndex) in question.options" :key="opIndex">
                                        <div class="input-group mb-3 w-100" style="max-width: 400px;">
                                            <div class="input-group-text">
                                                <input 
                                                    class="form-check-input mt-0" 
                                                    type="radio" 
                                                    :name="'q' + question.id.value + opIndex" 
                                                    :value="option" v-model="responses[question.id]"/>
                                            </div>
                                            <label class="input-group-text">{{ option }}</label>    
                                        </div>
                                        
                                        
                                    </div>
                                </div>
                                <!-- Multiple choice (Checkbox) -->
                                <div v-else-if="question.ans_type === 'msq'">
                                    <div v-for="(option, opIndex) in question.options" :key="opIndex">
                                        <div class="input-group mb-3 w-100" style="max-width: 400px;">
                                            <div class="input-group-text">
                                                <input 
                                                    class="form-check-input mt-0" 
                                                    type="checkbox" 
                                                    :value="option" 
                                                    @change="$event.target.checked 
                                                    ? (responses[question.id] = [...(responses[question.id] || []), option]) 
                                                    : (responses[question.id] = responses[question.id].filter(value => value !== option))"
                                                />
                                            </div>
                                            <label class="input-group-text d-flex aligbnb" style=" min-width: 200px; max-width: 400px;" :for="'q' + question.id.value + opIndex">{{ option }}</label>
                                            
                                        </div>
                                    </div>
                                </div>
                                <!-- Numeric (Text Input) -->
                                <div v-else-if="question.ans_type === 'num'">
                                    <input type="number" step="any" v-model.number="responses[question.id]" class="form-control" placeholder="Enter your answer"/>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-8 col-sm-12 text-center" v-else-if="isQuizAvailable === false">
                            <h2>This quiz has not started.</h2>
                            <h4>Quiz will be available on: {{ formatDateTime(quizData.start_date) }}</h4>
                        </div>
                    </div>
                    <div ref="submitQuiz" class="modal fade" tabindex="-1">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Submit Quiz</h5>
                                    <button v-if="remainingTime > 0" type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="mb-3 align-items-center">
                                        <h5 v-if="remainingTime === 0">Your time is up. Submitting quiz.</h5>
                                        <h5 v-if="remainingTime > 0">Are you sure, you want to submit the quiz?</h5>
                                    </div>
                                </div>                                
                                <div class="modal-footer">
                                    <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
                                    <button v-if="remainingTime > 0" @click="quizSubmission" class="btn btn-success">Submit</button>
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
// ===================================================================================================================================
import fetchWithAuth from "@/utils/api";
import { ref, computed, nextTick, onBeforeUnmount, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { Modal } from "bootstrap";
// ===================================================================================================================================
const route = useRoute();
const router = useRouter();
const store = useStore();
const time_limit = ref(null);
const user_id = computed (() => store.state.user.id); // Example user ID (should be dynamic)
const quizId = ref(route.params.quizId); // Example quiz ID (should be dynamic)
const subjectId = ref(route.params.subjectId)
const quizData = ref(null);
const responses = ref({}); // Store user responses
const quizStarted = ref(false) // Start quiz and timer
const remainingTime = ref(time_limit.value) // Remaining time for quiz
const timer = ref(null) // Quiz timer
const startDate = ref(null)
const isDeadline = ref(null)
const deadlineDate = ref(null)
// ===================================================================================================================================



// ===================================================================================================================================
function checkQuizAvailability(quiz) {
    if (!quiz || !quiz.start_date || !quiz.deadline) return false;

    const now = new Date();
    const start = new Date(quiz.start_date);
    const end = new Date(quiz.deadline);
    const formattedStart = start.toLocaleString('en-GB', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
        timeZoneName: undefined  // exclude time zone
    });
    const formattedDeadline = end.toLocaleString('en-GB', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
        timeZoneName: undefined  // exclude time zone
    });
    const nowUTC = now.getTime();
    const startUTC = start.getTime();
    const endUTC = end.getTime();

    return {
        isAvailable: now >= start && now <= end,
        start: formattedStart,
        deadline: formattedDeadline,
        isDeadline: now <= end,
    };
}
const isQuizAvailable = ref(false)
// ===================================================================================================================================



// ===================================================================================================================================
// Fetch Quiz Data 
const fetchQuizData = async () => {
    try{
        const response = await fetchWithAuth(`/api/quiz/${quizId.value}`, {method:"GET"})
        if (response.ok){
            const data = await response.json();
            quizData.value = data;
            time_limit.value = quizData.value.time_limit*60;
            const result = checkQuizAvailability(quizData.value);
            isQuizAvailable.value = result.isAvailable;
            startDate.value = result.start;
            deadlineDate.value = result.deadline;
            isDeadline.value = result.isDeadline;
        }
    } catch (error) {
        console.log(error)
    }   
}

// ===================================================================================================================================



// ===================================================================================================================================
// Get user attempts for quiz
const attempts = ref(null);
const attemptMessage = ref(null);
const userAttempts = async () => {
    try {
        const response = await fetchWithAuth(`/api/attempts/${quizId.value}`, {method:"GET"})
        if (response.ok){
            const data = await response.json();
            attempts.value = data.all_attempts;
        } else if (!response.ok) {
            const data = await response.json();
            attemptMessage.value = data.message;
        }
    } catch (error) {
        console.error(error)
    }
}
// ===================================================================================================================================



onMounted(() => {
    fetchQuizData();
    userAttempts();
})



// ===================================================================================================================================
// Watcher to track when user starts quiz.
watch(quizStarted, (newVal) => {
    if (newVal === true && time_limit.value) {
        remainingTime.value = time_limit.value
        startTimer()
    }
})
// Start timer when quiz begins.
function startTimer() {
    timer.value = setInterval(() => {
        if (remainingTime.value > 0) {
            remainingTime.value--
        } else {
            clearInterval(timer.value)
            timeElapsed()
        }
    }, 1000)
}
// Stop and clear timer when leaving page
onBeforeUnmount(() => {
    if (timer.value) clearInterval(timer.value)
})

// Progress percentage
const progressPercent = computed(() => {
  return Math.floor((remainingTime.value / time_limit.value) * 100)
})

// Format time (MM:SS)
const formattedTime = computed(() => {
    const minutes = Math.floor(remainingTime.value / 60).toString().padStart(2, '0')
    const seconds = (remainingTime.value % 60).toString().padStart(2, '0')
    return `${minutes}:${seconds}`
})

// Color class based on time left
const progressColor = computed(() => {
    const percent = progressPercent.value
    if (percent > 66) return 'bg-success'
    else if (percent > 33) return 'bg-warning text-dark'
    else return 'bg-danger'
})

function timeElapsed() {
    showSubmitQuizModal()
    setTimeout(quizSubmission, 3000)
}



// ===================================================================================================================================//----------------------------------------------------------------------------------------------------------------------



// ===================================================================================================================================
// Quiz submission modal
const submitQuiz = ref(null);
let submitQuizModal = null;

onMounted(async () => {
    await nextTick();

    if (submitQuiz.value) {
        submitQuizModal = new Modal(submitQuiz.value);
    }
})


const showSubmitQuizModal = () => {
    if (!submitQuizModal && submitQuiz.value) {
        submitQuizModal = new Modal(submitQuiz.value);
    }
    if (quizStarted.value === true) {
        submitQuizModal?.show();
    } else {
        store.dispatch("alertMessage", "You have not started the quiz.")
    }
};

// ===================================================================================================================================



// ===================================================================================================================================
// Submit the responses
const quizSubmission = async () => {
    try{
        const response = await fetchWithAuth(`/api/quiz/${ quizId.value }/response`, {
            method: "POST",
            body: JSON.stringify({"answers":responses.value})
        })
        if (response.ok) {
            const data = await response.json()
            submitQuizModal.hide()
            router.push(`/subject/${subjectId.value}`)
            store.dispatch("alertMessage", `${data.message}`)
        } else {    
            const data = await response.json()
            submitQuizModal.hide()
            store.dispatch("alertMessage", `${data.message}`)
        }
    } catch (error) {
        console.error(error)
    }
};
// ===================================================================================================================================

// Back link -------------------------------------------------------------------------------------
const goBack = () => {
    router.go(-1);  // Goes back one step in history
};
//------------------------------------------------------------------------------------------------


const formatDateTime = (isoString) => {
    const date = new Date(isoString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}, ${day}-${month}-${year}`;
};

const scorePercent = (score, fullScore) => {
    const scorePercentage = (score/fullScore)*100;
    return scorePercentage;
}
</script>


<style scoped>
.question{
    margin: 20px;
}
.q-satement, .q-options{
    margin-bottom: 20px;
}


.btn{
    font-weight: 600;
}
.question{
    margin: 20px;
}
.q-satement, .q-options{
    margin-bottom: 20px;
}
.progress-bar {
    transition: width 1s linear;
    font-weight: bold;
    font-size: 1.1rem;
}
</style>
