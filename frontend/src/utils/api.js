import store from '@/store/index.js';
import router from '@/router/index.js';

async function fetchWithAuth(endpoint, options = {}){
    try {
        let token = store.state.authToken;
        if (!token) {
            throw new Error("No authentication token found");
        }
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
        const newOptions = { ...options, headers: { ...defaultHeaders, ...options.headers } };

        let response = await fetch(`${endpoint}`, newOptions);

        if (response.status === 401) {
            store.dispatch('alertMessage', "Unauthorized access. Please log in again.");
            console.log("Token expired or invalid. Logging out.");
            store.commit('setLogout');
            router.push({ name: 'Login' });
        }
        return response
    }
    catch (error){
        console.error("Error in fetchWithAuth:", error);
        throw error; // Propagate error so the caller can handle it
    }
}

export default fetchWithAuth;