<template>
    <n-list bordered>
        <template #header>
            <n-space>
                <n-button @click="get_data">刷新</n-button>
                <n-button @click="clear_history">清空</n-button>
            </n-space>
        </template>

        <n-list-item v-if="!list.length">
            <n-empty description="暂无内容"></n-empty>
        </n-list-item>

        <n-list-item :key="li" v-for="li of list" @click="goto(li)">
            <n-thing content-indented>
                <template #header>{{ li.title }}</template>
                <template #header-extra>
                    <n-time :time="Number(li.time)" unix />
                </template>
                <n-ellipsis :line-clamp="2" :tooltip="false">
                    {{ li.body }}
                </n-ellipsis>
            </n-thing>
        </n-list-item>

        <template #footer>
            <n-space justify="center">
                <n-pagination
                    :page-slot="5"
                    v-model:page="page"
                    :on-update:page="on_show"
                    v-model:page-size="size"
                    :item-count="data.length"
                />
            </n-space>
        </template>
    </n-list>
</template>


<script>
export default {
    name: "history",
    data() {
        return {
            data: this.$store.state.history,
            list: this.$store.state.history.slice(0, 5),
            page: 1,
            size: 5,
        };
    },
    methods: {
        get_data() {
            this.page = 1;
            this.data = this.$store.state.history;
            this.list = this.data.slice(0, 5);
        },
        clear_history() {
            this.$store.commit("clear_history");
            this.get_data();
        },
        on_show(page) {
            this.page = page;
            this.list = this.data.slice((page - 1) * 5, page * 5);
        },
        goto(item) {
            this.$router.push("/item/" + item.id);
        },
    },
    // activated() {
    //     this.data = this.$store.state.history;
    //     this.on_show(this.page);
    // },
};
</script>
