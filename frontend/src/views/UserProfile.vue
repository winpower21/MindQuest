<template>
	<div class="container-fluid p-0">
		<Sidebar />
		<div class="hero-section">
			<div class="top-content d-flex justify-content-center align-items-center">
				<div class="card shadow p-4" style="width: 100%; min-width: 400px; border-radius: 16px;">
					<div class="text-center">
						<img :src="`data:image/svg+xml;utf8,${avatar_svg}`" alt="Avatar" class="rounded-circle mb-3"
							style="width: 200px; height: 200px; border: 3px solid #f5f5f5;" />
						<h4 class="mb-1">{{ user.name }}</h4>
						<p class="text-muted mb-4">{{ user.email }}</p>
						<div class="d-grid gap-2">
							<button class="btn btn-outline-primary" @click="showResetPasswordModal">
								<i class="bi bi-shield-lock"></i> Reset Password
							</button>
							<button v-if="user.role !== 'admin'" class="btn btn-outline-danger"
								@click="showDeleteAccountModal">
								<i class="bi bi-trash"></i> Delete Account
							</button>
						</div>
					</div>
				</div>
				<!-- Bootstrap Modal for Resetting Password -->
				<div ref="modifyPassword" class="modal fade" tabindex="-1">
					<div class="modal-dialog">
						<div class="modal-content">
							<div class="modal-header">
								<h5 class="modal-title">Reset Password</h5>
								<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
							</div>
							<div class="modal-body">
								<div class="mb-3" v-if="!isOldPasswordCorrect">
									<label for="oldpassword" class="form-label">Enter Existing Password:</label>
									<input type="password" v-model="oldPassword" class="form-control" id="oldpassword">
								</div>
								<div>
									<p v-if="message && !isOldPasswordCorrect">{{ message }}</p>
								</div>
								<div class="mb-3" v-if="isOldPasswordCorrect">
									<label for="newpassword" class="form-label">Enter New Password:</label>
									<input type="password" v-model="newPassword" class="form-control" id="newpassword">
								</div>
								<div class="mb-3" v-if="isOldPasswordCorrect">
									<label for="confirmpassword" class="form-label">Confirm New Password:</label>
									<input type="text" v-model="confirmPassword" class="form-control" id="confirmpassword"
										:class="{ 'wrongPassowrd': newPassword !== confirmPassword, 'correctPassword': newPassword === confirmPassword }">
								</div>
							</div>
							<div class="modal-footer">
								<!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
								<button v-if="!isOldPasswordCorrect" @click="checkPassword"
									class="btn btn-success">Next</button>
								<button v-if="isOldPasswordCorrect" @click="resetPassword"
									class="btn btn-success">Change Password</button>
								<button @click="modifyPasswordModal.hide()" class="btn btn-warning">Cancel</button>
							</div>
						</div>
					</div>
				</div>
				<!-- Bootstrap Modal for Deleting Account -->
				<div ref="delAccount" class="modal fade" tabindex="-1">
					<div class="modal-dialog">
						<div class="modal-content">
							<div class="modal-header">
								<h5 class="modal-title">Delete Account</h5>
								<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
							</div>
							<div class="modal-body">
								<div class="mb-3 align-items-center">
									<h5 v-if="!isOldPasswordCorrect">Are you sure you want to delete your account?</h5>
									<h5 v-if="isOldPasswordCorrect">Confirm account deletion?</h5>
									<p v-if="isOldPasswordCorrect"> Once you click Confirm, all user data and records
										will be lost.</p>
								</div>

								<div class="mb-3" v-if="!isOldPasswordCorrect">
									<label for="password" class="form-label">Enter your password and click Yes to
										continue:</label>
									<input type="password" v-model="oldPassword" class="form-control" id="password">
								</div>
								<div>
									<p v-if="message && !isOldPasswordCorrect">{{ message }}</p>
								</div>
							</div>
							<div class="modal-footer">
								<!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
								<button v-if="!isOldPasswordCorrect" @click="checkPassword"
									class="btn btn-danger">Yes</button>
								<button v-if="isOldPasswordCorrect" @click="deleteAccount"
									class="btn btn-danger">Confirm</button>
								<button @click="delAccountModal.hide()" class="btn btn-success">Cancel</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import generateAvatarSvg from '@/utils/avatargenerator';
