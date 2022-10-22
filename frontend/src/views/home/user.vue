<template>
  <n-space vertical>
    <!-- 头部 -->
    <n-card>
      <!-- 用户名称 -->
      <template #header> {{ info.name }} </template>
      <!-- 用户头像 -->
      <template #header-extra>
        <n-avatar></n-avatar>
      </template>
      <n-text v-if="info.motto">{{ info.motto }}</n-text>
      <n-text v-else depth="3" underline>这位用户很懒，没有留言哦。</n-text>
      <template #action>
        <!-- TODO: 举报，关注等 -->
      </template>
    </n-card>
    <!-- 其他信息 -->
    <n-grid cols="12" x-gap="7" y-gap="7" item-responsive responsive="self">
      <!-- 用户信息 -->
      <n-gi span="12 800:5 1200:4">
        <UserInfoVue :id="id" />
      </n-gi>

      <!-- 用户文章 -->
      <n-gi span="12 800:7 1200:8">
        <n-space vertical>
          <DataListVue :avater="0" :description="0" :url="'/items/'" v-model:author="id" ref="DataList">
            <template #header>
              <n-space justify="space-between">
                <n-h3 align-text style="margin-bottom: 0;">用户文章</n-h3>
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
    let id = this.$route.params.id;
    // 发送请求获最新取数据
    axios.get("/info/" + id).then((re) => {
      this.$store.commit("insert_info", re.data);
      this.info = re.data;
    });
    return {
      id,
      info: this.$store.state.user_info[id] || {},
    }
  },
  components: {
    Reload,
    UserInfoVue, DataListVue, IntroVue,
  },
  watch: {
    $route() {
      this.id = this.$route.params.id
      axios.get("/info/" + this.id).then((re) => {
        this.$store.commit("insert_info", re.data);
        this.info = re.data;
      });
    }
  }
};
</script>