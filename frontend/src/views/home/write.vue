<template>
  <n-card v-show="suc == 0">
    <template #header> 文章编辑 </template>
    <template #header-extra>
      <n-button circle @click="show_markdown = !show_markdown">
        <n-icon>
          <LogoMarkdown />
        </n-icon>
      </n-button>
    </template>
    <!-- 内容表单 -->
    <n-form :model="data" :rules="rules">
      <n-form-item-row label="标题">
        <n-input clearable show-count maxlength="64" v-model:value="data.title" />
      </n-form-item-row>
      <n-form-item-row label="标签" path="tag">
        <n-select v-model:value="data.tag" filterable multiple tag />
      </n-form-item-row>
      <n-form-item-row label="内容" v-show="!show_markdown">
        <n-grid cols="2" item-responsive responsive="self">
          <!-- 输入组件 -->
          <n-grid-item span="2 700:1">
            <n-input clearable show-count type="textarea" maxlength="6500" v-model:value="data.body" :autosize="{
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
            <n-button secondary @click="again">再次编写</n-button>
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
    if (this.$route.params.id) {
      axios.get("/i/" + this.$route.params.id).then((req) => {
        // 判断是否为作者
        if (req.data.author != this.$store.state.user.id) {
          this.$router.push("/");
        } else { data = { ...req.data, tag: req.data.tag.split(",") }; }
      }).catch(() => { this.$router.push("/") });
    }
    return {
      suc: 0,
      data,
      marked,
      show_markdown: false,
      rules: {
        tag: {
          message: "字数总和需要小于128",
          trigger: ["input", "blur"],
          validator() {
            return data.tag.join(",").length <= 128;
          },
        },
      },
    };
  },
  methods: {
    post() {
      // 将tag表合并
      let tag = this.data.tag.join(",");
      if (
        0 < this.data.title.length &&
        tag.length <= 128 &&
        0 < this.data.body.length
      ) {
        axios.post("/i/", { ...this.data, tag }).then(() => {
          // 显示成功
          this.suc = 1;
        });
      }
    },
    again() {
      // 再写一篇
      this.suc = 0;
      this.data.title = this.data.body = "";
      this.data.tag = [];
    },
  },
  components: { LogoMarkdown },
};
</script>