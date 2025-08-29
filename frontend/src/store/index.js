import { createStore } from "vuex";
import { jwtDecode } from "jwt-decode";
import router from '../router/index.js';
import fetchWithAuth from '../utils/api.js';
import generateAvatarSvg from "@/utils/avatargenerator.js";

const store = createStore({
    state() {
        return {
            authToken: localStorage.getItem("authToken") || null,
            user: JSON.parse(localStorage.getItem("user")) || null,
            login_status: (JSON.parse(localStorage.getItem("user"))) ? true : false,
            alertMessage: null
        }
    },
    mutations: {
        setToken(state, authToken) {
            localStorage.setItem("authToken", authToken);
            state.authToken = authToken;
            const decodedToken = jwtDecode(authToken);
            localStorage.setItem("tokenExpiry", decodedToken.exp);
        },
        setUser(state, userData){
            state.login_status = true;
            state.user = userData;
            localStorage.setItem("user", JSON.stringify(userData));
        },
        setLogout(state) {
            localStorage.removeItem("authToken");
            localStorage.removeItem("user");
            state.authToken = null;
            state.user = null;
            state.avatar_svg = null;
            state.login_status = false;
        },
        setAlertMessage(state, message) {
            console.log("Alert Message:", message);
            state.alertMessage = message;
        },
        clearAlertMessage(state) {
            state.alertMessage = null;
        }
    },
    actions: {
        alertMessage({commit}, message){
            commit('setAlertMessage', message)
        },
        async login({ commit }, credentials) {
            try {
                const response = await fetch('/api/login', {
                    method: "POST",
                    headers: {"Content-Type" : "application/json"},
                    body: JSON.stringify(credentials)
                });
                if (response.ok) {
                    const data = await response.json();
                    commit('setToken', data.authToken);
                    commit('setUser', data.user);
                    commit('setAlertMessage', "Login successful!");
                    router.push('/dashboard')
                } else {
                    const errorData = await response.json();
                    commit('setAlertMessage', errorData.message);
                }
                return true;
            } catch (error) {
                commit('setAlertMessage', `An error occurred during login: ${error.message}`);
            }
        },
        async logout({ commit }) {
            try{
                const response = await fetchWithAuth('/api/logout', {
                    method: "POST"
                });
                if (response.ok) {
                    commit('setLogout');
                    commit('setAlertMessage', "Logout successful!");
                    router.push({ name: 'Home' });
                } else {
                    const errorData = await response.json();
                    commit('setAlertMessage', errorData.message);
                }
            } catch (error) {
                commit('setAlertMessage', `An error occurred during logout: ${error.message}`);
            }
        }
    },
    getters: {
        login_status: state => !!state.authToken, // Converts token to true/false,
    }
})


export default store;