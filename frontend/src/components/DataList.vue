<template>
  <n-space vertical>

    <!-- 搜到内容 -->
    <n-list bordered>
      <!-- 头部内容 -->
      <template #header v-if="header">
        <slot name="header"></slot>
      </template>

      <n-list-item v-if="!list.length">
        <n-empty description="空空如也"></n-empty>
      </n-list-item>

      <!-- 页面内容 -->
      <n-list-item :key="li" v-for="li of list" @click="goto(li)">
        <n-thing>
          <!-- 头像 -->
          <template #avatar v-if="avater">
            <div @mouseover="hover = 1" @mouseout="hover = 0">
              <PopupCardVue :id="li.author" />
            </div>
          </template>
          <!-- 标题 -->
          <template #header>
            {{ li.title }}
          </template>
          <!-- 详情栏 -->
          <template #description v-if="description">
            <slot name="description">
              <n-text depth="3">{{ $store.state.user_info[li.author]?.name }}</n-text>
            </slot>
          </template>
          <!-- 内容介绍 -->
          <template #footer v-if="footer">
            <n-ellipsis :line-clamp="2" :tooltip="false" class="item_body">
              {{ li.description }}
            </n-ellipsis>
          </template>
          <!-- 附加组件 -->
          <template #action v-if="action">
            <slot name="action">
              <n-space justify="space-between">
                <n-text>
                  <n-text>点击量</n-text>
                  <n-divider vertical />
                  <n-text>{{ li.hits }}</n-text>
                </n-text>
                <n-time :time="Number(li.time)" unix />
              </n-space>
            </slot>
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
  </n-space>
</template>

<script>
import axios from "axios";
import PopupCardVue from "@/components/PopupCard.vue";
export default {
  props: {
    avater: { default: true },
    description: { default: true },
    footer: { default: true },
    action: { default: true },
    header: { default: true },
    url: { type: String, default: "/items/" },
    author: { type: String, default: "" },
  },
  data() {
    this.$nextTick(this.get_data)
    return {
      data: [],
      list: [],
      lock: 0,
      page: 1,
      size: 5,
      hover: false,
    };
  },
  methods: {
    get_data() {
      // 刷新数据
      if (this.url) {
        axios.get(this.url + "?author=" + this.author).then((req) => {
          // 初始化页数
          this.page = 1;
          // 载入数据
          this.data = req.data;
          // 当前页面数据
          this.list = this.data.slice(0, 5);
          // 是否已经取完数据
          this.lock = !req.data.length < 40;
        });
      }
    },
    on_show(page) {
      // 翻页组件切换页面触发函数
      this.page = page;
      // 判断是否到底
      if (page == this.data.length / 5 && !this.lock) {
        // 请求参数
        let arg = ["?skip=" + parseInt(page / 8), "author=" + this.author].join("&");
        axios.get(this.url + arg).then((req) => {
          this.data.push(...req.data);
          this.lock = !req.data.length < 40;
        });
      }
      this.list = this.data.slice((page - 1) * 5, page * 5);
    },
    goto(item) {
      if (!this.hover) this.$router.push({ name: "item", params: { id: item.id } });
    },
  },
  // 监视变动
  watch: {
    url() {
      if (this.url) {
        axios.get(this.url).then((req) => {
          this.page = 1;
          this.lock = !req.data.length < 40;
          this.data = req.data;
          this.list = this.data.slice(0, 5);
        });
      }
    },
  },
  components: { PopupCardVue },
};
</script>

<style scoped>
.item_body {
  max-width: 85vw;
}

@media (min-width: 748px) {
  .item_body {
    max-width: 90vw;
  }
}
</style>