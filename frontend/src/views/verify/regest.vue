<template>
  <n-form :model="u" :rules="rules">
    <n-form-item-row label="邮箱账号" path="email">
      <n-input clearable type="email" v-model:value="u.email" />
    </n-form-item-row>
    <n-form-item-row label="账号密码" path="password">
      <n-input
        clearable
        type="password"
        show-password-on="click"
        v-model:value="u.password"
      />
    </n-form-item-row>
    <n-form-item-row label="使用名称" path="name">
      <n-input clearable v-model:value="u.name" />
    </n-form-item-row>
    <n-button block type="primary" @click="register">注册</n-button>
  </n-form>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      u: { name: "", email: "", password: "" },
      rules: {
        name: {
          required: true,
          message: "1-16位长度",
          trigger: ["input", "blur"],
          validator(_, val) {
            return /^.{1,20}$/.test(val);
          },
        },
        email: {
          required: true,
          message: "邮箱格式不匹配",
          trigger: ["input", "blur"],
          validator(_, val) {
            return /^\w{2,32}\@\w+\.\w+$/.test(val);
          },
        },
        password: {
          required: true,
          message: "6-24位任意字符",
          trigger: ["input", "blur"],
          validator(_, val) {
            return /^.{6,24}$/.test(val);
          },
        },
      },
    };
  },
  methods: {
    register() {
      if (
        /^.{1,20}$/.test(this.u.name) &&
        /^\w{2,32}\@\w+\.\w+$/.test(this.u.email) &&
        /^.{6,24}$/.test(this.u.password)
      ) {
        axios.post("/u/", this.u);
      }
    },
  },
};
</script>