<template>
  <n-space vertical>
    <!-- 搜索与刷新栏 -->
    <n-card>
      <template #header>
        <n-space vertical>
          <n-input-group>
            <!-- 输入控件 -->
            <n-input clearable v-model:value="keywords" @keyup.enter="search" :placeholder="'空格间隔多个条件'" />
            <!-- 搜索按钮 -->
            <n-button type="info" @click="search">
              <template #icon>
                <n-icon>
                  <Search />
                </n-icon>
              </template>
              搜索
            </n-button>
          </n-input-group>
          <!-- 关键字展示 -->
          <TagListVue v-if="words" :data="words" />
        </n-space>
      </template>
    </n-card>

    <!-- 搜到内容 -->
    <DataListVue :url="url" :header="0" />

    <!-- 推荐内容 -->
    <IntroVue />
  </n-space>
</template>

<script>
import { Search } from "@vicons/ionicons5";
import PopupCardVue from "@/components/PopupCard.vue";
import TagListVue from "@/components/TagList.vue";
import IntroVue from "@/components/Intro.vue";
import DataListVue from "@/components/DataList.vue";
export default {
  data() {
    let keyword = this.$route.params.keyword || ""
    return {
      url: keyword ? "/items/k/" + keyword : "/items/",
      words: keyword.split(" ").join(","),
      keywords: keyword,
    };
  },
  methods: {
    search() {
      if (this.keywords) {
        this.words = this.keywords.split(" ").join(",");
        this.url = "/items/k/" + this.keyword
      } else {
        this.words = "";
        this.url = "/items/";
      };
    },
  },
  components: {
    Search,
    PopupCardVue, TagListVue, IntroVue, DataListVue
  },
  // 捕捉路由参数变化
  watch: {
    $route() {
      this.keywords = this.$route.params.keyword || ""
      this.search()
    }
  },
};
</script>