import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import { useMainStore } from "./store";  // <— make sure the path is correct

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

const mainStore = useMainStore();
mainStore.init();   // <— this pulls `user` (and `token`) from localStorage if present

app.mount("#app");
