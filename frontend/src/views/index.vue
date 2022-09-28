<template>
  <n-drawer v-model:show="active" :width="270" :placement="'left'">
    <n-drawer-content>
      <n-menu
        :options="menuBar"
        :default-value="$route.name"
        @update:value="menuValue"
      />

      <template #header>
        <n-space @click="menuValue('user')">
          <n-avatar>
            <n-icon><PersonCircle /></n-icon>
          </n-avatar>
          <n-ellipsis style="max-width: 160px; margin: 7px" :tooltip="false">
            {{ $store.state.user.name }}
          </n-ellipsis>
        </n-space>
      </template>

      <template #footer>
        <n-button block @click="signout">登出</n-button>
      </template>
    </n-drawer-content>
  </n-drawer>

  <n-layout style="height: 100vh" :native-scrollbar="false">
    <n-layout style="top: 0; z-index: 1000; position: sticky">
      <n-layout-header bordered style="padding: 5px">
        <n-space justify="space-between">
          <n-button circle @click="active = true">
            <template #icon>
              <n-icon>
                <ListSharp />
              </n-icon>
            </template>
          </n-button>

          <n-button circle @click="this.$store.commit('theme')">
            <template #icon>
              <n-icon>
                <Contrast />
              </n-icon>
            </template>
          </n-button>
        </n-space>
      </n-layout-header>
    </n-layout>

    <div style="padding: 24px">
      <!-- 保存状态 在调试情况下会导致热重载报错 -->
      <!-- <router-view v-slot="{ Component }">
        <keep-alive include="index">
          <component :is="Component" :key="$route.name" />
        </keep-alive>
      </router-view> -->
      <router-view></router-view>
    </div>
  </n-layout>
</template>

<script>
import axios from "axios";
import { useMessage, useLoadingBar } from "naive-ui";
import { PersonCircle, ListSharp, Contrast } from "@vicons/ionicons5";

// 菜单栏
const menuBar = [
  { label: "首页", key: "home" },
  { label: "创建", key: "create" },
  { label: "关于", key: "about" },
  {
    label: "用户",
    key: "",
    children: [
      { label: "主页", key: "user" },
      { label: "历史", key: "history" },
      { label: "安全", key: "security" },
    ],
  },
];

export default {
  data() {
    axios.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${sessionStorage.getItem("token")}`;
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
        // 提示内容
        if (req.data.detail) msg.success(req.data.detail);
        return req;
      },
      (err) => {
        ldb.error();
        if (typeof err.response.data.detail == "string") {
          // 403身份验证失败
          if (err.response.status == 403) this.signout();
          // 提示内容
          msg.error(err.response.data.detail);
        }
      }
    );
    axios
      .get("/u/")
      .then((req) => {
        this.$store.commit("user", req.data);
      })
      .catch(this.signout);
    return {
      menuBar,
      request,
      response,
      active: false,
    };
  },
  methods: {
    menuValue(key) {
      // 导航跳转路径
      this.active = false;
      this.$router.push({ name: key });
    },
    signout() {
      // 清除所有数据并登出
      sessionStorage.clear();
      this.$store.commit("clear_all");
      this.$router.push("/verify/login");
      document.querySelector("html").style = "";
    },
  },
  beforeUnmount() {
    // 清除绑定的头部
    axios.defaults.headers.common["Authorization"] = null;
    // 解除绑定的加载动效
    axios.interceptors.request.eject(this.request);
    axios.interceptors.response.eject(this.response);
  },
  // 注册组件
  components: { PersonCircle, ListSharp, Contrast },
};
</script>