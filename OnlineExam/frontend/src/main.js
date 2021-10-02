import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import BaseCard from "./components/UI/BaseCard.vue";
import BaseDialog from "./components/UI/BaseDialog.vue";
import BaseButton from "./components/UI/BaseButton.vue";

const app = createApp(App);
app.component("base-card", BaseCard);
app.component('base-button', BaseButton);
app.component('base-dialog', BaseDialog); 

app.use(router).mount("#app");
