<template>
    <n-layout style="height: 100vh">
        <n-card>
            <template #header>{{ ["登录", "注册", "找回"][page] }}</template>
            <template #header-extra>
                <n-space>
                    <n-button
                        :type="page == 0 ? 'success' : ''"
                        @click="change_page(0)"
                        text
                    >
                        登录
                    </n-button>
                    <n-button
                        :type="page == 1 ? 'success' : ''"
                        @click="change_page(1)"
                        text
                    >
                        注册
                    </n-button>
                    <n-button
                        :type="page == 2 ? 'success' : ''"
                        @click="change_page(2)"
                        text
                    >
                        找回
                    </n-button>
                </n-space>
            </template>

            <router-view v-slot="{ Component }">
                <keep-alive>
                    <component :is="Component" />
                </keep-alive>
            </router-view>

            <template #action>
                <n-space>
                    <n-button circle @click="this.$store.commit('theme')">
                        <template #icon>
                            <n-icon>
                                <Contrast />
                            </n-icon>
                        </template>
                    </n-button>
                    <n-button circle @click="github">
                        <template #icon>
                            <n-icon>
                                <Link />
                            </n-icon>
                        </template>
                    </n-button>
                </n-space>
            </template>
        </n-card>
    </n-layout>
</template>

<script>
import axios from "axios";
import { Contrast, Link } from "@vicons/ionicons5";
import { useMessage, useLoadingBar } from "naive-ui";

export default {
    data() {
        let msg = useMessage();
        let ldb = useLoadingBar();
        // 加载动效
        let request = axios.interceptors.request.use((req) => {
            ldb.start();
            return req;
        });
        let response = axios.interceptors.response.use(
            (req) => {
                ldb.finish();
                if (req.data.detail) msg.success(req.data.detail);
                else if (req.config.url == "/l/") msg.success("登录成功");
                return req;
            },
            (err) => {
                ldb.error();
                if (typeof err.response.data.detail == "string") {
                    msg.error(err.response.data.detail);
                }
            }
        );
        return {
            request,
            response,
            page: ["login", "regest", "retrieve"].indexOf(this.$route.name),
        };
    },
    methods: {
        change_page(page) {
            this.page = page;
            this.$router.push({ name: ["login", "regest", "retrieve"][page] });
        },
        github() {
            window.open("https:/github.com/303doc/bbs");
        },
    },
    components: {
        Contrast,
        Link,
    },
    beforeUnmount() {
        // 解除绑定的加载动效
        axios.interceptors.request.eject(this.request);
        axios.interceptors.response.eject(this.response);
    },
};
</script>

<style scoped>
.n-card {
    width: auto;
    margin: 1vh;
    height: 98vh;
    max-width: 360px;
}
/* .n-layout {
    z-index: 100;
}

@media (min-width: 400px) {
    .n-layout::before {
        z-index: -30;
        top: 0;
        left: 0;
        content: "";
        display: block;
        position: absolute;
        width: 100vw;
        height: 100vh;
        animation: pic 16s linear infinite;
    }
    @keyframes pic {
        0% {
            background: url("@/assets/p1.jpg");
            background-size: cover;
        }
        15% {
            background: url("@/assets/p1.jpg");
            background-size: cover;
        }
        25% {
            background: url("@/assets/p2.jpg");
            background-size: cover;
        }
        40% {
            background: url("@/assets/p2.jpg");
            background-size: cover;
        }
        50% {
            background: url("@/assets/p3.jpg");
            background-size: cover;
        }
        65% {
            background: url("@/assets/p3.jpg");
            background-size: cover;
        }
        75% {
            background: url("@/assets/p4.jpg");
            background-size: cover;
        }
        90% {
            background: url("@/assets/p4.jpg");
            background-size: cover;
        }
        100% {
            background: url("@/assets/p1.jpg");
            background-size: cover;
        }
    }
} */
</style>