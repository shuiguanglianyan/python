# devops-cmdb

一个可直接落地的 DevOps CMDB 示例项目，包含资产、服务、变更三大核心域，提供 Web 管理页面 + OpenAPI。

## 功能特性

- 资产管理：新增、删除、搜索、状态筛选。
- 服务管理：关联资产，追踪仓库与部署方式。
- 变更管理：记录风险等级、变更窗口、执行人与回滚计划。
- 总览看板：资产数、服务数、待处理变更数。
- API 接口：支持列表/更新/删除与总览统计。
- Docker 一键启动。

## 技术栈

- FastAPI
- SQLAlchemy 2.0
- Jinja2
- SQLite（可通过 `DATABASE_URL` 切换到 PostgreSQL/MySQL）

## 启动方式

### 本地

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问：<http://localhost:8000>

默认登录：`admin / admin`

### Docker

```bash
docker compose up -d --build
```

## API 文档

- Swagger: `/docs`
- OpenAPI: `/openapi.json`

## 目录结构

```text
app/
  main.py             # 路由与业务逻辑
  db.py               # 数据库连接
  models.py           # ORM 模型
  schemas.py          # Pydantic 数据模型
  templates/          # Jinja2 页面
  static/             # 样式资源
tests/
  test_app.py
```

## 测试

```bash
pytest -q
```

## 生产建议

- 使用 PostgreSQL + Alembic 做迁移管理。
- 接入企业 SSO（OIDC/SAML）替换默认账号。
- 在网关层启用 HTTPS、WAF、审计与限流。
- 增加 RBAC、多租户、审计日志与告警闭环。


## 额外工程：课程签到微信小程序

已新增可直接运行的小程序工程：`wechat-miniapp-signin/`，支持钢琴课与古筝课签到。

快速开始：

```bash
# 用微信开发者工具导入目录
wechat-miniapp-signin
```

详细说明见：`wechat-miniapp-signin/README.md`。
