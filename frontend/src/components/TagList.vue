<template>
  <n-space>
    <n-tag checkable v-for="li of JSON.parse(data || '[]')" :key="li" round>
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
  name: "TagList",
  props: { data: String, },
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