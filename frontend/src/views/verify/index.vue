<template>
  <n-layout style="height: 100vh">
    <n-card>
      <template #header>{{ ["登录", "注册", "找回"][page] }}</template>
      <template #header-extra>
        <n-space>
          <n-button :type="page == 0 ? 'success' : ''" @click="change_page(0)" text>
            登录
          </n-button>
          <n-button :type="page == 1 ? 'success' : ''" @click="change_page(1)" text>
            注册
          </n-button>
          <n-button :type="page == 2 ? 'success' : ''" @click="change_page(2)" text>
            找回
          </n-button>
        </n-space>
      </template>

      <!-- 保持页面更换不清空输入 -->
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
</style>