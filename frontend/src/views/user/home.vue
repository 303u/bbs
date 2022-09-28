<template>
  <n-list bordered>
    <template #header>
      <n-space justify="space-between">
        <n-button @click="get_data">刷新</n-button>
        <n-radio-group v-model:value="type">
          <n-radio-button :value="0"> 查看 </n-radio-button>
          <n-radio-button :value="1"> 修改 </n-radio-button>
          <n-radio-button :value="2"> 删除 </n-radio-button>
        </n-radio-group>
      </n-space>
    </template>

    <n-list-item :key="li" v-for="li of list" @click="exec(li)">
      <n-thing content-indented>
        <template #header>{{ li.title }}</template>
        <template #description>
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
import axios from "axios";

export default {
  name: "home",
  data() {
    axios.get("/i/?me=1").then((req) => {
      this.data = req.data;
      this.list = this.data.slice(0, 5);
      this.lock = !req.data.length < 40;
    });
    return {
      data: [],
      list: [],
      lock: 0,
      page: 1,
      size: 5,
      type: 0,
    };
  },
  methods: {
    get_data() {
      axios.get("/i/?me=1").then((req) => {
        this.page = 1;
        this.lock = !req.data.length < 40;
        this.data = req.data;
        this.list = this.data.slice(0, 5);
      });
    },
    on_show(page) {
      this.page = page;
      if (page >= this.data.length / 5 && !this.lock) {
        axios.get("/i/?me=1&skip=" + parseInt(page / 8)).then((req) => {
          this.data.push(...req.data);
          this.lock = !req.data.length < 40;
        });
      }
      this.list = this.data.slice((page - 1) * 5, page * 5);
    },
    exec(item) {
      if (this.type == 1) {
        this.$router.push("/rewrite/" + item.id);
      } else if (this.type == 2) {
        this.data.splice(this.data.indexOf(item), 1);
        this.list = this.data.slice((this.page - 1) * 5, this.page * 5);
        axios.delete("/i/" + item.id);
      } else {
        this.$router.push("/item/" + item.id);
      }
    },
  },
  // beforeMount() {},
  // beforeUnmount() {},
};
</script>