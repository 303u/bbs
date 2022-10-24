<template>
  <n-grid cols="12" item-responsive responsive="self">
    <!-- 信息修改 -->
    <n-gi span="12 700:6 1200:4">
      <n-card>
        <n-collapse default-expanded-names="user_info" accordion>
          <n-collapse-item title="修改信息" name="user_info">
            <n-form :model="u" :rules="rules">
              <n-form-item-row>
                <n-checkbox v-model:checked="a.n"> 名称 </n-checkbox>
                <n-checkbox v-model:checked="a.e"> 邮箱 </n-checkbox>
                <n-checkbox v-model:checked="a.p"> 密码 </n-checkbox>
              </n-form-item-row>
              <n-collapse-transition :show="a.n">
                <n-form-item-row label="新账户名称" path="name">
                  <n-input v-model:value="u.name" maxlength="20" />
                </n-form-item-row>
              </n-collapse-transition>
              <n-collapse-transition :show="a.e">
                <n-form-item-row label="新对接邮箱" path="email">
                  <n-input v-model:value="u.email" type="email" maxlength="64" />
                </n-form-item-row>
              </n-collapse-transition>
              <n-collapse-transition :show="a.p">
                <n-form-item-row label="输入新密码" path="password">
                  <n-input v-model:value="u.password" type="password" show-password-on="click" maxlength="24"
                    :input-props="{ autocomplete:false }" />
                </n-form-item-row>
              </n-collapse-transition>
              <n-collapse-transition :show="a.p || a.e">
                <n-form-item-row label="输入验证码" path="token" maxlength="8">
                  <n-input-group>
                    <n-input v-model:value="u.token" />
                    <n-button @click="get_token"> 获取 </n-button>
                  </n-input-group>
                </n-form-item-row>
              </n-collapse-transition>
              <n-button block type="primary" @click="change"> 提交 </n-button>
            </n-form>
          </n-collapse-item>

          <n-collapse-item title="注销账号">
            <n-space vertical>
              <n-steps vertical :current="current" :status="'process'">
                <n-step title="确认文件"></n-step>
                <n-step title="提交申请"></n-step>
                <n-step title="注销成功"></n-step>
              </n-steps>
              <n-divider />

              <n-space vertical v-if="current == 1">
                <n-collapse accordion>
                  <n-collapse-item title="账户相关"></n-collapse-item>
                  <n-collapse-item title="数据处理"></n-collapse-item>
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
                <n-button block @click="current = 1"> 返回上条 </n-button>
                <n-button block type="error" @click="cancel_account">
                  确认注销
                </n-button>
              </n-space>

              <n-space vertical v-if="current == 3">
                <n-result status="success" title="成功">
                  <template #footer>
                    已完成注销操作，将自动退出账号。
                    <n-countdown :duration="3000" :active="current == 3" />
                  </template>

                </n-result>
              </n-space>
            </n-space>
          </n-collapse-item>
        </n-collapse>
      </n-card>
    </n-gi>
    <!-- 安全信息展示 -->
    <n-gi span="6 700:3 1200:4">
      <n-timeline>
        <n-timeline-item type="success" title="邮箱号绑定" content="已绑定" />
        <n-timeline-item type="error" title="手机号绑定" content="等待完善" />
        <n-timeline-item type="error" title="身份验证" content="等待完善" />
        <n-timeline-item type="info" title="信息完善" content="等待完善" line-type="dashed" />
        <n-timeline-item content="等待完善">
          <template #icon>
            <n-icon></n-icon>
          </template>
        </n-timeline-item>
      </n-timeline>
    </n-gi>
    <!-- 百分比效果 -->
    <n-gi span="6 700:3 1200:4">
      <n-space justify="center">
        <n-progress type="dashboard" gap-position="bottom" :percentage="25">
          <n-statistic tabular-nums>
            <n-number-animation show-separator :from="0" :to="25" />
          </n-statistic>
          <n-text>%</n-text>
        </n-progress>
      </n-space>
      <n-h2 prefix="bar" type="error">请完善信息</n-h2>
      <n-button block @click="$router.push({name:'self'})">快速前往</n-button>
    </n-gi>
    <!-- 日历 -->
    <n-gi span="0 700:12">
      <n-calendar #="{ year, month, date }">
        {{ year }}-{{ month }}-{{ date }}
      </n-calendar>
    </n-gi>
  </n-grid>
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
          message: "最少6位",
          trigger: ["input", "blur"],
          validator(_, val) {
            return val.length > 5;
          },
        },
        token: {
          required: true,
          message: "8位长度",
          trigger: ["input", "blur"],
          validator(_, val) {
            return val.length == 8;
          },
        },
      },
    };
  },
  methods: {
    cancel_account() {
      axios.delete("/users/").then(() => {
        this.current = 3;
        // 清空用户数据
        sessionStorage.clear();
        localStorage.clear();
        this.$store.commit("clear_all")
        this.$router.push("/verify");
      });
    },
    get_token() {
      axios.post("/users/token").then((req) => {
        this.code = req.data.code;
      });
    },
    change() {
      if (!this.a.n) this.u.name = null;
      if (!this.a.e) this.u.email = null;
      if (!this.a.p) this.u.password = null;
      if ((this.a.e || this.a.p) && this.u.token.length == 8) {
        if (this.a.n && !this.u.name.length) return;
        if (this.a.p && !/^\w{6,24}$/.test(this.u.password)) return;
        if (this.a.e && !/^\w{2,32}\@\w+\.\w+$/.test(this.u.email)) return;
      } else if (this.a.n && this.u.name.length) {
      } else return;
      let name = this.u.name;
      axios
        .put("/users/?token=" + this.u.token, this.u, {
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
<style scoped>
.n-timeline {
  margin: 15px;
}

.n-progress,
.n-calendar {
  margin-top: 15px;
}
</style>