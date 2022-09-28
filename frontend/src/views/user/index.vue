<template>
  <n-space vertical>
    <n-card id="user" size="large" :bordered="false">
      <template #header>
        <!-- 用户名称 -->
        {{ $store.state.user.name }}
      </template>
      <template #header-extra>
        <!-- 用户头像 -->
        <n-avatar>
          <n-icon>
            <PersonCircle />
          </n-icon>
        </n-avatar>
      </template>
      <n-space>
        <n-button @click="c(0)" text>
          <n-text :type="$route.name == 'user' ? 'success' : ''"> 主页 </n-text>
        </n-button>
        <n-button @click="c(1)" text>
          <n-text :type="$route.name == 'history' ? 'success' : ''">
            历史
          </n-text>
        </n-button>
        <n-button @click="c(2)" text>
          <n-text :type="$route.name == 'security' ? 'success' : ''">
            安全
          </n-text>
        </n-button>
      </n-space>
    </n-card>

    <!-- 保存状态 在调试情况下会导致热重载报错 -->
    <!-- <router-view v-slot="{ Component }">
      <keep-alive exclude="user, history">
        <component :is="Component" />
      </keep-alive>
    </router-view> -->

    <n-grid cols="12" item-responsive responsive="self">
      <n-grid-item span="12 700:3 1400:2">
        <n-menu :options="menuBar" :default-value="$route.name" :value="$route.name"/>
      </n-grid-item>
      <n-grid-item span="12 700:9 1400:10">
        <router-view></router-view>
      </n-grid-item>
    </n-grid>
  </n-space>
</template>

<script>
// 菜单栏
const menuBar = [
  { label: "主页", key: "user" },
  { label: "历史", key: "history" },
  { label: "安全", key: "security" },
];
import { PersonCircle } from "@vicons/ionicons5";
export default {
  data() {
    return {
      menuBar,
    };
  },
  methods: {
    c(page) {
      this.page = page;
      this.$router.push({ name: ["user", "history", "security"][page] });
    },
  },
  components: { PersonCircle },
};
</script>

<style scoped>
.n-card#user {
  background: linear-gradient(45deg,
      rgba(0, 130, 255, 0.25) 0%,
      rgba(0, 170, 255, 0.75) 100%);
  overflow: hidden;
}

.n-card#user {
  z-index: 0;
}

.n-card#user::after {
  top: 0;
  z-index: -10;
  content: "";
  display: block;
  position: absolute;
  transform: rotate(45deg);
  width: 100vw;
  height: 100vw;
  background: #59f5;
  animation: aftera 6s linear infinite;
}

.n-card#user::before {
  top: 0;
  z-index: -10;
  content: "";
  display: block;
  position: absolute;
  transform: rotate(10deg);
  width: 100vw;
  height: 100vw;
  background: #59f3;
  animation: beforea 6s linear infinite;
}

@keyframes aftera {
  0% {
    transform: rotate(90deg);
  }

  100% {
    transform: rotate(180deg);
  }
}

@keyframes beforea {
  0% {
    transform: rotate(45deg);
  }

  100% {
    transform: rotate(135deg);
  }
}
</style>