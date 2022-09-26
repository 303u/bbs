# bbs-server

## docker部署

1. 编译前端静态文件

`.gitignore` 文件配置了忽略文件夹 `/dist`，
若直接github下载压缩包则需要更多细节调整。

2. 配置环境变量

`.gitignore` 置了忽略 `.env` 文件防止泄露密码到github，
`docker-compose.yml` 指向了两个 .env 文件。

3. 运行

```bash
docker compose up -d
```

## 后端

- 路径 `backend`

需要配置邮箱才能使用验证码功能。

- `.env` 文件配置

| 健        | 值             |
| --------- | -------------- |
| title     | 服务器名称     |
| version   | 服务器版本     |
| emailh    | 邮箱服务器地址 |
| emailu    | 邮箱OP3账号    |
| emailp    | 邮箱OP3对接码  |
| emailp    | 邮箱OP3对接码  |
| alchemy   | ORM的对接方式  |
| key       | 加密盐         |
| digestmod | 加密模式       |

查看 alchemy 配置的写法：
https://docs.sqlalchemy.org/en/14/core/engines.html

简单配置 `alchemy=sqlite://` 不创建数据库可用于本地测试。

> - ### 调试操作：
1. 安装依赖

```bash
pip install -r requirement.txt
```

2. 配置环境变量

3. 直接运行 `dev.py`

4. `ctrl + c` 停止服务器

## 前端

- 路径 `frontend`

| 命令          | 效果 |
| ------------- | ---- |
| npm install   | 安装 |
| npm run build | 编译 |
| npm run serve | 调试 |

- `nginx.conf` 文件

覆盖默认 nginx 配置文件。

## 数据

- 路径 `ops`

引用了 **MySQL8.0**, 可调整实际使用数据库。

`/var/lib/mysql` 为容器中的 MySQL 数据位置。

`/docker-entrypoint-initdb.d/` 启动时默认执行容器中的 .sql .sh 文件

- `.env` 文件配置

| 健                  | 值               |
| ------------------- | ---------------- |
| MYSQL_ROOT_PASSWORD | 默认root用户密码 |
| MYSQL_DATABASE      | 数据库名         |
| MYSQL_USER          | 自定义用户       |
| MYSQL_PASSWORD      | 自定义用户密码   |

自定义用户权限只能访问环境变量定义的数据库。