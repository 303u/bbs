<template>
  <n-grid cols="12" x-gap="7" y-gap="7" item-responsive responsive="self">
    <!-- 用户信息 -->
    <n-gi span="12 700:5 1200:4">
      <UserInfoVue />
    </n-gi>

    <!-- 内容组件 -->
    <n-gi span="12 700:7 1200:8">
      <n-space vertical>
        <!-- 文章 -->
        <DataListVue :avater="0" :description="0" :url="'/i/'" :author="$store.state.user.id"  ref="DataList">
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
                <!-- 新建按钮 -->
                <n-button circle tertiary type="success" @click="$router.push({name:'write'})">
                  <template #icon>
                    <n-icon>
                      <Add />
                    </n-icon>
                  </template>
                </n-button>
              </n-space>
            </n-space>
          </template>
        </DataListVue>

        <!-- 历史浏览记录 -->
        <n-list bordered>
          <!-- 头部内容 -->
          <template #header>
            <n-space justify="space-between">
              <n-h3 align-text style="margin-bottom: 0;">本地历史记录</n-h3>
              <n-space>
                <!-- 刷新按钮 -->
                <n-button circle tertiary type="info" @click="get_history_data">
                  <template #icon>
                    <n-icon>
                      <Reload />
                    </n-icon>
                  </template>
                </n-button>
                <!-- 清空按钮 -->
                <n-button circle tertiary type="error" @click="clear_history">
                  <template #icon>
                    <n-icon>
                      <TrashOutline />
                    </n-icon>
                  </template>
                </n-button>
              </n-space>
            </n-space>
          </template>

          <n-list-item v-if="!list.length">
            <n-empty description="空空如也"></n-empty>
          </n-list-item>

          <!-- 跳入内容 -->
          <n-list-item :key="li" v-for="li of list" @click="$router.push('/item/' + li.id)">
            <n-thing content-indented>
              <!-- 头像 -->
              <template #avatar>
                <div @mouseover="hover = 1" @mouseout="hover = 0">
                  <PopupCardVue :id="li.author" />
                </div>
              </template>
              <!-- 标题 -->
              <template #header>{{ li.title }}</template>
              <template #description>{{ $store.state.user_info[li.author]?.name }}</template>
            </n-thing>
          </n-list-item>

          <template #footer>
            <n-space justify="center">
              <n-pagination :page-slot="5" v-model:page="page" :on-update:page="on_history_show" :page-size="5"
                :item-count="data.length" />
            </n-space>
          </template>
        </n-list>
      </n-space>
    </n-gi>
  </n-grid>
</template>

<script>
import { Add, Reload, TrashOutline, Eye, Pencil } from "@vicons/ionicons5";
import PopupCardVue from "@/components/PopupCard.vue";
import UserInfoVue from "@/components/UserInfo.vue";
import DataListVue from "@/components/DataList.vue";
export default {
  data() {
    return {
      data: this.$store.state.history,
      list: this.$store.state.history.slice(0, 5),
      lock: 0,
      page: 1,
    };
  },
  methods: {
    get_history_data() {
      this.page = 1;
      this.data = this.$store.state.history;
      this.list = this.data.slice(0, 5);
    },
    clear_history() {
      this.$store.commit("clear_history");
      this.get_history_data();
    },
    on_history_show(page) {
      this.page = page;
      this.list = this.data.slice((page - 1) * 5, page * 5);
    },
  },
  components: {
    Reload, TrashOutline, Add, Eye, Pencil,
    PopupCardVue, UserInfoVue, DataListVue
  }
  // beforeMount() {},
  // beforeUnmount() {},
  // activated() {},
};
</script>