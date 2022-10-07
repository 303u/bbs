<template>
  <n-card>
    <template #header>更多推荐</template>

    <!-- 推荐内容 -->
    <n-grid cols="12" item-responsive x-gap="6" y-gap="6">
      <n-gi span="12 400:6 800:4 1200:3" v-for="li in data">
        <n-card>
          <n-thing>
            <!-- 头像 -->
            <template #avatar>
              <PopupCardVue :id="li.author" />
            </template>
            <!-- 内容 -->
            <n-skeleton text :repeat="2" />
            <n-skeleton text style="width: 60%" />
          </n-thing>
        </n-card>
      </n-gi>
    </n-grid>

    <!-- 数量为空 -->
    <n-empty v-if="!data.length"></n-empty>
  </n-card>
</template>

<script>
import axios from 'axios';
import PopupCardVue from './PopupCard.vue';
export default {
  data() {
    // axios.get("/i/").then((req) => {
    //     // 载入数据
    //     this.data = req.data;
    // });
    return {
      data: [{}, {}, {}, {}, {}, {}]
      // data: []
    }
  },
  components: {
    PopupCardVue,
  }
}
</script>

<style scoped>

</style>