import { createRouter, createWebHistory } from "vue-router";

import Home from "../pages/Home.vue";
import BrowseProviders from "../pages/BrowseProviders.vue";
import ProviderProfile from "../pages/ProviderProfile.vue";
import JobRequestForm from "../pages/JobRequestForm.vue";
import MessageWindow from "../pages/MessageWindow.vue";
import Login from "../pages/Login.vue";
import Register from "../pages/Register.vue";
import MyJobs from "../pages/MyJobs.vue";
import MyRequests from "../pages/MyRequests.vue";
import Profile from "../pages/Profile.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/providers",
    name: "BrowseProviders",
    component: BrowseProviders,
  },
  {
    path: "/providers/:id",
    name: "ProviderProfile",
    component: ProviderProfile,
    props: true,
  },
  {
    path: "/request/:providerId",
    name: "JobRequestForm",
    component: JobRequestForm,
    props: true,
  },
  {
    path: "/messages/:jobId",
    name: "MessageWindow",
    component: MessageWindow,
    props: true,
  },
  {
    path: "/my-jobs",
    name: "MyJobs",
    component: MyJobs,
  },
  {
    path: "/my-requests",              // <-- new route
    name: "MyRequests",
    component: MyRequests,
  },
  {
    path: "/profile",              // ← Add this route
    name: "Profile",
    component: Profile,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  // ...others if needed...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
