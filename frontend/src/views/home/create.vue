<template>
    <n-card v-show="suc == 0">
        <template #header> 创建文章 </template>
        <template #header-extra>
            <n-button circle @click="show_markdown = !show_markdown">
                <n-icon><LogoMarkdown /></n-icon>
            </n-button>
        </template>
        <!-- 内容表单 -->
        <n-form :model="data" :rules="rules" v-show="!show_markdown">
            <n-form-item-row label="标题" path="title">
                <n-input
                    clearable
                    show-count
                    maxlength="25"
                    v-model:value="data.title"
                />
            </n-form-item-row>
            <n-form-item-row label="标签" path="tag">
                <n-select v-model:value="data.tag" filterable multiple tag />
            </n-form-item-row>
            <n-form-item-row label="内容" path="body">
                <n-input
                    clearable
                    show-count
                    type="textarea"
                    maxlength="32000"
                    v-model:value="data.body"
                    :autosize="{
                        minRows: 10,
                    }"
                />
            </n-form-item-row>
            <n-button type="primary" @click="post" block>创建</n-button>
        </n-form>
        <!-- 效果预览 -->
        <n-card v-show="show_markdown">
            <div v-html="marked(data.body)"></div>
        </n-card>
        <n-back-top :right="50" />
    </n-card>

    <n-card v-show="suc != 0">
        <n-result status="success" title="已成功提交">
            <template #footer>
                <n-space justify="center">
                    <n-button-group>
                        <n-button secondary @click="again">再次创建</n-button>
                        <n-button secondary @click="this.$router.push('/')">
                            返回主页
                        </n-button>
                        <n-button secondary @click="this.$router.push('/user')">
                            查看投稿
                        </n-button>
                    </n-button-group>
                </n-space>
            </template>
        </n-result>

        <n-divider>
            <n-time :time="new Date().getTime()" />
        </n-divider>
    </n-card>
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import { LogoMarkdown } from "@vicons/ionicons5";

export default {
    data() {
        let data = { title: "", body: "", tag: [] };
        return {
            suc: 0,
            data,
            marked,
            show_markdown: false,
            rules: {
                title: {
                    required: true,
                    message: "标题字数1-32",
                    trigger: ["input", "blur"],
                    validator(_, val) {
                        return 0 < val.length <= 32;
                    },
                },
                tag: {
                    message: "字数总和太长",
                    trigger: ["input", "blur"],
                    validator() {
                        return JSON.stringify(data.tag).length <= 128;
                    },
                },
                body: {
                    message: "字数总和太长",
                    trigger: ["input", "blur"],
                    validator() {
                        return data.body.length <= 32000;
                    },
                },
            },
        };
    },
    methods: {
        post() {
            let tag = JSON.stringify(this.data.tag);
            if (
                0 < this.data.title.length <= 32 &&
                tag.length <= 128 &&
                this.data.body.length <= 32000
            ) {
                axios.post("/i/", { ...this.data, tag }).then(() => {
                    this.suc = 1;
                    this.data.title = this.data.body = "";
                    this.data.tag = [];
                });
            }
        },
        again() {
            this.suc = 0;
        },
    },
    // 注册组件
    components: { LogoMarkdown },
};
</script>