import { useStore } from 'vuex';
import Sidebar from '@/components/Sidebar.vue';
import fetchWithAuth from '@/utils/api';
import { Modal } from 'bootstrap';
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useStore();
const user = store.state.user;
const avatar_svg = ref('');

const getAvatar = async () => {
	console.log(user.avatar_seed, user.avatar_style)
	const svg = await generateAvatarSvg(user.avatar_seed, user.avatar_style);
	avatar_svg.value = encodeURIComponent(svg);
};

onMounted(getAvatar);

// ============================================================================================================================================================
const newPassword = ref("");
const confirmPassword = ref("")
const oldPassword = ref("")
const isOldPasswordCorrect = ref(false)
const message = ref(null)


const modifyPassword = ref(null);
const delAccount = ref(null);
let modifyPasswordModal = null
let delAccountModal = null


onMounted(async () => {
	await nextTick();
	if (modifyPassword.value) {
		modifyPasswordModal = new Modal(modifyPassword.value);
	}
	if (delAccount.value) {
		delAccountModal = new Modal(delAccount.value);
	}
})

const showResetPasswordModal = () => {
	newPassword.value = ""
	confirmPassword.value = ""
	oldPassword.value = ""
	if (!modifyPasswordModal && modifyPassword.value) {
		modifyPasswordModal = new Modal(modifyPassword.value);
	}
	modifyPasswordModal?.show();
};

const showDeleteAccountModal = () => {
	oldPassword.value = ""
	if (!delAccountModal && delAccount.value) {
		delAccountModal = new Modal(delAccount.value);
	}
	delAccountModal?.show();
};


const checkPassword = async () => {
	try {
		const response = await fetchWithAuth("/api/check-password", { method: "POST", body: JSON.stringify({ 'password': `${oldPassword.value}` }) })
		if (response.ok) {
			const data = await response.json();
			console.log(data.message)
			isOldPasswordCorrect.value = true
			oldPassword.value = ""
		} else {
			const data = await response.json();
			message.value = data.message
		}
	} catch (error) {
		modifyPasswordModal.hide()
		console.error(error)
	}
}

const resetPassword = async () => {
	// Logic to send reset email or open modal
	try {
		const response = await fetchWithAuth("/api/reset-password", { method: "POST", body: JSON.stringify({ 'password': `${newPassword.value}` }) })
		if (response.ok) {
			const data = await response.json()
			modifyPasswordModal.hide()
			store.dispatch("alertMessage", `${data.message}. Logging user out.`)
			setTimeout(() => {
				store.dispatch("logout");
			}, 3000);
		} else {
			const data = await response.json()
			console.log(data.message)
			store.dispatch("alertMessage", `${data.message}`)
			isOldPasswordCorrect.value = false;
		}
	} catch (error) {
		modifyPasswordModal.hide()
		console.error(error)
	}

};



// ============================================================================================================================================================

const deleteAccount = async () => {
	if (confirm('Are you sure you want to delete your account? This cannot be undone.')) {
		try {
			const response = await fetchWithAuth('/api/delete_account', { method: "POST" })
			if (response.ok) {
				localStorage.clear();
				router.push("/");
				window.location.reload()
			} else {
				const data = await response.json()
				delAccountModal.hide()
				store.dispatch('alertMessage', `${data.message}`)
			}
		} catch (error) {
			console.error(error)
		}

	}
};
// ============================================================================================================================================================
</script>

<style scoped>
.hero-section {
	padding-top: 80px;
	padding-left: 80px;
	padding-right: 20px;
	min-height: 100vh;
	display: flex;
	justify-content: center;
	align-items: center;
	padding: 20px;
}

.fade-line {
	height: 2px;
	width: 100%;
	/* Adjust width as needed */
	background: linear-gradient(to right, #000, transparent);
	opacity: 0.8;
	/* Optional: to make it soft */
}

.content-container {
	padding: 30px;
	display: flex;
	flex-direction: column;
}

.card {
	background-color: #fffdfb;
	transition: box-shadow 0.3s ease;
}

.card:hover {
	box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

button {
	font-weight: 500;
}

.wrongPassowrd {
	color: red;
	border: 2px solid red;
}

.correctPassword {
	color: green;
	border: 2px solid green;
}
</style>
