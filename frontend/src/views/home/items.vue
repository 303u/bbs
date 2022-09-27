<template>
    <n-space vertical>
        <n-card>
            <template #header>{{ data.title }}</template>
            <template #header-extra>
                <n-time :time="Number(data.time || 0)" unix />
            </template>
            <TagList :data="data.tag" />
            <n-divider />
            <div v-html="marked(data.body || '')"></div>
        </n-card>

        <n-list bordered>
            <template #header>
                <n-space vertical>
                    <n-card v-if="c.reply">
                        <template #header>
                            <n-space>
                                <PopupCard :id="c.reply" />
                                <n-text type="info" depth="3" underline>
                                    @{{ info(c.reply).name }}
                                </n-text>
                            </n-space>
                        </template>
                        <template #header-extra>
                            <n-button @click="c.reply = null">取消</n-button>
                        </template>
                    </n-card>
                    <n-input
                        clearable
                        show-count
                        type="textarea"
                        maxlength="128"
                        placeholder="添加评论"
                        v-model:value="c.body"
                        :autosize="{ minRows: 1, maxRows: 3 }"
                    />
                    <n-button @click="add_comment" block>提交</n-button>
                </n-space>
            </template>

            <n-list-item :key="li" v-for="li of comment">
                <n-thing content-indented>
                    <template #avatar>
                        <PopupCard :id="li.author" />
                    </template>
                    <template #header>
                        <n-space>
                            <n-text>
                                {{ info(li.author).name }}
                            </n-text>
                            <n-tag v-if="data.author == li.author" type="error">
                                作者
                            </n-tag>
                            <n-tag v-else-if="li.author == user.id" type="info">
                                自己
                            </n-tag>
                        </n-space>
                    </template>
                    <template #header-extra v-if="li.reply">
                        <n-text type="info" depth="3" underline>
                            @{{ info(li.reply).name }}
                        </n-text>
                    </template>
                    <template #description>
                        <n-time :time="Number(li.time)" unix />
                    </template>
                    <n-text> {{ li.body }} </n-text>
                    <n-row>
                        <n-col :span="24"></n-col>
                    </n-row>
                    <template #footer>
                        <n-space>
                            <n-button @click="c.reply = li.author" tertiary>
                                回复
                            </n-button>
                            <n-button
                                @click="dele(li)"
                                tertiary
                                v-if="li.author == user.id"
                            >
                                删除
                            </n-button>
                        </n-space>
                    </template>
                </n-thing>
            </n-list-item>
        </n-list>
    </n-space>

    <n-back-top :right="50" />
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import { PersonCircle } from "@vicons/ionicons5";
import PopupCard from "@/components/PopupCard.vue";
import TagList from "@/components/TagList.vue";

export default {
    data() {
        axios.get("/i/" + this.$route.params.id).then((req) => {
            this.data = req.data;
            // 历史浏览
            this.$store.commit("add_history", req.data);
        });
        axios.get("/t/" + this.$route.params.id).then((req) => {
            // 获取评论
            this.comment = req.data;
        });
        return {
            user: this.$store.state.user,
            c: { body: null, reply: null },
            marked,
            data: {},
            comment: [],
        };
    },
    methods: {
        add_comment() {
            if (/^[.\s\S]{1,128}$/.test(this.c.body)) {
                axios
                    .post("/t/", { ...this.c, item: this.data.id })
                    .then(() => {
                        this.comment_flash();
                        this.c.body = this.c.reply = "";
                    });
            }
        },
        comment_flash() {
            axios.get("/t/" + this.data.id).then((req) => {
                this.comment = req.data;
            });
        },
        dele(talk) {
            if (talk.author == this.user.id) {
                axios.delete("/t/" + talk.id).then(() => {
                    this.comment_flash();
                });
            }
        },
        info(id) {
            return this.$store.state.user_info[id] || {};
        },
    },
    components: { PersonCircle, PopupCard, TagList },
};
</script>