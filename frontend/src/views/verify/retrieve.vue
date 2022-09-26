<template>
  <n-form :model="u" :rules="rules">
    <n-form-item-row label="邮箱账号" path="email">
      <n-input clearable v-model:value="u.email" />
    </n-form-item-row>
    <n-form-item-row label="新密码" path="password">
      <n-input clearable type="password" show-password-on="click" v-model:value="u.password" />
    </n-form-item-row>
    <n-form-item-row label="验证码" path="token">
      <n-input-group>
        <n-input clearable v-model:value="u.token" />
        <n-button @click="recovery" :disabled="!u.email">获取</n-button>
      </n-input-group>
    </n-form-item-row>
    <n-button block @click="submit" type="primary">提交</n-button>
  </n-form>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            code: null,
            current: 0,
            u: {
                email: null,
                token: null,
                password: null,
            },
            rules: {
                email: {
                    required: true,
                    message: "邮箱格式不匹配",
                    trigger: ["input", "blur"],
                    validator(_, val) {
                        return /^\w{4,32}\@\w+\.\w+$/.test(val);
                    },
                },
                token: {
                    required: true,
                    message: "8位长度",
                    trigger: ["input", "blur"],
                    validator(_, val) {
                        return /^\w{8}$/.test(val);
                    },
                },
                password: {
                    required: true,
                    message: "8-16位任意字符",
                    trigger: ["input", "blur"],
                    validator(_, val) {
                        return /^.{8,16}$/.test(val);
                    },
                },
            },
        };
    },
    methods: {
        recovery() {
            if (/^\w{4,32}\@\w+\.\w+$/.test(this.u.email)) {
                axios.post("/l/r/" + this.u.email).then((req)=>{
                    this.code = req.data.code
                });
            }
        },
        submit() {
            if (
                /^\w{8}$/.test(this.u.token) &&
                /^\w{4,32}\@\w+\.\w+$/.test(this.u.email) &&
                /^.{8,16}$/.test(this.u.password)
            ) {
                axios.post("/l/t/" + this.u.token, this.u,{ headers: { code: this.code }});
            }
        },
    },
};
</script>