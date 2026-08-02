import { createRouter, createWebHistory } from "vue-router";
import PinGate from "../views/PinGate.vue";
import Dashboard from "../views/Dashboard.vue"; 
import Login from "../views/Login.vue";
import Profile from "../views/Profile.vue";
import History from "../views/History.vue";



const routes = [
  { path: "/", name: "PinGate", component: PinGate },
  { path: "/login", name: "Login", component: Login },
  { path: "/dashboard", name: "Dashboard", component: Dashboard },
      { path: "/profile", name: "Profile", component: Profile },
      { path: "/history", name: "History", component: History },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
