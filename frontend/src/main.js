import { createApp } from "vue";
import { marked } from "marked";
import hljs from "highlight.js";
import App from "./main.vue";
import naive from "naive-ui";
import store from "./store";
import router from "./route";
// 代码高亮
import "highlight.js/styles/atom-one-dark.css";

marked.setOptions({
    highlight(code) {
        return hljs.highlightAuto(code).value
    }
})

createApp(App).use(naive).use(store).use(router).mount("#app")
