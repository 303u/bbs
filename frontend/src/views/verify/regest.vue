<template>
  <n-form :model="u" :rules="rules">
    <n-form-item-row label="邮箱账号" path="email">
      <n-input clearable type="email" v-model:value="u.email" maxlength="64" />
    </n-form-item-row>
    <n-form-item-row label="账号密码" path="password">
      <n-input clearable type="password" show-password-on="click" v-model:value="u.password" maxlength="24" />
    </n-form-item-row>
    <n-form-item-row label="使用名称" path="name">
      <n-input clearable v-model:value="u.name" maxlength="20" />
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
          message: "1-20位长度",
          trigger: ["input", "blur"],
          validator(_, val) {
            return val.length > 0;
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
            return val.length > 5;
          },
        },
      },
    };
  },
  methods: {
    register() {
      if (
        this.u.name.length > 0 &&
        /^\w{2,32}\@\w+\.\w+$/.test(this.u.email) &&
        this.u.password.length > 5
      ) {
        axios.post("/u/", this.u).then(() => {
          this.$router.push({ name: "login" })
        });
      }
    },
  },
};
</script>