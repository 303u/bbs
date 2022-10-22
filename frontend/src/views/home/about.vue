<template>
  <n-h1 prefix="bar">
    <n-text type="primary"> 关于本站 </n-text>
  </n-h1>

  <n-grid x-gap="12" cols="1 500:2 1000:3" :y-gap="16">
    <n-gi>
      <n-card>
        <template #header> FastAPI </template>
        <template #header-extra>
          <n-button circle @click="open('https://fastapi.tiangolo.com')">
            <template #icon>
              <n-icon><Link /></n-icon>
            </template>
          </n-button>
        </template>
        <n-space>
          <n-tag> 高性能 </n-tag>
          <n-tag> 易于学习 </n-tag>
          <n-tag> 高效编码 </n-tag>
        </n-space>
        <template #footer>
          FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web
          框架。类型注释与依赖注入系统也是框架亮点。
        </template>
      </n-card>
    </n-gi>
    <n-gi>
      <n-card>
        <template #header> SQLAlchemy </template>
        <template #header-extra>
          <n-button circle @click="open('https://www.sqlalchemy.org/')">
            <template #icon>
              <n-icon><Link /></n-icon>
            </template>
          </n-button>
        </template>
        <n-space>
          <n-tag> 灵活 </n-tag>
          <n-tag> 直观 </n-tag>
          <n-tag> 企业级持久性 </n-tag>
        </n-space>
        <template #footer>
          强大的能力改变你对数据库和 SQL 的看法，
          以其对象关系映射器（ORM）而闻名。
        </template>
      </n-card>
    </n-gi>
    <n-gi>
      <n-card>
        <template #header> Naive UI </template>
        <template #header-extra>
          <n-button circle @click="open('https://www.naiveui.com/')">
            <template #icon>
              <n-icon><Link /></n-icon>
            </template>
          </n-button>
        </template>
        <n-space>
          <n-tag> 比较完整 </n-tag>
          <n-tag> 主题可调 </n-tag>
          <n-tag> 速度快 </n-tag>
        </n-space>
        <template #footer>
          一个 Vue 3 组件库，有超过 80 个组件。使用 xicons 作为图标库。使用 MIT
          license 许可证书。
        </template>
      </n-card>
    </n-gi>
  </n-grid>

  <n-h1 prefix="bar">
    <n-text type="info"> 联系方式 </n-text>
  </n-h1>

  <n-list bordered hoverable clickable>
    <n-list-item>
      <n-thing content-indented>
        <template #header>合作邮箱</template>
        <template #header-extra>xxxxxxx@xx.com</template>
      </n-thing>
    </n-list-item>

    <n-list-item>
      <n-thing content-indented>
        <template #header>投诉邮箱</template>
        <template #header-extra>xxxxxxx@xx.com</template>
      </n-thing>
    </n-list-item>

    <n-list-item>
      <n-thing content-indented>
        <template #header>联系电话</template>
        <template #header-extra>xxxxxxxxxxx</template>
      </n-thing>
    </n-list-item>
  </n-list>
</template>

<script>
import { Link } from "@vicons/ionicons5";

export default {
  methods: {
    open(url) {
      window.open(url);
    },
  },
  components: { Link },
};
</script>
