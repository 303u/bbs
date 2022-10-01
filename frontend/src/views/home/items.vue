<template>
  <n-space vertical>
    <n-card>
      <!-- 文章标题 -->
      <template #header>{{ data.title }}</template>

      <n-space vertical>
        <!-- 作者与时间 -->
        <n-card>
          <template #header>
            <n-space>
              <PopupCard :id="data.author" />
            </n-space>
          </template>
          <template #header-extra>
            <n-time :time="Number(data.time || 0)" unix />
          </template>
        </n-card>

        <!-- tag标签 -->
        <TagList :data="data.tag || ''" />
      </n-space>
    </n-card>

    <!-- 文章内容 -->
    <n-card>
      <div v-html="marked(data.body || '')"></div>
    </n-card>

    <!-- 评论区 -->
    <n-list bordered>
      <!-- 回复组件 -->
      <template #header>
        <n-space vertical>
          <!-- 如果指定回复目标 -->
          <n-card v-if="c.reply">
            <template #header>
              <n-space>
                <PopupCard :id="c.reply" />
                <n-text type="info" depth="3" underline>
                  @{{ $store.state.user_info[c.reply]?.name }}
                </n-text>
              </n-space>
            </template>
            <template #header-extra>
              <n-button @click="c.reply = ''">取消</n-button>
            </template>
          </n-card>

          <!-- 表单组件 -->
          <n-input clearable show-count type="textarea" maxlength="300" placeholder="添加评论" v-model:value="c.body"
            :autosize="{ minRows: 1, maxRows: 3 }" />
          <n-button @click="create_comment()" block>提交</n-button>
        </n-space>
      </template>
      <!-- 评论详情 -->
      <n-list-item :key="li" v-for="li of comment">
        <n-thing content-indented>

          <!-- 头像 -->
          <template #avatar>
            <n-space vertical>
              <PopupCard :id="li.author" />
              <!-- 作者与自己标识 -->
              <n-popover trigger="hover" v-if="data.author == li.author">
                <template #trigger>
                  <n-button secondary circle type="error">
                    <template #icon>
                      <n-icon>
                        <PersonCircle />
                      </n-icon>
                    </template>
                  </n-button>
                </template>
                <n-text>作者</n-text>
              </n-popover>
              <n-popover trigger="hover" v-else-if="li.author == user.id">
                <template #trigger>
                  <n-button secondary circle type="info">
                    <template #icon>
                      <n-icon>
                        <PersonCircle />
                      </n-icon>
                    </template>
                  </n-button>
                </template>
                <n-text>自己</n-text>
              </n-popover>
            </n-space>
          </template>

          <!-- 名称与信息 -->
          <template #header>
            <n-space>
              <n-ellipsis style="width: 155px" :tooltip="false">
                {{ $store.state.user_info[li.author]?.name }}
              </n-ellipsis>
            </n-space>
          </template>

          <!-- 回复对象 -->
          <template #header-extra v-if="li.reply">
            <PopupCard :id="li.reply" />
          </template>

          <!-- 时间 -->
          <template #description>
            <n-time :time="Number(li.time)" unix />
          </template>

          <!-- 内容 -->
          <n-text> {{ li.body }} </n-text>

          <!-- 操作 -->
          <template #footer>
            <n-space>
              <n-button @click="c.reply = li.author" tertiary> 回复 </n-button>
              <n-button @click="delete_comment(li)" tertiary v-if="li.author == user.id">
                删除
              </n-button>
            </n-space>
          </template>
        </n-thing>
      </n-list-item>
    </n-list>
  </n-space>
  <!-- 快速回到顶部 -->
  <n-back-top :right="50" />
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import { PersonCircle } from "@vicons/ionicons5";
import PopupCard from "@/components/PopupCard.vue";
import TagList from "@/components/TagList.vue";

export default {
  data() {
    axios.get("/i/" + this.$route.params.id).then((req) => {
      this.data = req.data;
      // 加入历史浏览
      this.$store.commit("add_history", req.data);
      axios.get("/t/" + this.$route.params.id).then((req) => {
        // 获取评论
        this.comment = req.data;
      });
    }).catch(() => {
      // 项目不存在则返回页面
      this.$router.back()
    });
    return {
      user: this.$store.state.user,
      c: { body: "", reply: "" },
      marked,
      data: {},
      comment: [],
    };
  },
  methods: {
    create_comment() {
      // 新建评论
      if (0 < this.c.body.length < 301) {
        axios.post("/t/", { ...this.c, item: this.data.id }).then(() => {
          this.reload_comment();
          this.c.body = this.c.reply = "";
        });
      }
    },
    reload_comment() {
      // 加载评论
      axios.get("/t/" + this.data.id).then((req) => {
        this.comment = req.data;
      });
    },
    delete_comment(talk) {
      // 删除评论
      if (talk.author == this.user.id) {
        axios.delete("/t/" + talk.id).then(() => {
          this.reload_comment();
        });
      }
    },
  },
  // 捕捉路由参数变化
  watch: {
    $route() {
      // 如果跳出页面则不执行信息抓取
      if (this.$route.params.id) {
        axios.get("/i/" + this.$route.params.id).then((req) => {
          this.data = req.data;
          // 加入历史浏览
          this.$store.commit("add_history", req.data);
          axios.get("/t/" + this.$route.params.id).then((req) => {
            // 获取评论
            this.comment = req.data;
          });
        }).catch(() => {
          // 项目不存在则返回页面
          this.$router.back()
        });
      }
    }
  },
  components: { PersonCircle, PopupCard, TagList },
};
</script>