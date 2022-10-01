<template>
  <n-space vertical>
    <!-- banner 横幅 -->
    <BannerVue />

    <!-- 文章与部分评论 -->
    <n-grid cols="10" item-responsive responsive="self">
      <n-grid-item span="10 800:6 1200:7">
        <n-list bordered>
          <!-- 搜索与刷新栏 -->
          <template #header>
            <n-space vertical>
              <n-input-group>
                <n-button tertiary type="info" @click="get_data">
                  <template #icon>
                    <n-icon>
                      <Reload />
                    </n-icon>
                  </template>
                </n-button>
                <n-input clearable v-model:value="input_words" @keyup.enter="on_search" />
                <n-button tertiary type="primary" @click="on_search">
                  <template #icon>
                    <n-icon>
                      <Search />
                    </n-icon>
                  </template>
                </n-button>
              </n-input-group>
              <!-- 关键字展示 -->
              <n-space>
                <div :key="li" v-for="li of keywords.split(' ')">
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
                <div @mouseover="hover = 1" @mouseout="hover = 0">
                  <PopupCardVue :id="li.author" />
                </div>
              </template>
              <!-- 标题 -->
              <template #header>
                {{ li.title }}
              </template>
              <!-- 详情栏 -->
              <!-- <template #description></template> -->
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
      </n-grid-item>

      <!-- 站点公告 -->
      <n-grid-item id="tips" span="10 800:4 1200:3">
        <n-card>
          <template #cover>
            <WindmillVue :cls="winds" />
          </template>
          <template #header>站点公告</template>
          <!-- 风速按钮与弹窗 -->
          <template #header-extra>
            <n-popover trigger="hover">
              <template #trigger>
                <n-button circle @click="winds = !winds">
                  <template #icon>
                    <n-icon>
                      <BatteryCharging />
                    </n-icon>
                  </template>
                </n-button>
              </template>
              <span>调整动画风速</span>
            </n-popover>
          </template>
          <!-- 内容 -->
          <BannerVue />
        </n-card>
      </n-grid-item>
    </n-grid>
  </n-space>
</template>

<script>
import axios from "axios";
import { Link, Search, Reload, BatteryCharging } from "@vicons/ionicons5";
import PopupCardVue from "@/components/PopupCard.vue";
import WindmillVue from "@/components/Windmill.vue";
import BannerVue from "@/components/Banner.vue";

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
    return {
      data: [],
      list: [],
      lock: 0,
      page: 1,
      size: 5,
      winds: true,
      hover: false,
      keywords: "",
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
    on_search(keyword) {
      // 跳转查询页面
      this.$router.push({ name: "search", params: { keyword } })
    },
    on_show(page) {
      // 翻页组件切换页面触发函数
      this.page = page;
      // 判断是否到底
      if (page == this.data.length / 5 && !this.lock) {
        axios.get("/i/" + "?skip=" + parseInt(page / 8)).then((req) => {
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
    BatteryCharging,
    PopupCardVue,
    WindmillVue,
    BannerVue,
  },
};
</script>

<style scoped>
#tips {
  top: 7vh;
  position: sticky;
}

@media (min-width: 848px) {
  #tips {
    margin-left: 7px;
  }
}

@media (max-width: 848px) {
  #tips {
    margin-top: 7px;
  }
}
</style>