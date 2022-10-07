<template>
  <n-space vertical>
    <!-- 关联信息 -->
    <n-card>
      <n-statistic tabular-nums>
        <n-text> 文章数量 </n-text>
        <n-number-animation show-separator :from="0" :to="Number(data.item_count)" />
      </n-statistic>
    </n-card>
    <!-- 个人信息 -->
    <n-table>
      <tbody>
        <tr>
          <td> 性别 </td>
          <td>
            <n-text v-if="typeof data.gender == 'number'">{{ data.gender }}</n-text>
            <n-text v-else depth="3" underline>未完善</n-text>
          </td>
        </tr>
        <tr>
          <td> 城市 </td>
          <td>
            <n-text v-if="data.city">{{ data.city }}</n-text>
            <n-text v-else depth="3" underline>未完善</n-text>
          </td>
        </tr>
        <tr>
          <td> 爱好 </td>
          <td>
            <n-text v-if="data.hobby">{{ data.hobby }}</n-text>
            <n-text v-else depth="3" underline>未完善</n-text>
          </td>
        </tr>
        <tr>
          <td> 生日 </td>
          <td>
            <n-time v-if="data.birthady" :time="data.birthady.parseInt()" format="yyyy-MM-dd" />
            <n-text v-else depth="3" underline>未完善</n-text>
          </td>
        </tr>
        <tr>
          <td> 活跃 </td>
          <td>
            <n-time :time="Number(data.last_login) || 0" type="relative" />
          </td>
        </tr>
        <tr v-if="$store.state.user.id == data?.id">
          <td colspan="2">
            <n-button block>修改信息</n-button>
          </td>
        </tr>
      </tbody>
    </n-table>
  </n-space>
</template>

<script>
export default {
  props: {
    data: {
      type: Object,
      default: {
        id: "",
        gender: "",
        city: "",
        hobby: "",
        birthady: "",
        last_login: "",
        item_count: "",
      }
    },
  },
  data() {
    return {}
  },
  methods: {
  },
};
</script>