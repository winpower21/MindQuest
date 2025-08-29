<template>
    <div  class="container-fluid p-0" v-if="quizData">
        <Sidebar />
        <div class="hero-section">
            <div class="top-content">
                <div class="container-fluid">
                    <button @click="goBack" class="btn btn-dark" style="font-size: larger; margin: 0px 10px 10px 0px;"><i class="bi bi-skip-backward-fill"></i> Back</button>
                    <br>
                    <div class="row gx-5 gy-5">
                        <div class="col-lg-4 col-sm-12">
                            <div style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h2 class="display-7 text-decoration-underline" style="margin-bottom: 15px;">{{ quizData.name }}</h2>
                                <h5>Description: {{ quizData.description }}</h5>
                                <h5>Total Marks: {{ quizData.total_marks }}</h5>
                                <h5>Time Limit: {{ quizData.time_limit }} minutes</h5>
                                <h5>Start Date: {{ startDate }}</h5>
                                <h5>Deadline: {{ deadlineDate }}</h5>
                                <div class="d-flex align-items-end justify-content-end" v-if="quizData.attempts.length === 0">
                                    <router-link class="btn btn-outline-secondary" :to="`/${subjectId}/${chapterId}/${quizId}/edit`" >Edit Quiz</router-link>
                                </div>
                                <div v-else>
                                    <hr>
                                    <h6 style="color: red;">Cannot edit quiz. Already has attempts.</h6>
                                    <router-link class="btn btn-outline-secondary" :to="`/${subjectId}/${chapterId}/${quizId}/attempts`" >View All Attempts</router-link>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-8 col-sm-12">
                            <div v-for="(question, index) in quizData.questions" :key="index" class="question" style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h3>Question {{ index + 1 }}</h3>
                                <div>
                                    <p>{{ question.question_statement }}</p>
                                </div>
                                <hr>
                                <div class="row">
                                    <div class="col">
                                        <p style="margin-bottom: 0;">
                                            <span>Answer Type:</span>
                                            <span style="font-weight: bold; margin-left: 10px">{{ question.ans_type === 'mcq' ? 'Multiple Choice Question' : question.ans_type === 'msq' ? 'Multiple Select Question' : question.ans_type === 'num' ? 'Numeric Question' : 'Unknown Type' }}</span>
                                        </p>
                                    </div>
                                    <div class="col d-flex align-content-end justify-content-end">
                                        <p style="display: flex; gap: 10px;">
                                            <span>Marks:</span>
                                            <span style="font-weight: bold; margin-left: 10px">{{ question.marks }}</span>
                                        </p>
                                    </div>
                                </div>
                                <hr>
                                <div v-if="question.ans_type === 'mcq' || question.ans_type === 'msq'">
                                    <h5>Options:</h5>
                                    <ol type="a">
                                        <li v-for="(option, optIndex) in question.options" :key="optIndex" :class="{ 'correct-option': question.correct_options.includes(option) }" style="margin: 4px;">
                                            {{ option }}
                                        </li>
                                    </ol>
                                </div>
                                <div v-else-if="question.ans_type === 'num'">
                                    <h5>Numeric Range:</h5>
                                    <p>
                                    <span style="margin-right: 30px;">
                                        <span>Minimum:</span>
                                        <span style="margin-left: 10px; font-weight: bold;">{{ question.correct_min }}</span>
                                    </span>
                                    <span style="margin-right: 30px;">----|----</span>
                                    <span>
                                        <span>Maximum:</span>
                                        <span style="margin-left: 10px; font-weight: bold;">{{ question.correct_max }}</span>
                                    </span>
                                    </p>
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
// Imports ---------------------------------------------------------------------------------------
import fetchWithAuth from "@/utils/api";
import Sidebar from "@/components/Sidebar.vue";
import { ref, onMounted, nextTick, computed, watch} from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { Modal } from "bootstrap";
//------------------------------------------------------------------------------------------------

// Assignmetns -----------------------------------------------------------------------------------
const store = useStore();
const route = useRoute();
const router = useRouter();
const quizData = ref(null);
const totalMarks = ref(null);
const props = defineProps(['subjectId', 'chapterId', 'quizId'])
const chapterId = ref(props.chapterId)
const subjectId = ref(props.subjectId)
const quizId = ref(props.quizId)
const startDate = ref(null)
const deadlineDate = ref(null)
//------------------------------------------------------------------------------------------------


// ===================================================================================================================================
function dateFormatter(quiz) {
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
    

    return {
        start: formattedStart,
        deadline: formattedDeadline,
    };
}

// ===================================================================================================================================



// Fetch quiz data -------------------------------------------------------------------------------
const fetchQuizData = async () => {
    try{
        const response = await fetchWithAuth(`/api/quiz/${quizId.value}/view`, {method: "GET"})
        if (response.ok){
            quizData.value = await response.json();
            totalMarks.value = quizData.totalMarks
            const result = dateFormatter(quizData.value);
            startDate.value = result.start;
            deadlineDate.value = result.deadline;            
        } else {
            const errorMessage = await response.json()
            console.log(errorMessage)
        }
    }
    catch (error) {
        console.error(error)
    }
}
onMounted(fetchQuizData)
//------------------------------------------------------------------------------------------------


// Back link -------------------------------------------------------------------------------------
const goBack = () => {
    router.go(-1);  // Goes back one step in history
};
//------------------------------------------------------------------------------------------------



</script>


<style>
/* Add styling as needed */
.question{
    margin: 20px;
}
.q-satement, .q-options{
    margin-bottom: 20px;
}


.correct-option {
    font-weight: bold;
    color: #0f5132;
    background-color: #d1e7dd; /* Soft green highlight */
    padding: 4px 8px;
    border-radius: 4px;
}
.btn{
    font-weight: 600;
}
</style>
