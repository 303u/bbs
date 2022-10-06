<template>
  <n-space vertical>
    <!-- 搜索与刷新栏 -->
    <n-card>
      <template #header>
        <n-space vertical>
          <n-input-group>
            <n-input clearable v-model:value="input_words" @keyup.enter="on_search" />
            <n-button type="info" @keyup.enter="on_search">
              <template #icon>
                <n-icon>
                  <Search />
                </n-icon>
              </template>
              搜索
            </n-button>
          </n-input-group>
          <!-- 关键字展示 -->
          <TagListVue v-if="key_words" :data="key_words" />
        </n-space>
      </template>
    </n-card>

    <!-- 搜到内容 -->
    <n-list bordered>

      <n-list-item v-if="!list.length">
        <n-empty description="空空如也"></n-empty>
      </n-list-item>

      <!-- 页面内容 -->
      <n-list-item :key="li" v-for="li of list" @click="goto(li)">
        <n-thing>
          <!-- 头像 -->
          <template #avatar>
            <div @mouseover="hover = 1" @mouseout="hover = 0">
              <PopupCardVue :id="li.author" />
            </div>
          </template>
          <!-- 标题 -->
          <template #header>
            {{ li.title }}
          </template>
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
          <n-pagination :page-slot="5" v-model:page="page" :on-update:page="on_show" v-model:page-size="size"
            :item-count="data.length" />
        </n-space>
      </template>
    </n-list>

    <!-- 推荐内容 -->
    <IntroVue />
  </n-space>
</template>

<script>
import axios from "axios";
import { Link, Search, Reload } from "@vicons/ionicons5";
import PopupCardVue from "@/components/PopupCard.vue";
import TagListVue from "@/components/TagList.vue";
import IntroVue from "@/components/Intro.vue";
export default {
  data() {
    let keyword = this.$route.params.keyword || "";
    if (keyword) {
      axios.get("/i/t/" + keyword).then((req) => {
        // 载入数据
        this.data = req.data;
        // 当前页面数据
        this.list = this.data.slice(0, 5);
        // 是否已经取完数据
        this.lock = !req.data.length < 40;
      });
    }
    return {
      data: [],
      list: [],
      lock: 0,
      page: 1,
      size: 5,
      winds: true,
      hover: false,
      key_words: keyword,
      input_words: keyword,
    };
  },
  methods: {
    on_search() {
      if (this.input_words) {
        this.key_words = this.input_words.split(" ").join(",");
        axios.get("/i/t/" + this.input_words).then((req) => {
          this.page = 1;
          this.lock = !req.data.length < 40;
          this.data = req.data;
          this.list = this.data.slice(0, 5);
        });
      };
    },
    on_show(page) {
      // 翻页函数
      this.page = page;
      if (page == this.data.length / 5 && !this.lock) {
        let url = "/i/t/" + this.key_words;
        axios.get(url + "?skip=" + parseInt(page / 8)).then((req) => {
          this.data.push(...req.data);
          this.lock = !req.data.length < 40;
        });
      }
      this.list = this.data.slice((page - 1) * 5, page * 5);
    },
    goto(item) {
      if (!this.hover) this.$router.push("/item/" + item.id);
    },
  },
  components: {
    Link,
    Search,
    Reload,
    PopupCardVue,
    TagListVue,
    IntroVue,
  },
  // 捕捉路由参数变化
  watch: {
    $route() {
      let keyword = this.$route.params.keyword || "";
      if (keyword) {
        axios.get("/i/t/" + keyword).then((req) => {
          // 载入数据
          this.data = req.data;
          // 当前页面数据
          this.list = this.data.slice(0, 5);
          // 是否已经取完数据
          this.lock = !req.data.length < 40;
        });
      }
      this.key_words = keyword || "";
      this.input_words = keyword;
    }
  },
};
</script>

<style scoped>
#search {
  margin: 5vh 0;
}
</style>