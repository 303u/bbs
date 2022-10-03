<template>
    <n-card>
        <template #cover>
            <WindmillVue :cls="winds" />
        </template>
        <template #header>站点公告</template>
        <!-- 风速按钮与弹窗 -->
        <template #header-extra>
            <n-popover trigger="hover">
                <template #trigger>
                    <n-button circle @click="winds = !winds">
                        <template #icon>
                            <n-icon>
                                <BatteryCharging />
                            </n-icon>
                        </template>
                    </n-button>
                </template>
                <span>调整动画风速</span>
            </n-popover>
        </template>
        <!-- 内容 -->
        <n-alert type="info">
            <n-skeleton text :repeat="6" />
            <n-skeleton text style="width: 60%" />
        </n-alert>
    </n-card>
</template>

<script>
import { BatteryCharging, Link } from "@vicons/ionicons5";
import WindmillVue from "@/components/Windmill.vue";
export default {
    data() {
        return {
            winds: true,
        }
    },
    components: {
        Link,
        BatteryCharging,
        WindmillVue,
    }
}
</script>

<style scoped>
.n-card {
    top: 7vh;
    position: sticky;
}

.n-timeline {
    margin: 15px 0;
}
</style>