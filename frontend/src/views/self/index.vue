<template>
  <n-space vertical>
    <n-card class="user-card" size="large" :bordered="false">
      <!-- 用户名称 -->
      <template #header>{{ $store.state.user.name }}</template>
      <!-- 用户头像 -->
      <template #header-extra>
        <n-avatar></n-avatar>
      </template>
      <!-- 菜单栏 -->
      <n-menu :value="$route.name" mode="horizontal" :options="menuBar" @update:value="menuValue" />
    </n-card>

    <!-- 保存状态 在调试情况下会导致热重载报错 -->
    <!-- <router-view v-slot="{ Component }">
      <keep-alive exclude="user, history">
        <component :is="Component" />
      </keep-alive>
    </router-view> -->
    <router-view></router-view>
  </n-space>
</template>

<script>
// 菜单栏
import { PersonCircle } from "@vicons/ionicons5";
export default {
  data() {
    return {
      menuBar: [
        { label: "主页", key:"self", },
        { label: "安全", key: "security", }
      ],
    };
  },
  methods: {
    menuValue(key) {
      // 导航跳转路径
      this.$router.push({ name: key });
    },
  },
  components: { PersonCircle },
};
</script>

<style scoped>
.user-card {
  z-index: 0;
  overflow: hidden;
  background: linear-gradient(45deg,
      rgba(0, 130, 255, 0.25) 0%,
      rgba(0, 170, 255, 0.75) 100%);
}

.user-card::after {
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

.user-card::before {
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