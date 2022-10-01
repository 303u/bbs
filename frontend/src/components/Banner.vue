<template>
  <n-carousel draggable autoplay>
    <n-card :key="li" v-for="li of banner">
      <template #cover>
        <n-card id="cov" :bordered="false">
        </n-card>
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
      <n-skeleton text width="70%" v-if="li.body == ''" />
      <n-skeleton text :repeat="3" v-if="li.body == ''" />
      <n-ellipsis v-else :line-clamp="4" :tooltip="false">
        {{ li.body }}
      </n-ellipsis>
    </n-card>
  </n-carousel>
</template>

<script>
import { Link } from "@vicons/ionicons5";
export default {
  name: "Banner",
  data() {
    return {
      banner: [
        { title: "版本公告", body: "", url: "" },
        { title: "使用提示", body: "", url: "" },
      ],
    };
  },
  methods: {
    open(id) {
      // 前往项目
      this.$router.push({ name: "item", params: { id } })
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

#cov::after {
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

#cov::before {
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
