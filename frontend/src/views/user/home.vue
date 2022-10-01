<template>
  <n-grid cols="12" item-responsive responsive="self">
    <!-- 其他信息 -->
    <!-- <n-timeline-item type="success" title="成功">
      <template #header>你加入了论坛</template>
      <n-time :time="Number($store.state.user.id?.substring(0, 10)||0)" :to="new Date().getTime() / 1000"
        type="relative" unix />
      <template #footer>
        <n-time :time="Number($store.state.user.id?.substring(0, 10)||0)" format="yyyy-MM-dd" unix />
      </template>
    </n-timeline-item> -->
    <n-grid-item span="12 700:5 1200:4" id="info">
      <n-list bordered>
        <n-list-item>
          <n-empty description="空空如也"></n-empty>
        </n-list-item>
        <n-list-item>
          <n-time :time="Number($store.state.user.id?.substring(0, 10)||0)" unix />
        </n-list-item>
        <n-list-item>
          <n-time :time="0" :to="864000000" type="relative" />
        </n-list-item>
        <n-list-item>
          <n-button block @click="$router.push('security')">修改信息</n-button>
        </n-list-item>
      </n-list>
    </n-grid-item>
    <!-- 文章 -->
    <n-grid-item span="12 700:7 1200:8">
      <n-space vertical>
        <n-list bordered>
          <template #header>
            <n-space justify="space-between">
              <n-h3 prefix="bar" align-text style="margin-bottom: 0;">仓库文章</n-h3>
              <n-space>
                <!-- 刷新按钮 -->
                <n-button circle tertiary type="info" @click="get_data">
                  <template #icon>
                    <n-icon>
                      <Reload />
                    </n-icon>
                  </template>
                </n-button>
                <!-- 清空按钮 -->
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
          <n-list-item v-if="!list.length">
            <n-empty description="空空如也"></n-empty>
          </n-list-item>

          <n-list-item :key="li" v-for="li of list">
            <n-thing content-indented>
              <!-- 标题 -->
              <template #header>{{ li.title }}</template>
              <!-- 时间 -->
              <template #description>
                <n-time :time="Number(li.time)" unix />
              </template>
              <!-- 大概内容 -->
              <n-ellipsis :line-clamp="2" :tooltip="false">
                {{ li.body }}
              </n-ellipsis>
              <!-- 操作 -->
              <template #action>
                <n-space>
                  <n-button @click="$router.push('/item/' + li.id)">查看</n-button>
                  <n-button @click="$router.push('/write/' + li.id)">修改</n-button>
                  <n-button @click="delete_item(li)">删除</n-button>
                </n-space>
              </template>
            </n-thing>
          </n-list-item>
          <!-- 翻页组件 -->
          <template #footer>
            <n-space justify="center">
              <n-pagination :page-slot="5" v-model:page="page" :on-update:page="on_show" :page-size="5"
                :item-count="data.length" />
            </n-space>
          </template>
        </n-list>

        <!-- 历史浏览记录 -->
        <n-list bordered>
          <!-- 头部内容 -->
          <template #header>
            <n-space justify="space-between">
              <n-h3 prefix="bar" align-text style="margin-bottom: 0;">本地历史记录</n-h3>
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
          <n-list-item v-if="!history.list.length">
            <n-empty description="空空如也"></n-empty>
          </n-list-item>

          <!-- 跳入内容 -->
          <n-list-item :key="li" v-for="li of history.list" @click="this.$router.push('/item/' + li.id)">
            <n-thing content-indented>
              <!-- 头像 -->
              <template #avatar>
                <div @mouseover="hover = 1" @mouseout="hover = 0">
                  <PopupCardVue :id="li.author" />
                </div>
              </template>
              <!-- 标题 -->
              <template #header>{{ li.title }}</template>
              <!-- 时间 -->
              <template #header-extra>
                <n-time :time="Number(li.time)" unix />
              </template>
            </n-thing>
          </n-list-item>

          <template #footer>
            <n-space justify="center">
              <n-pagination :page-slot="5" v-model:page="history.page" :on-update:page="on_history_show" :page-size="5"
                :item-count="history.data.length" />
            </n-space>
          </template>
        </n-list>
      </n-space>
    </n-grid-item>
  </n-grid>
</template>

<script>
import axios from "axios";
import { Add, Reload, TrashOutline } from "@vicons/ionicons5";
import PopupCardVue from "@/components/PopupCard.vue";
export default {
  name: "home",
  data() {
    axios.get("/i/?me=1").then((req) => {
      this.data = req.data;
      this.list = this.data.slice(0, 5);
      this.lock = !req.data.length < 40;
    });
    return {
      data: [],
      list: [],
      lock: 0,
      page: 1,
      history: {
        data: this.$store.state.history,
        list: this.$store.state.history.slice(0, 5),
        page: 1,
      }
    };
  },
  methods: {
    get_data() {
      axios.get("/i/?me=1").then((req) => {
        this.page = 1;
        this.lock = !req.data.length < 40;
        this.data = req.data;
        this.list = this.data.slice(0, 5);
      });
    },
    on_show(page) {
      this.page = page;
      if (page >= this.data.length / 5 && !this.lock) {
        axios.get("/i/?me=1&skip=" + parseInt(page / 8)).then((req) => {
          // 加入新数据
          this.data.push(...req.data);
          // 数据取完末尾锁定
          this.lock = !req.data.length < 40;
        });
      }
      this.list = this.data.slice((page - 1) * 5, page * 5);
    },
    delete_item(item) {
      axios.delete("/i/" + item.id).then(() => {
        this.data.splice(this.data.indexOf(item), 1);
        this.list = this.data.slice((this.page - 1) * 5, this.page * 5);
      });
    },
    get_history_data() {
      this.history.page = 1;
      this.history.data = this.$store.state.history;
      this.history.list = this.history.data.slice(0, 5);
    },
    clear_history() {
      this.$store.commit("clear_history");
      this.get_history_data();
    },
    on_history_show(page) {
      this.history.page = page;
      this.history.list = this.history.data.slice((page - 1) * 5, page * 5);
    },
  },
  components: { Reload, TrashOutline, Add, PopupCardVue }
  // beforeMount() {},
  // beforeUnmount() {},
  // activated() {},
};
</script>

<style scoped>
@media (min-width: 748px) {
  #info {
    margin-right: 7px;
  }
}

@media (max-width: 748px) {
  #info {
    margin-bottom: 7px;
  }
}
</style>