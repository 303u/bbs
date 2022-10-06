import { marked } from "marked";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import "@/assets/markdown.css"
// 代码高亮
marked.setOptions({
    gfm: 1,
    breaks: 1,
    tables: 1,
    smartLists: 1,
    highlight(code) {
        return hljs.highlightAuto(code).value
    }
})