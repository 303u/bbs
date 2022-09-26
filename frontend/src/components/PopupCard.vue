<template>
    <n-avatar @mouseover="over" @mouseout="show = 0"> </n-avatar>
    <n-card v-show="show">
        <n-avatar>
            <n-icon> </n-icon>
        </n-avatar>
        <n-ellipsis style="max-width: 170px; margin: 12px" :tooltip="false">
            {{ user.name }}
        </n-ellipsis>
    </n-card>
</template>

<script>
import axios from "axios";
export default {
    name: "PopupCard",
    props: {
        id: { type: String },
    },
    data() {
        return {
            user: {},
            show: false,
        };
    },
    methods: {
        over() {
            if (!this.user.name) {
                axios.get("/u/" + this.id).then((re) => (this.user = re.data));
            }
            this.show = 1;
        },
    },
};
</script>

<style scoped>
.n-card {
    z-index: 0;
    width: 300px;
    overflow: hidden;
    position: absolute;
}
.n-card::after {
    top: 0;
    z-index: -10;
    content: "";
    display: block;
    position: absolute;
    transform: rotate(45deg);
    width: 100vw;
    height: 100vw;
    background: #59f5;
}
.n-card::before {
    top: 0;
    z-index: -10;
    content: "";
    display: block;
    position: absolute;
    transform: rotate(10deg);
    width: 100vw;
    height: 100vw;
    background: #59f3;
}
</style>