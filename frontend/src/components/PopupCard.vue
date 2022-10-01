<template>

  <!-- 弹窗hover 延迟100 -->
  <n-popover trigger="hover" :duration="100">
    <template #trigger>
      <!-- 默认外部显示头像 -->
      <n-avatar @click="show_user">
        <n-icon> </n-icon>
      </n-avatar>
    </template>

    <n-card>
      <template #header>
        <n-space>
          <!-- 头像 -->
          <n-avatar>
            <n-icon> </n-icon>
          </n-avatar>
          <!-- 名称 -->
          <n-ellipsis style="width: 155px; margin-top: 3px" :tooltip="false">
            {{ $store.state.user_info[id]?.name }}
          </n-ellipsis>
        </n-space>
      </template>
      <!-- 其他信息 -->
      <template #action>
        <n-text> {{ $store.state.user_info[id] }} </n-text>
      </template>
    </n-card>
  </n-popover>
</template>

<script>
import axios from "axios";
export default {
  name: "PopupCard",
  props: { id: { type: String, default: "" }, },
  data() {
    // 判断是否已加载过此信息
    if (!this.$store.state.user_info[this.id] && this.id) {
      // 如果没有，塞入默认信息防止多次请求
      this.$store.commit("insert_info", { id: this.id });
      // 发送请求获取默认数据
      axios.get("/u/" + this.id).then((re) => {
        this.$store.commit("insert_info", re.data);
      });
    }
    return {}
  },
  methods: {
    show_user() {
      // 前往用户详情页
      this.$router.push;
    },
  },
};
</script>

<style scoped>
.n-card {
  margin: 0;
  z-index: 10;
  width: 255px;
  overflow: hidden;
}

.n-card::after {
  top: 0;
  z-index: -10;
  content: "";
  display: block;
  position: absolute;
  transform: rotate(45deg);
  width: 700px;
  height: 700px;
  background: #59f5;
}

.n-card::before {
  top: 0;
  z-index: -10;
  content: "";
  display: block;
  position: absolute;
  transform: rotate(10deg);
  width: 700px;
  height: 700px;
  background: #59f3;
}
</style>