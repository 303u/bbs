<template>
  <n-space>
    <n-tag checkable v-for="li of data.split(',')" :key="li" round @click="search(li)">
      <!-- 省略超长tag -->
      <n-ellipsis style="max-width: 220px;overflow: hidden">
        {{ li }}
        <!-- hover显示详情 -->
        <template #tooltip>
          <div>{{ li }}</div>
        </template>
      </n-ellipsis>
    </n-tag>
  </n-space>
</template>

<script>
export default {
  props: { data: String, },
  data() {
    return {}
  },
  methods: {
    search(li) {
      this.$router.push({ name: "search", params: { keyword: li } })
    }
  }
};
</script>

<style scoped>
.n-tag {
  max-width: 230px;
}


div {
  max-width: 230px;
  word-wrap: break-word;
}
</style>