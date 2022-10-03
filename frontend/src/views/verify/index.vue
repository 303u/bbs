<template>
  <n-layout style="height: 100vh">
    <n-card>
      <template #header>
        <n-text v-if="$route.name == 'login'">登录</n-text>
        <n-text v-if="$route.name == 'regest'">注册</n-text>
        <n-text v-if="$route.name == 'retrieve'">找回</n-text>
      </template>
      <template #header-extra>
        <n-space>
          <n-button @click="$router.push({name:'login'})" text>
            <n-text :type="$route.name == 'login' ? 'success' : ''">登录</n-text>
          </n-button>
          <n-button @click="$router.push({name:'regest'})" text>
            <n-text :type="$route.name == 'regest' ? 'success' : ''">注册</n-text>
          </n-button>
          <n-button @click="$router.push({name:'retrieve'})" text>
            <n-text :type="$route.name == 'retrieve' ? 'success' : ''">找回</n-text>
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
          <n-button circle @click="$store.commit('theme')">
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
    };
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