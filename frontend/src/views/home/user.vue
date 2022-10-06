<template>
    <n-space vertical>
        <!-- 头部 -->
        <n-card>
            <template #header>
                <n-space>
                    <!-- 头像 -->
                    <n-avatar>{{ this.$route.params.id }}</n-avatar>
                    <!-- 名称 -->
                    <!-- <n-ellipsis style="width: 155px; margin-top: 3px" :tooltip="false">
                        {{ $store.state.user_info[id]?.name }}
                    </n-ellipsis> -->
                </n-space>
            </template>
            <template #action>
                <!-- <n-text> {{ $store.state.user_info[id].id }} </n-text> -->
                {{ this.$route.params.id }}
            </template>
        </n-card>
        <!-- 其他信息 -->
        <UserInfoVue />
        <DataListVue>
            <template #header>插槽</template>
        </DataListVue>
    </n-space>
</template>

<script>
import DataListVue from "@/components/DataList.vue";
import UserInfoVue from "@/components/UserInfo.vue";

// import axios from "axios";
export default {
    data() {
        // 判断是否已加载过此信息
        return {}
    },
    methods: {
    },
    components: { UserInfoVue, DataListVue }
};
</script>