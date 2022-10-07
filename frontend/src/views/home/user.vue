<template>
  <n-space vertical>
    <!-- 头部 -->
    <n-card>
      <!-- 用户名称 -->
      <template #header> {{ user.name }} </template>
      <!-- 用户头像 -->
      <template #header-extra>
        <n-avatar></n-avatar>
      </template>
      <template #footer>
        <n-text v-if="user.motto">{{ user.motto }}</n-text>
        <n-text v-else depth="3" underline>这位用户很懒，没有留下格言哦。</n-text>
      </template>
      <template #action>
        <n-time :time="Number($route.params.id?.substring(0, 10)||0)" :to="new Date().getTime() / 1000" type="relative"
          unix />
        <!-- <n-time :time="Number($route.params.id?.substring(0, 10)||0)" format="yyyy-MM-dd" unix /> -->
      </template>
    </n-card>
    <!-- 其他信息 -->
    <n-grid cols="12" x-gap="7" y-gap="7" item-responsive responsive="self">
      <!-- 用户信息 -->
      <n-gi span="12 800:5 1200:4">
        <UserInfoVue />
      </n-gi>

      <!-- 用户文章 -->
      <n-gi span="12 800:7 1200:8">
        <n-space vertical>
          <DataListVue :avater="0" :description="0" :url="'/i/'" :author="$route.params.id" ref="DataList">
            <template #header>
              <n-space justify="space-between">
                <n-h3 align-text style="margin-bottom: 0;">仓库文章</n-h3>
                <n-space>
                  <!-- 刷新按钮 -->
                  <n-button circle tertiary type="info" @click="$refs.DataList.get_data()">
                    <template #icon>
                      <n-icon>
                        <Reload />
                      </n-icon>
                    </template>
                  </n-button>
                </n-space>
              </n-space>
            </template>
          </DataListVue>
          <IntroVue />
        </n-space>
      </n-gi>
    </n-grid>
  </n-space>
</template>

<script>
import { Reload } from "@vicons/ionicons5";
import DataListVue from "@/components/DataList.vue";
import UserInfoVue from "@/components/UserInfo.vue";
import IntroVue from "@/components/Intro.vue";
import axios from "axios";
export default {
  data() {
    // 判断是否已加载过此信息
    let id = this.$route.params.id;
    if (!this.$store.state.user_info[id] && id) {
      // 如果没有，塞入默认信息防止多次请求
      this.$store.commit("insert_info", { id: id });
      // 发送请求获取默认数据
      axios.get("/u/" + id).then((re) => {
        this.$store.commit("insert_info", re.data);
        this.user = re.data
        console.log(this.user);
      });
    }
    return {
      user: this.$store.state.user_info[id],
    }
  },
  methods: {
  },
  components: {
    Reload,
    UserInfoVue, DataListVue, IntroVue,
  }
};
</script>