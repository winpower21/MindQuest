import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store';

const routes = [
	{
		path: '/',
		name: 'Home',
		component:  () => import('../views/Home.vue')
	},
	{
		path: '/login',
		name: 'Login',
		component:  () => import('../views/Login.vue')
	},
	{
		path: '/register',
		name: 'Register',
		component:  () => import('../views/Register.vue')
	},
	{
		path: '/dashboard',
		name: 'Dashboard',
		component: () => import('../views/Dashboard.vue'),
		meta: {requiresAuth: true}
	},
	{
		path: '/subjects',
		name: 'Subjects',
		component: () => import('../views/Subjects.vue'),
		meta: { requiresAuth: true }
	},
	{
        path: '/subject/:subjectId',
        name: "SubjectPage",
        component: () => import('../views/SubjectPage.vue'),
        meta: { requiresAuth: true },
        props: true  // Allows passing 'id' as a prop to the component
    },
	{
		path: '/:subjectId/:chapterId/create_quiz',
		name: 'CreateQuiz',
		component: () => import('../views/CreateQuiz.vue'),
		meta: { requiresAuth: true, requiresRole: 'admin' },
		props: true // Allows passing 'subjectId' and 'chapterId' as props to the component
	},
	{
		path: '/:subjectId/:chapterId/:quizId/view',
		name: 'ViewQuiz',
		component: () => import('../views/ViewQuiz.vue'),
		meta: { requiresAuth: true, requiresRole: 'admin' },
		props:true
	},
	{
		path: '/:subjectId/:chapterId/:quizId/edit',
		name: 'EditQuiz',
		component: () => import('../views/EditQuiz.vue'),
		meta: { requiresAuth: true, requiresRole: 'admin' },
		props:true
	},
	{
		path: '/:subjectId/:chapterId/:quizId/attempt',
		name: 'AttemptQuiz',
		component: () => import('../views/AttemptQuiz.vue'),
		meta: { requiresAuth: true, requiresRole: 'user'},
		props:true
	},
	{
		path: '/user-profile',
		name: 'UserProfile',
		component: () => import('../views/UserProfile.vue'),
		meta: { requiresAuth: true},
		props:true
	},
	{
		path: '/users',
		name: 'UserManagement',
		component: () => import('../views/UserManagement.vue'),
		meta: { requiresAuth: true, requiresRole: "admin"},
		props:true
	},
	{
		path: '/user-answers',
		name: 'ViewUserAnswers',
		component: () => import('../views/ViewUserAnswers.vue'),
		meta: { requiresAuth: true },
		props:true
	},
	{
		path: '/search',
		name: 'SearchResults',
		component: () => import('../views/SearchResults.vue'),
		meta: { requiresAuth: true },
		props:true
	},
	{
		path: '/all-attempts',
		name: 'AllAttempts',
		component: () => import('../views/AllAttempts.vue'),
		meta: { requiresAuth: true},
		props:true
	},
	{
		path: '/statistics',
		name: 'AdminStats',
		component: () => import('../views/AdminStats.vue'),
		meta: { requiresAuth: true, requiresRole: "admin"},
		props:true
	}
]


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

//const store = useStore()

router.beforeEach((to, from, next) => {
	const isLoggedIn = store.getters.login_status;
	const tokenExpiry = store.state.tokenExpiry || localStorage.getItem('tokenExpiry');
	const userRole = store.state.user?.role
	console.log("User role from router",userRole)
	const now = Date.now() / 1000;

	if (to.meta.requiresAuth && !isLoggedIn){
		store.dispatch("alertMessage", "You must log in to access this page.");
        next('/login');
	} else if (to.meta.requiresAuth && isLoggedIn && tokenExpiry !== null) {
		if (now > tokenExpiry) {
			store.dispatch("alertMessage", "Your session has expired. Please log in again.");
			store.commit('setLogout');
			next('/login');
		}
	}
	return next();
});




// router.beforeEach((to, from, next) => {
//     const isLoggedIn = store.getters.login_status
	
//     if (to.meta.requiresAuth && !isLoggedIn) {
//         store.dispatch("alertMessage", "You must log in to access this page.");
//         next('/login');
//     } else if (store.state.tokenExpiry !== null) {
//         const now = Date.now() / 1000; // Convert to seconds
// 		if (now > localStorage.getItem("tokenExpiry")) {
// 			store.dispatch("alertMessage", "Your session has expired. Please log in again.");
// 			store.commit('setLogout');
// 			n)ext('/login');
// 		} 
//     } else {
// 		next(); // Proceed to the route
// 	}
// });


export default router
