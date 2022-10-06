import { createApp } from "vue";
import main from "@/main.vue";
import store from "@/store";
import router from "@/route";
// 插件
import "@/plugins/markdown"
import component from "@/plugins/component";

createApp(main).use(component).use(store).use(router).mount("#app")
