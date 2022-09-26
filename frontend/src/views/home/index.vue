<template>
    <n-space vertical id="background">
        <!-- banner 横幅 -->
        <n-carousel draggable autoplay style="height: 13em">
            <n-card style="height: 13em" :key="li" v-for="li of banner">
                <template #header>{{ li.title }}</template>
                <template #header-extra>
                    <n-button circle @click="open(li.url)">
                        <template #icon>
                            <n-icon><Link /></n-icon>
                        </template>
                    </n-button>
                </template>
                <n-skeleton text width="70%" v-if="li.body == ''" />
                <n-skeleton text :repeat="3" v-if="li.body == ''" />
                <n-ellipsis v-else :line-clamp="4" :tooltip="false">
                    {{ li.body }}
                </n-ellipsis>
            </n-card>
        </n-carousel>

        <n-list bordered>
            <!-- 搜索与刷新栏 -->
            <template #header>
                <n-space vertical>
                    <n-input-group>
                        <n-button tertiary type="info" @click="get_data">
                            <template #icon>
                                <n-icon><Reload /></n-icon>
                            </template>
                        </n-button>
                        <n-input
                            clearable
                            v-model:value="input_words"
                            @keyup.enter="select"
                        />
                        <n-button tertiary type="primary" @click="select">
                            <template #icon>
                                <n-icon><Search /></n-icon>
                            </template>
                        </n-button>
                    </n-input-group>
                    <!-- 关键字展示 -->
                    <n-space>
                        <div :key="li" v-for="li of key_words.split(' ')">
                            <n-tag round v-if="li" size="large">
                                {{ li }}
                            </n-tag>
                        </div>
                    </n-space>
                </n-space>
            </template>

            <!-- 页面内容 -->
            <n-list-item :key="li" v-for="li of list" @click="goto(li)">
                <n-thing>
                    <!-- 头像 -->
                    <template #avatar>
                        <popup-card :id="li.author" />
                    </template>
                    <!-- 标题 -->
                    <template #header>
                        {{ li.title }}
                    </template>
                    <!-- <template #description> {{ li.author }} </template> -->
                    <!-- 内容 -->
                    <template #footer>
                        <n-ellipsis :line-clamp="2" :tooltip="false">
                            {{ li.body }}
                        </n-ellipsis>
                    </template>
                    <template #action>
                        <n-time :time="Number(li.time)" unix />
                    </template>
                </n-thing>
            </n-list-item>

            <!-- 翻页控件 -->
            <template #footer>
                <n-space justify="center">
                    <n-pagination
                        :page-slot="5"
                        v-model:page="page"
                        :on-update:page="on_show"
                        v-model:page-size="size"
                        :item-count="data.length"
                    />
                </n-space>
            </template>
        </n-list>
    </n-space>
</template>

<script>
import axios from "axios";
import { Link, Search, Reload } from "@vicons/ionicons5";
import PopupCard from "@/components/PopupCard.vue";

export default {
    name: "home",
    data() {
        axios.get("/i/").then((req) => {
            // 载入数据
            this.data = req.data;
            // 当前页面数据
            this.list = this.data.slice(0, 5);
            // 是否已经取完数据
            this.lock = !req.data.length < 40;
        });
        // axios.get("/banner").then((req) => {
        //     this.banner = req.data;
        // });
        return {
            banner: [
                { title: "声明", body: "", url: "" },
                { title: "公告", body: "", url: "" },
            ],
            data: [],
            list: [],
            lock: 0,
            page: 1,
            size: 5,
            key_words: "",
            input_words: "",
        };
    },
    methods: {
        get_data() {
            // 刷新数据
            axios.get("/i/").then((req) => {
                this.page = 1;
                this.lock = !req.data.length < 40;
                this.data = req.data;
                this.list = this.data.slice(0, 5);
            });
            this.key_words = this.input_words = "";
        },
        select() {
            if (this.input_words) {
                this.key_words = this.input_words;
                axios.get("/i/t/" + this.key_words).then((req) => {
                    this.page = 1;
                    this.lock = !req.data.length < 40;
                    this.data = req.data;
                    this.list = this.data.slice(0, 5);
                });
            } else this.get_data();
        },
        on_show(page) {
            // 翻页函数
            this.page = page;
            if (page == this.data.length / 5 && !this.lock) {
                let url = "/i/";
                // 根据是否存在关键字刷新数据
                if (this.key_words) url += "t/" + this.key_words;
                axios.get(url + "?s=" + parseInt(page / 8)).then((req) => {
                    this.data.push(...req.data);
                    this.lock = !req.data.length < 40;
                });
            }
            this.list = this.data.slice((page - 1) * 5, page * 5);
        },
        goto(item) {
            this.$router.push("/item/" + item.id);
        },
        open(url) {
            window.open(url);
        },
    },
    components: { Link, Search, Reload, PopupCard },
};
</script>

<style scoped>
/* #background {
    z-index: 15;
}
#background::after {
    top: 0;
    z-index: -1;
    content: "";
    display: block;
    position: absolute;
    transform: rotate(45deg);
    width: 100vw;
    height: 100vw;
    background: #59f5;
}
#background::before {
    top: 0;
    z-index: -1;
    content: "";
    display: block;
    position: absolute;
    transform: rotate(10deg);
    width: 100vw;
    height: 100vw;
    background: #59f3;
} */
</style>