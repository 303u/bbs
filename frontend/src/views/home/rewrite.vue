<template>
  <n-card v-show="suc == 0">
    <template #header> 修改文章 </template>
    <template #header-extra>
      <n-button circle @click="show_markdown = !show_markdown">
        <n-icon>
          <LogoMarkdown />
        </n-icon>
      </n-button>
    </template>
    <!-- 内容表单 -->
    <n-form :model="data" :rules="rules">
      <n-form-item-row label="标题" path="title">
        <n-input clearable show-count maxlength="25" v-model:value="data.title" />
      </n-form-item-row>
      <n-form-item-row label="标签" path="tag">
        <n-select v-model:value="data.tag" filterable multiple tag />
      </n-form-item-row>
      <n-form-item-row label="内容" path="body" v-show="!show_markdown">
        <n-grid cols="2" item-responsive responsive="self">
          <!-- 输入组件 -->
          <n-grid-item span="2 700:1">
            <n-input clearable show-count type="textarea" maxlength="32000" v-model:value="data.body" :autosize="{
              minRows: 10,
            }" />
          </n-grid-item>
          <!-- 效果预览 -->
          <n-grid-item span="0 700:1">
            <n-card :bordered="false">
              <div v-html="marked(data.body)"></div>
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-form-item-row>
      <!-- 效果预览 -->
      <n-card v-show="show_markdown" :bordered="false">
        <div v-html="marked(data.body)"></div>
      </n-card>
      <n-button type="primary" @click="post" block>提交</n-button>
    </n-form>

    <n-back-top :right="50" />
  </n-card>

  <n-card v-show="suc != 0">
    <n-result status="success" title="已成功提交">
      <template #footer>
        <n-space justify="center">
          <n-button-group>
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
    axios.get("/i/" + this.$route.params.id).then((req) => {
      // 获取数据
      this.data = { ...req.data, tag: JSON.parse(req.data.tag || "[]") };
      // 判断是否为作者
      if (req.data.author != this.$store.state.user.id) {
        this.$router.push("/");
      }
    });
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
        axios
          .put("/i/" + this.$route.params.id, {
            ...this.data,
            tag,
          })
          .then(() => {
            this.suc = 1;
            this.data.title = this.data.body = "";
            this.data.tag = [];
          });
      }
    },
  },
  // 注册组件
  components: { LogoMarkdown },
};
</script>