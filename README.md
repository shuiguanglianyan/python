# Lightweight CMDB

一个轻量级、可投入生产的小型 DevOps 运维 CMDB：
- FastAPI + SQLite（默认）
- Jinja2 页面 + 简单响应式样式
- 资产、服务、变更记录管理
- 关键词搜索与状态筛选
- Docker 一键启动，开箱即用

## 快速开始（本地）

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问：<http://localhost:8000>

## 一键启动（Docker）

```bash
docker compose up -d --build
```

访问：<http://localhost:8000>

## API 文档

- Swagger UI: `/docs`
- OpenAPI: `/openapi.json`

## 数据模型

- **Assets（资产）**：主机名、IP、环境、系统、负责人、状态、备注
- **Services（服务）**：服务名、所属资产、仓库地址、部署方式、负责人、状态、备注
- **Changes（变更记录）**：标题、关联服务、风险等级、变更窗口、执行人、审批人、状态、回滚计划

## 运行测试

```bash
pytest -q
```

## 生产建议

- 使用外部数据库（PostgreSQL/MySQL），将 `DATABASE_URL` 指向生产库
- 在反向代理（Nginx/Caddy）后运行，启用 HTTPS
- 根据组织需求接入 SSO、RBAC、审计日志与告警系统
