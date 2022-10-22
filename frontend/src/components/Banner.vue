<template>
  <n-carousel draggable autoplay>
    <n-card :key="li" v-for="li of banner">
      <template #cover>
        <div v-if="!li.img" id="cov"></div>
        <div v-else :style="`background:url(${li.img}); background-size: cover; height:25vh`"></div>
      </template>
      <template #header>{{ li.title }}</template>
      <template #header-extra>
        <n-button circle @click="open(li.url)">
          <template #icon>
            <n-icon>
              <Link />
            </n-icon>
          </template>
        </n-button>
      </template>
      <div style="height: 7em;">
        <n-skeleton text width="70%" v-if="!li.description" />
        <n-skeleton text :repeat="3" v-if="!li.description" />
        <n-ellipsis v-else :line-clamp="4" :tooltip="false">
          {{ li.description }}
        </n-ellipsis>
      </div>
    </n-card>
  </n-carousel>
</template>

<script>
import { Link } from "@vicons/ionicons5";
import axios from "axios";
export default {
  data() {
    axios.get("/intro/banner").then((req) => {
      if (req.data.length) this.banner = req.data;
    })
    return {
      banner: [
        { title: "使用提示", img: "https://images.pexels.com/photos/13388836/pexels-photo-13388836.jpeg", },
        { title: "版本公告", img: "https://images.pexels.com/photos/13388662/pexels-photo-13388662.jpeg", },
      ],
    };
  },
  methods: {
    open(url) {
      // 前往项目
      if (url) this.$router.push({ name: "item", params: { id: url } });
    },
  },
  components: { Link },
};
</script>

<style scoped>
#cov {
  z-index: 0;
  height: 25vh;
  overflow: hidden;
  background: linear-gradient(45deg,
      rgba(0, 130, 255, 0.25) 0%,
      rgba(0, 170, 255, 0.75) 100%);
}
</style>
