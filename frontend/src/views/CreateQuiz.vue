<template>
    <div class="container-fluid p-0">
        <Sidebar />
        <div class="hero-section">
            <div class="top-content">
                <div class="container-fluid">
                    <button @click="goBack" class="btn btn-dark"
                        style="font-size: larger; margin: 0px 10px 10px 0px;"><i class="bi bi-skip-backward-fill"></i>
                        Back</button>
                    <br>
                    <div class="row gx-5 gy-5">
                        <div class="col-lg-4 col-sm-12">
                            <div
                                style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h2 class="display-7" style="margin-bottom: 15px;">Create New Quiz</h2>
                                <div class="fade-line"></div>
                                <div class="form-floating mb-3">
                                    <input class="form-control" type="text" id="quizName" v-model="quiz_name"
                                        placeholder="name" required />
                                    <label class="form-label" for="quizName">Quiz Name:</label>
                                </div>
                                <div class="form-floating mb-3">
                                    <input class="form-control" type="text" id="description" v-model="quiz_description"
                                        placeholder="description" required />
                                    <label class="form-label" for="description">Quiz Description:</label>
                                </div>
                                <div class="form-floating mb-3">
                                    <input class="form-control" type="number" id="tlimit" v-model="time_limit" min="1"
                                        placeholder="1" required />
                                    <label class="form-label" for="tlimit">Time Limit (In minutes):</label>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label" for="startDate">Quiz Start Date</label>
                                    <input class="form-control datetime-input" type="date" id="startDate"
                                        v-model="start_date" />
                                    <div id="startHelp" class="form-text">If not provided will be set to today.</div>
                                </div>
                                <h6 class="form-text">Note: Default deadline is 7 days from start date.</h6>
                                <div class="row">
                                    <div class="col-6">
                                        <h4>Total Marks: {{ totalMarks }}</h4>
                                    </div>
                                    <div class="col-6 d-flex justify-content-end">
                                        <h4>Questions Count: {{ question_count }}</h4>
                                    </div>
                                </div>
                                <hr>
                                <button class="btn btn-success" @click="submitQuiz()">Submit Quiz</button>
                            </div>
                        </div>
                        <div class="col-lg-8 col-sm-12">
                            <div v-for="(question, index) in questions" :key="index" class="question"
                                style="border: 2px solid; border-color: lightgrey; border-radius: 10px; padding: 20px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);">
                                <h3>Question {{ index + 1 }}</h3>
                                <div class="form-floating mb-3 q-satement">
                                    <textarea class="form-control" v-model="question.question_statement"
                                        placeholder="Question Statement" required></textarea>
                                    <label class="form-label">Question Statement:</label>
                                </div>
                                <div class="row align-items-center q-options">
                                    <div class="col-auto">
                                        <label for="questionType" class="form-label">Question Type</label>
                                        <select class="form-select" id="questionType" v-model="question.ans_type"
                                            @change="updateQuestionType(question, question.ans_type)" required>
                                            <option value="mcq">MCQ (Single Correct)</option>
                                            <option value="msq">MSQ (Multiple Correct)</option>
                                            <option value="num">NUM (Numeric Range)</option>
                                        </select>
                                    </div>
                                    <div class="col-auto">
                                        <label for="questonMarks" class="form-label">Marks</label>


                                        <input class="form-control" id="questionMarks" type="number"
                                            v-model.number="question.marks" placeholder="Marks" min="0" required
                                            @input="validateMarks(question)" />
                                        <!-- <input class="form-control" id="questionMarks" type="number"
                                            v-model="question.marks" placeholder="Marks" required /> -->
                                    </div>
                                </div>
                                <div v-if="question.ans_type === 'mcq' || question.ans_type === 'msq'">
                                    <div class="row">
                                        <div class="col">
                                            <h4>Options:</h4>
                                        </div>
                                        <div class="col d-flex align-items-end justify-content-end">
                                            <button class="btn btn-secondary" @click="addOption(question)">Add
                                                Option</button>
                                        </div>
                                    </div>
                                    <br>
                                    <div v-for="(option, optIndex) in question.options" :key="optIndex">
                                        <!-- Radio for MCQ -->
                                        <div v-if="question.ans_type === 'mcq'">
                                            <div class="input-group mb-3">
                                                <div class="input-group-text">
                                                    <input class="form-check-input mt-0" type="radio"
                                                        :name="'mcq-' + index" :value="option"
                                                        @change="updateCorrectOptions(question, option)"
                                                        :checked="question.correct_options.includes(option)" />
                                                </div>
                                                <input type="text" class="form-control"
                                                    v-model="question.options[optIndex]" placeholder="Enter option text"
                                                    required />
                                                <button class="btn"
                                                    @click="removeOption(question, optIndex)">Remove</button>
                                            </div>
                                        </div>
                                        <div v-if="question.ans_type === 'msq'">
                                            <div class="input-group mb-3">
                                                <div class="input-group-text">
                                                    <input class="form-check-input mt-0" type="checkbox" :value="option"
                                                        @change="updateCorrectOptions(question, option)"
                                                        :checked="question.correct_options.includes(option)" />
                                                </div>
                                                <input type="text" class="form-control"
                                                    v-model="question.options[optIndex]" placeholder="Enter option text"
                                                    required />
                                                <button class="btn"
                                                    @click="removeOption(question, optIndex)">Remove</button>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                                <div v-else-if="question.ans_type === 'num'">
                                    <h4>Numeric Range:</h4>
                                    <div class="input-group mb-3">
                                        <input type="number" class="form-control" v-model="question.correct_min"
                                            placeholder="Minimum Value" required />
                                        <span class="input-group-text">to</span>
                                        <input type="number" class="form-control" v-model="question.correct_max"
                                            placeholder="Maximum Value" required />
                                    </div>
                                </div>
                                <button class="btn btn-outline-danger" style="margin-top: 5px;"
                                    @click="removeQuestion(index)">Remove question</button>
                            </div>
                            <button class="btn btn-outline-primary" @click="question_count++">Add question</button>
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
import { reactive, ref, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";


//------------------------------------------------------------------------------------------------

// Assignmetns -----------------------------------------------------------------------------------
const store = useStore();
const route = useRoute();
const router = useRouter();
const question_count = ref(0);
const questions = reactive([]);
const quiz_name = ref(null);
const quiz_description = ref(null);
const time_limit = ref(null);
const start_date = ref(null);
const deadline = ref(null);
const totalMarks = computed(() => {
    return questions.reduce((sum, question) => sum + (Number(question.marks) || 0), 0);
});
const chapterId = ref(route.params.chapterId)
const subjectId = ref(route.params.subjectId)

let quiz_data;
//------------------------------------------------------------------------------------------------

// Back link -------------------------------------------------------------------------------------
const goBack = () => {
    router.go(-1);  // Goes back one step in history
};
//------------------------------------------------------------------------------------------------


const validateMarks = (question) => {
    if (question.marks === null || question.marks === '') {
        question.marks = 0;
    } else if (question.marks < 0) {
        question.marks = 0;
    }
};



// Add and remove Questions ----------------------------------------------------------------------
watch(question_count, (newCount, oldCount) => {
    if (newCount > oldCount) {
        for (let i = oldCount; i < newCount; i++) {
            questions.push({
                question_statement: "",
                ans_type: "",
                options: [],
                correct_options: [],
                correct_min: null,
                correct_max: null,
                marks: null,
            })
        }
    }
})
//------------------------------------------------------------------------------------------------

// Add and remove options ------------------------------------------------------------------------
const removeQuestion = (index) => {
    questions.splice(index, 1);
    question_count.value = question_count.value - 1
}
const addOption = (question) => {
    question.options.push("");
}
const removeOption = (question, index) => {
    const removedOption = question.options[index];

    // remove option
    question.options.splice(index, 1);
    // also remove from correct_options if it exists
    question.correct_options = question.correct_options.filter(opt => opt !== removedOption);
}
//------------------------------------------------------------------------------------------------



// Update Correct Options -------------------------------------------------------------------------
const updateCorrectOptions = (question, option) => {
    if (question.ans_type === "mcq") {
        question.correct_options = [option]; // Only one correct answer for MCQ
    } else if (question.ans_type === "msq") {
        if (question.correct_options.includes(option)) {
            // If already selected, remove it
            question.correct_options = question.correct_options.filter(opt => opt !== option);
        } else {
            // Otherwise, add it
            question.correct_options.push(option);
        }
    }
};


const updateQuestionType = (question, type) => {
    question.ans_type = type;
    question.options.splice(0, question.options.length); // Reset options when changing type
    question.correct_options.splice(0, question.correct_options.length); // Reset correct options when changing type
    question.correct_min = null; // Reset numeric range
    question.correct_max = null; // Reset numeric range
};

//------------------------------------------------------------------------------------------------


// Submit Quiz -----------------------------------------------------------------------------------
const submitQuiz = async () => {
    if (!quiz_name.value || !quiz_description.value || !time_limit.value || question_count.value <= 0) {
        store.dispatch("alertMessage", "Please fill all the fields correctly.");
        return;
    }

    // Validate each question
    for (let i = 0; i < questions.length; i++) {
        const q = questions[i];
        if (!q.question_statement || !q.ans_type || q.marks === null) {
            store.dispatch("alertMessage", `Please fill all fields for Question ${i + 1}`);
            return;
        }

        if ((q.ans_type === "mcq" || q.ans_type === "msq")) {
            if (q.options.length < 2) {
                store.dispatch("alertMessage", `Question ${i + 1} should have at least 2 options.`);
                return;
            }
            if (q.correct_options.length === 0) {
                store.dispatch("alertMessage", `Please select at least one correct option for Question ${i + 1}`);
                return;
            }
        }

        if (q.ans_type === "num") {
            if (q.correct_min === null || q.correct_max === null || q.correct_min === "" || q.correct_max === "") {
                store.dispatch("alertMessage", `Please provide a valid numeric range for Question ${i + 1}`);
                return;
            }
        }
    }

    // Prepare quiz data
    quiz_data = {
        name: quiz_name.value,
        description: quiz_description.value,
        time_limit: time_limit.value,
        total_marks: totalMarks.value,
        start_date: start_date.value ? `${start_date.value}T00:00:00` : null,
        deadline: deadline.value ? `${deadline.value}T00:00:00` : null,
        questions: questions.map(q => ({
            question_statement: q.question_statement,
            ans_type: q.ans_type,
            options: q.options,
            correct_options: q.correct_options,
            correct_min: q.correct_min,
            correct_max: q.correct_max,
            marks: q.marks
        })),
    };


    try {
        const response = await fetchWithAuth(`/api/chapter/${chapterId.value}/quiz`, {
            method: "POST",
            body: JSON.stringify(quiz_data),
        });
        if (response.ok) {
            const data = await response.json();
            router.push(`/subject/${subjectId.value}`); // Redirect to the created quiz page
            store.dispatch("alertMessage", `${data.message}`);
        } else {
            const errorMessage = await response.json();
            store.dispatch("alertMessage", `${errorMessage.message}`);
        }
    } catch (error) {
        console.error("Error creating quiz:", error);
        alert("An error occurred while creating the quiz. Please try again.");
    }
}
//------------------------------------------------------------------------------------------------

</script>


<style>
/* Add styling as needed */
.question {
    margin: 20px;
}

.q-satement,
.q-options {
    margin-bottom: 20px;
}


.btn {
    font-weight: 600;
}

.datetime-input {
    padding: 10px 15px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 12px;
    background-color: #f9f9f9;
    color: #333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease-in-out;
    width: 100%;
    max-width: 300px;
}

.datetime-input:focus {
    border-color: #4f46e5;
    /* soft blue/purple */
    outline: none;
    background-color: #fff;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}
</style>
