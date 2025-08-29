<template>
    <div class="container-fluid p-0">
        <Sidebar />
        <div class="hero-section d-flex">
            <div class="top-content">
                <div class="row">
                    <div class="col">
                        <button @click="goBack" class="btn btn-dark"
                            style="font-size: larger; margin: 0px 10px 10px 0px;"><i
                                class="bi bi-skip-backward-fill"></i> Back</button>
                    </div>
                    <div class="col d-flex align-content-end justify-content-end">
                        <div class="row mb-3 shadow" style="border-radius: 10px; padding: 5px; border: 2px grey solid;">
                            <label class="col-sm-4 col-form-label" style="font-weight: bold;" for="userSearch"><i
                                    class="bi bi-search"></i> Search User:</label>
                            <div class="col-sm-8 d-flex">
                                <input class="form-control form-control-sm" type="text" id="userSearch"
                                    v-model="userSearch" placeholder="Name/Email" required />
                                <button class="btn btn-primary" style="font-weight: bold;"
                                    @click="userSearchFunc">Search</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="fade-line "></div>
                <br>
                <div class="content-container">
                    <div v-if="userData && !userSearch" id="custom-cards">
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-3 g-4">
                            <div v-for="(user, index) in userData" :key="user.id || index" class="col">
                                <div class="card rounded-4 px-4 py-4 h-100 d-flex">
                                    <div class="d-flex align-items-center h-100">
                                        <div class="me-4">
                                            <img :src="avatars[user.id]" height="140" width="140"
                                                class="rounded-circle shadow"
                                                style="padding: 5px; background: white;" />
                                        </div>
                                        <div class="flex-grow-1">
                                            <h4 class="mb-1">Name: {{ user.name }}</h4>
                                            <p class="mb-1 text-muted">Email: {{ user.email }}</p>
                                            <p class="mb-1 text-muted">Role: {{ user.roles[0].name }}</p>
                                            <p class="mb-3 text-muted">Status: {{ user.active ? 'Active' : 'Inactive' }}
                                            </p>
                                            <button @click="toggleUserStatus(user.id)"
                                                v-if="user.roles[0].name !== 'admin'"
                                                class="btn btn-primary btn-sm fw-bold px-4">
                                                {{ user.active ? "Deactivate" : "Activate" }} User Account
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="userSearchData && userSearch" id="custom-cards">
                        <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-3 g-4">
                            <div v-for="(user, index) in userSearchData" :key="user.id || index" class="col">
                                <div class="card rounded-4 px-4 py-4 h-100 d-flex">
                                    <div class="d-flex align-items-center h-100">
                                        <div class="me-4">
                                            <img :src="avatars[user.id]" height="140" width="140"
                                                class="rounded-circle shadow"
                                                style="padding: 5px; background: white;" />
                                        </div>
                                        <div class="flex-grow-1">
                                            <h4 class="mb-1">Name: {{ user.name }}</h4>
                                            <p class="mb-1 text-muted">Email: {{ user.email }}</p>
                                            <p class="mb-1 text-muted">Role: {{ user.roles[0].name }}</p>
                                            <p class="mb-3 text-muted">Status: {{ user.active ? 'Active' : 'Inactive' }}
                                            </p>
                                            <button @click="toggleUserStatus(user.id)"
                                                v-if="user.roles[0].name !== 'admin'"
                                                class="btn btn-primary btn-sm fw-bold px-4">
                                                {{ user.active ? "Deactivate" : "Activate" }} User Account
                                            </button>
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
// ============================================================================================================================
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import fetchWithAuth from '@/utils/api';
import generateAvatarSvg from '@/utils/avatargenerator';
import Sidebar from '@/components/Sidebar.vue';
// ============================================================================================================================
const store = useStore();
const router = useRouter();

// ============================================================================================================================================
const goBack = () => {
    router.go(-1);  // Goes back one step in history
};
// ============================================================================================================================================



const userData = ref(null);
const avatars = ref({})
const userSearch = ref("")
const userSearchData = ref(null);

const fetchUserData = async () => {
    try {
        const response = await fetchWithAuth("/api/users", { method: "GET" })
        if (response.ok) {
            const data = await response.json();
            userData.value = data;
            console.log(userData.value)
            for (const user of data) {
                const svg = await generateAvatarSvg(user.avatar_seed, user.avatar_style);
                avatars.value[user.id] = `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`
            }
        } else {
            const data = await response.json();
            store.dispatch("alertMessage", `${data.message}`)
        }
    } catch (error) {
        console.error(error)
    }
}

const toggleUserStatus = async (user_id) => {
    try {
        const response = await fetchWithAuth('/api/user_activation', { method: "POST", body: JSON.stringify({ "id": `${user_id}` }) })
        if (response.ok) {
            const data = await response.json()
            store.dispatch('alertMessage', data.message)
            fetchUserData()
        } else {
            const data = await response.json()
            store.dispatch('alertMessage', data.message)
        }
    } catch (error) {
        console.error(error)
    }
}


const userSearchFunc = async () => {
    if (userSearch.value.length >= 3) {
        try {
            const response = await fetchWithAuth(`/api/users/search?query=${userSearch.value}`, { method: "GET" })
            if (response.ok) {
                const data = await response.json();
                userSearchData.value = data;

            } else {
                const data = await response.json()
                store.dispatch("alertMessage", data.message)
                userSearch.value = "";
            }
        } catch (error) {
            console.error(error)
        }
    } else {
        store.dispatch("alertMessage", "Search query must have atleast 3 characters")
    }
}


onMounted(fetchUserData)
</script>



<style scoped></style>