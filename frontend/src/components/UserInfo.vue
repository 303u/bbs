<template>
  <n-space vertical>
    <!-- 关联信息 -->
    <n-card>
      <n-statistic tabular-nums>
        <n-text> 文章数量 </n-text>
        <n-number-animation show-separator :from="0" :to="info.item_count" />
      </n-statistic>
    </n-card>
    <!-- 个人信息 -->
    <n-table>
      <tbody>
        <tr>
          <td> 性别 </td>
          <td v-if="!edit">
            <n-text v-if="info.gender">男性</n-text>
            <n-text v-else>女性</n-text>
          </td>
          <td v-else>
            <n-radio-group v-model:value="info.gender">
              <n-radio-button :value="true" :label="'男性'" />
              <n-radio-button :value="false" :label="'女性'" />
            </n-radio-group>
          </td>
        </tr>
        <tr>
          <td> 城市 </td>
          <td v-if="!edit">
            <n-text v-if="info.city">{{ info.city }}</n-text>
            <n-text v-else depth="3" underline>未完善</n-text>
          </td>
          <td v-else>
            <n-input v-model:value="info.city" type="text" />
          </td>
        </tr>
        <tr>
          <td> 爱好 </td>
          <td v-if="!edit">
            <n-text v-if="info.hobby">{{ info.hobby }}</n-text>
            <n-text v-else depth="3" underline>未完善</n-text>
          </td>
          <td v-else>
            <n-input v-model:value="info.hobby" type="text" />
          </td>
        </tr>
        <tr>
          <td> 生日 </td>
          <td v-if="!edit">
            <n-time v-if="info.birthday" :time="info.birthday" format="yyyy-MM-dd" />
            <n-text v-else depth="3" underline>未完善</n-text>
          </td>
          <td v-else>
            <n-date-picker v-model:value="info.birthday" type="date" />
          </td>
        </tr>
        <tr>
          <td> 活跃 </td>
          <td>
            <n-time :time="info.last_login || 0" type="relative" unix />
          </td>
        </tr>
        <tr v-if="$store.state.user.id == id">
          <td colspan="2" v-if="!edit">
            <n-button block @click="edit = 1">修改信息</n-button>
          </td>
          <td colspan="2" v-else>
            <n-space justify="space-around">
              <n-button block @click="edit = 0">取消</n-button>
              <n-button block @click="commit">提交</n-button>
            </n-space>
          </td>
        </tr>
      </tbody>
    </n-table>
  </n-space>
</template>

<script>
import axios from 'axios';
export default {
  props: {
    id: {
      type: String,
      default: ""
    },
  },
  data() {
    // 获取用户信息
    axios.get("/info/" + this.id).then((re) => {
      this.info = { ...re.data };
      this.info_base = { ...re.data };
    });
    return {
      edit: false,
      info: {
        gender: true,
        city: "",
        hobby: "",
        birthday: "",
        motto: "",
        last_login: 0,
        item_count: 0,
      },
      info_base: {},
    }
  },
  methods: {
    commit() {
      this.edit = false
      let data = { ...this.info }
      // 过滤未变动的信息
      for (const i in data) {
        if (data[i] == this.info_base[i]) {
          delete data[i]
        };
      }
      if (JSON.stringify(data) != "{}") {
        axios.put("/info/", data).catch(() => {
          this.info = this.info_base;
        });
      }
    }
  },
};
</script>