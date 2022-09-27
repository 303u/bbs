<template>
    <n-avatar @mouseover="this.show = 1" @mouseout="show = 0"> </n-avatar>
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
        id: { type: String, default: "" },
    },
    data() {
        let info = this.$store.state.user_info[this.id] || {};
        if (!info.id && this.id) {
            axios.get("/u/" + this.id).then((re) => {
                this.user = re.data;
                this.$store.commit("add_user_info", re.data);
            });
        }
        return {
            user: info,
            show: false,
        };
    },
    methods: {},
};
</script>

<style scoped>
.n-card {
    z-index: 10;
    width: 270px;
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
    width: 700px;
    height: 700px;
    background: #59f5;
}
.n-card::before {
    top: 0;
    z-index: -10;
    content: "";
    display: block;
    position: absolute;
    transform: rotate(10deg);
    width: 700px;
    height: 700px;
    background: #59f3;
}
</style>