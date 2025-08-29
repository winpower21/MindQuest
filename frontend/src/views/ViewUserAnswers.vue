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
                            </div>
                            <hr>
                            <div style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h2 class="display-7 text-decoration-underline" style="margin-bottom: 15px;">{{ quizData.name }}</h2>
                                <h5>User Name: {{ user_name }}</h5>
                                <h5>User Marks: {{ attemptData.score }}</h5>
                                <h5>Submission Time: {{ formatDateTime(attemptData.submitted_at) }}</h5>
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
                                    <div class="row">
                                        <div class="col">
                                            <ol type="a">
                                                <p style="font-weight: bold;">Correct Options</p>
                                                <li v-for="(option, optIndex) in question.options" :key="optIndex" :class="{ 'correct-option': question.correct_options.includes(option) }" style="margin: 4px;">
                                                    {{ option }}
                                                </li>
                                            </ol>
                                        </div>
                                        <div class="col">
                                            <ol type="a">
                                                <p style="font-weight: bold;">User Selection</p>
                                                <li v-for="(option, optIndex) in question.options" :key="optIndex" :class="{ 'correct-ans': attemptData.responses[index].answer.includes(option) && question.correct_options.includes(option),  'wrong-ans': attemptData.responses[index].answer.includes(option) && !question.correct_options.includes(option)}" style="margin: 4px;">
                                                    {{ option }}
                                                </li>
                                            </ol>
                                        </div>
                                    </div>
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
                                    <hr>
                                    <span style="margin-right: 30px;">
                                        <span style="font-size: x-large; font-weight: bold;">User Answer: </span>
                                        <span :class="{ 'correct-ans': attemptData.responses[index].isCorrect === true, 'wrong-ans' : attemptData.responses[index].isCorrect !== true }">{{ attemptData.responses[index].answer }}</span>
                                    </span>
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

import { ref, onMounted, nextTick, computed, watch} from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import fetchWithAuth from "@/utils/api";
import Sidebar from "@/components/Sidebar.vue";
import formatDateTime from "@/utils/formatDateTime";
//------------------------------------------------------------------------------------------------

// Assignmetns -----------------------------------------------------------------------------------
const route = useRoute();
const router = useRouter();


const attempt_id = ref(route.query.attempt_id);
const user_name = ref(route.query.user_name);
const attemptData = ref(null)
const quizData = ref(null);
//------------------------------------------------------------------------------------------------


// Fetch quiz data -------------------------------------------------------------------------------
const fetchResponseData = async () => {
    try{
        const response = await fetchWithAuth(`/api/response/${attempt_id.value}`, {method: "GET"})
        if (response.ok){
            const data = await response.json();
            attemptData.value = data.attempt
            quizData.value = data.quiz
        } else {
            const errorMessage = await response.json()
            console.log(errorMessage)
        }
    }
    catch (error) {
        console.error(error)
    }
}
onMounted(fetchResponseData)
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
.correct-ans{
    font-weight: bold;
    color: #0f5132;
    background-color: #d1e7dd; /* Soft green highlight */
    padding: 4px 8px;
    border-radius: 4px;
}

.wrong-ans{
    font-weight: bold;
    color: red;
    background-color: rgb(255, 162, 162); /* Soft green highlight */
    padding: 4px 8px;
    border-radius: 4px;
}



.btn{
    font-weight: 600;
}
</style>
