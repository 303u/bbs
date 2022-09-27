import { createStore } from 'vuex';
import { darkTheme, zhCN, enUS, ruRU, dateZhCN, dateRuRU, dateEnUS } from 'naive-ui';

(lang => document.lang = lang)(navigator.language.slice(0, 2));

const store = createStore({
    state: {
        user: {},
        history: [],
        user_info: {},
        theme: window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light",
    },
    getters: {
        theme(state) {
            return {
                "dark": darkTheme,
            }[state.theme]
        },
        locale() {
            return {
                "zh": zhCN,
                "ru": ruRU,
                "en": enUS,
            }[navigator.language.slice(0, 2)]
        },
        locale_d() {
            return {
                "zh": dateZhCN,
                "ru": dateRuRU,
                "en": dateEnUS,
            }[navigator.language.slice(0, 2)]
        },
    },
    mutations: {
        user(state, take) {
            state.user = take;
            state.user_info[take.id] = take;
        },
        clear_history(state) { state.history.length = 0; },
        theme(state) { state.theme = state.theme == "light" ? "dark" : "light" },
        clear_all(state) {
            state.user = {};
            state.user_info = {};
            state.history.length = 0;;
        },
        add_user_info(state, take) {
            state.user_info[take.id] = take;
        },
        add_history(state, take) {
            // 如果能查到本机历史则删除
            for (let num in state.history) {
                if (state.history[num].id == take.id) {
                    state.history.splice(num, 1);
                    break;
                }
            }
            // 插入历史
            state.history.unshift(take);
        },
    },
})

export default store;