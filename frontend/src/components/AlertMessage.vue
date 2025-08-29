<template>
    <transition name="fade">
        <div v-if="alertMessage" class="alert-box">
            {{ alertMessage }}
        </div>
    </transition>
</template>

<script>
import { computed, watch } from "vue";
import { useStore } from "vuex";

export default {
    
    setup() {
        const store = useStore();
        const alertMessage = computed(() => store.state.alertMessage);

        watch(alertMessage, (newMessage) => {
            if (newMessage) {
                setTimeout(() => {
                    store.commit("clearAlertMessage");
                }, 3000);
            }
        });  
    return { alertMessage };
    }
};
</script>

<style scoped>
.alert-box {
    margin-top: 100px;
    position: fixed;
    z-index: 1;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white;
    padding: 15px 20px;
    border-radius: 8px;
    font-size: 16px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    opacity: 1;
    transition: opacity 0.5s ease-in-out;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
    opacity: 0;
}
</style>
