<template>
    <n-carousel draggable autoplay>
        <n-card :key="li" v-for="li of banner">
            <template #header>{{ li.title }}</template>
            <template #header-extra>
                <n-button circle @click="open(li.url)">
                    <template #icon>
                        <n-icon><Link /></n-icon>
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
import { Link, Search, Reload } from "@vicons/ionicons5";

export default {
    name: "Banner",
    data() {
        return {
            banner: [
                { title: "声明", body: "", url: "" },
                { title: "公告", body: "", url: "" },
            ],
        };
    },
    methods: {
        open(url) {
            window.open(url);
        },
    },
    components: { Link, Search, Reload },
};
</script>

<style scoped>
.n-carousel {
    margin-bottom: 24px;
}
</style>