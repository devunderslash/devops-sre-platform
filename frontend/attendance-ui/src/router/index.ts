import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";

import HomeView from "../views/HomeView.vue";
import NotFound from "../views/ErrorPage.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/players",
    name: "players",
    component: () =>
      import(/* webpackChunkName: "players" */ "../views/PlayersView.vue"),
  },
  {
    path: "/attendance",
    name: "attendance",
    component: () =>
      import(
        /* webpackChunkName: "attendance" */ "../views/AttendanceView.vue"
      ),
  },
  {
    path: "/:pathMatch(.*)*", // This wildcard route must be the last one
    name: "Page Not Found",
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
