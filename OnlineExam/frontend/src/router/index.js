import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import TheExam from "../components/exam_components/TheExam.vue"

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },

  {
    path: "/:SessionId",
    name: "Exam",
    component: TheExam,
  },
 
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
