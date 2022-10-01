<template>
  <n-form :model="form" :rules="rules" @keyup.enter="submit">
    <n-form-item-row label="邮箱账号" path="username">
      <n-input clearable v-model:value="form.username" type="email" maxlength="64" />
    </n-form-item-row>
    <n-form-item-row label="账号密码" path="password">
      <n-input clearable v-model:value="form.password" type="password" show-password-on="click" maxlength="24" />
    </n-form-item-row>
    <n-form-item-row label="保持登录">
      <n-popover trigger="hover">
        <template #trigger>
          <n-switch v-model:value="keep" />
        </template>
        <n-text>选中可保持七天登录身份</n-text>
      </n-popover>
    </n-form-item-row>
    <n-button type="primary" @click="submit" block>登录</n-button>
    <n-form-item-row label="人机验证" v-if="verify.count > 1" path="verify">
      <n-slider v-model:value="verify.value" :marks="verify.key" range />
    </n-form-item-row>
  </n-form>
</template>

<script>
import axios from "axios";
export default {
  data() {
    // 先创建验证码的两个值，在需要验证时再校验
    let verify = { value: [0, 0], key: {}, count: 0 };
    return {
      verify,
      keep: false,
      form: {
        username: "",
        password: "",
      },
      rules: {
        verify: {
          required: true,
          message: "范围不正确",
          trigger: ["input", "blur"],
          validator() {
            return (
              verify.value[0] in verify.key &&
              verify.value[1] in verify.key &&
              verify.value[0] != verify.value[1]
            );
          },
        },
        username: {
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
    submit() {
      if (
        // 验证正常登录
        /^\w{2,32}\@\w+\.\w+$/.test(this.form.username) &&
        this.form.password.length > 5 &&
        !(this.verify.count > 1)
      ) {
      } else if (
        // 验证验证码登录
        /^\w{2,32}\@\w+\.\w+$/.test(this.form.username) &&
        this.form.password.length > 5 &&
        this.verify.value[0] in this.verify.key &&
        this.verify.value[1] in this.verify.key &&
        this.verify.value[0] != this.verify.value[1]
      ) {
      } else {
        // 失败次数增加
        this.verify.count++;
        // 清空两个验证码
        this.verify.key = {};
        // 创建两个验证码
        let key = Math.ceil(Math.random() * 100);
        this.verify.key[key] = key;
        key = Math.ceil(Math.random() * 100);
        while (key in this.verify.key) {
          key = Math.ceil(Math.random() * 100);
        }
        this.verify.key[key] = key;
        return;
      }
      let form = new FormData();
      form.append("username", this.form.username);
      form.append("password", this.form.password);
      this.form.username = this.form.password = "";
      axios
        .post("/l/", form)
        .then((req) => {
          // 保存身份token
          (this.keep ? localStorage : sessionStorage).token = req.data.access_token;
          this.$router.push("/");
        })
        .catch(() => {
          this.verify.count++;
        });
    },
  },
};
</script>