<template>
    <n-space>
        <n-tag v-for="li of JSON.parse(data || '[]')" :key="li" round>
            <n-ellipsis style="max-width: 230px">
                {{ li }}
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
    props: {
        data: String,
    },
    data() {
        return {};
    },
};
</script>

<style scoped>
.n-tag:hover {
    box-shadow: 2em #0007;
}
div {
    max-width: 230px;
    word-wrap: break-word;
}
</style>