<template>
    <n-list>
        <n-card>
            <n-collapse default-expanded-names="A" accordion>
                <n-collapse-item title="修改信息" name="A">
                    <n-card style="max-width: 360px">
                        <n-form :model="u" :rules="rules">
                            <n-form-item-row>
                                <n-checkbox v-model:checked="a.n">
                                    名称
                                </n-checkbox>
                                <n-checkbox v-model:checked="a.e">
                                    邮箱
                                </n-checkbox>
                                <n-checkbox v-model:checked="a.p">
                                    密码
                                </n-checkbox>
                            </n-form-item-row>
                            <n-collapse-transition :show="a.n">
                                <n-form-item-row label="新账户名称" path="name">
                                    <n-input v-model:value="u.name" />
                                </n-form-item-row>
                            </n-collapse-transition>
                            <n-collapse-transition :show="a.e">
                                <n-form-item-row
                                    label="新对接邮箱"
                                    path="email"
                                >
                                    <n-input
                                        v-model:value="u.email"
                                        type="email"
                                    />
                                </n-form-item-row>
                            </n-collapse-transition>
                            <n-collapse-transition :show="a.p">
                                <n-form-item-row
                                    label="输入新密码"
                                    path="password"
                                >
                                    <n-input
                                        v-model:value="u.password"
                                        type="password"
                                        show-password-on="click"
                                    />
                                </n-form-item-row>
                            </n-collapse-transition>
                            <n-collapse-transition :show="a.p || a.e">
                                <n-form-item-row
                                    label="输入验证码"
                                    path="token"
                                >
                                    <n-input-group>
                                        <n-input v-model:value="u.token" />
                                        <n-button @click="get_token">
                                            获取
                                        </n-button>
                                    </n-input-group>
                                </n-form-item-row>
                            </n-collapse-transition>
                            <n-button block type="primary" @click="change">
                                提交
                            </n-button>
                        </n-form>
                    </n-card>
                </n-collapse-item>

                <n-collapse-item title="注销账号">
                    <n-card style="max-width: 360px">
                        <n-space vertical>
                            <n-steps
                                vertical
                                :current="current"
                                :status="'process'"
                            >
                                <n-step title="确认文件"></n-step>
                                <n-step title="提交申请"></n-step>
                                <n-step title="注销成功"></n-step>
                            </n-steps>
                            <n-divider />

                            <n-space vertical v-if="current == 1">
                                <n-collapse accordion>
                                    <n-collapse-item title="账户相关">
                                        注销账号的信息无法恢复
                                    </n-collapse-item>
                                    <n-collapse-item title="数据处理">
                                        评论与项目会按删除处理
                                    </n-collapse-item>
                                </n-collapse>
                                <n-divider />
                                <n-button block @click="current = 2">
                                    已知悉并同意条款
                                </n-button>
                            </n-space>

                            <n-space vertical v-if="current == 2">
                                <n-alert title="无法撤销" type="warning">
                                    请在阅读注销确认事项后注销账号
                                </n-alert>
                                <n-button block @click="current = 1">
                                    返回上条
                                </n-button>
                                <n-button
                                    block
                                    type="error"
                                    @click="cancel_account"
                                >
                                    确认注销
                                </n-button>
                            </n-space>

                            <n-space vertical v-if="current == 3">
                                <n-result status="success" title="成功">
                                    <template #footer>
                                        已完成注销操作，将在三秒左右自动退出账号。
                                    </template>
                                </n-result>
                            </n-space>
                        </n-space>
                    </n-card>
                </n-collapse-item>
            </n-collapse>
        </n-card>
    </n-list>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            current: 1,
            code: null,
            a: { n: false, e: false, p: false },
            u: {
                name: "",
                email: "",
                password: "",
                token: "",
            },
            rules: {
                name: {
                    required: true,
                    message: "2-16位长度",
                    trigger: ["input", "blur"],
                    validator(_, val) {
                        return /^.{2,16}$/.test(val);
                    },
                },
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
                        return /^\w{8,16}$/.test(val);
                    },
                },
            },
        };
    },
    methods: {
        cancel_account() {
            axios.delete("/u/").then(() => {
                sessionStorage.clear();
                this.current = 3;
                setTimeout(() => {
                    this.$router.push("/verify");
                }, 3000);
            });
        },
        get_token() {
            axios.post("/u/t/").then((req) => {
                this.code = req.data.code;
            });
        },
        change() {
            if (!this.a.n) this.u.name = null;
            if (!this.a.e) this.u.email = null;
            if (!this.a.p) this.u.password = null;
            if ((this.a.e || this.a.p) && /^\w{8}$/.test(this.u.token)) {
                if (this.a.n && !/^.{2,16}$/.test(this.u.name)) return;
                if (this.a.p && !/^\w{8,16}$/.test(this.u.password)) return;
                if (this.a.e && !/^\w{4,32}\@\w+\.\w+$/.test(this.u.email))
                    return;
            } else if (this.a.n && /^.{2,16}$/.test(this.u.name)) {
            } else return;
            let name = this.u.name;
            axios
                .put("/u/?token=" + this.u.token, this.u, {
                    headers: { code: this.code },
                })
                .then(() => {
                    if (name) this.$store.state.user.name = name;
                });
            this.u.name = this.u.email = this.u.password = "";
        },
    },
};
</script>