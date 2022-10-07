<template>
  <n-space vertical>
    <!-- banner 横幅 -->
    <BannerVue />

    <n-grid cols="10" x-gap="6" y-gap="6" item-responsive responsive="self">
      <!-- 内容主栏 -->
      <n-gi span="10 800:6 1200:7">
        <n-space vertical>
          <DataListVue ref="DataList">
            <template #header>
              <n-space vertical>
                <n-input-group>
                  <!-- 刷新按钮 -->
                  <n-button tertiary type="info" @click="$refs.DataList.get_data()">
                    <template #icon>
                      <n-icon>
                        <Reload />
                      </n-icon>
                    </template>
                  </n-button>
                  <!-- 输入控件 -->
                  <n-input clearable v-model:value="keywords" @keyup.enter="search" />
                  <!-- 搜索按钮 -->
                  <n-button tertiary type="primary" @click="search">
                    <template #icon>
                      <n-icon>
                        <Search />
                      </n-icon>
                    </template>
                  </n-button>
                </n-input-group>
              </n-space>
            </template>
          </DataListVue>
        </n-space>
      </n-gi>

      <!-- 站点公告 -->
      <n-gi id="tips" span="10 800:4 1200:3">
        <TipsVue />
      </n-gi>
    </n-grid>

    <!-- 其他推荐 -->
    <IntroVue />
  </n-space>
</template>

<script>
import { Link, Search, Reload, BatteryCharging } from "@vicons/ionicons5";
import PopupCardVue from "@/components/PopupCard.vue";
import BannerVue from "@/components/Banner.vue";
import TipsVue from "@/components/Tips.vue";
import IntroVue from "@/components/Intro.vue";
import DataListVue from "@/components/DataList.vue";
export default {
  name: "home",
  data() {
    return {
      keywords: "",
    };
  },
  methods: {
    search() {
      // 跳转查询页面
      this.$router.push({ name: "search", params: { keyword: this.keywords } })
    },
  },
  components: {
    Link, Search, Reload, BatteryCharging,
    PopupCardVue, BannerVue, TipsVue, IntroVue, DataListVue
  },
};
</script>

<style scoped>
#tips {
  top: 7vh;
  position: sticky;
}

.item_body {
  max-width: 85vw;
}

@media (min-width: 448px) {
  .item_body {
    max-width: 90vw;
  }
}
</style>