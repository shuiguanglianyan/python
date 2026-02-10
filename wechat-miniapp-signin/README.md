# 课程签到微信小程序（钢琴课 / 古筝课）

这是一个可直接在微信开发者工具运行的小程序工程。

## 功能

- 课程签到（钢琴课、古筝课）
- 学员姓名 + 备注登记
- 本地签到记录查看与清空
- 操作人信息设置
- 预留远程同步接口（可选）

## 你只需要改的配置

编辑根目录 `config.js`：

```js
module.exports = {
  WECHAT_SCHEDULER_KEY: 'PLEASE_REPLACE_WITH_YOUR_KEY',
  API_BASE_URL: 'https://example.com/api',
  USE_REMOTE_API: false
};
```

- `WECHAT_SCHEDULER_KEY`：改成你的微信调度/服务鉴权 key
- `API_BASE_URL`：你的后端地址（可选）
- `USE_REMOTE_API`：
  - `false`：只走本地存储（开箱即用）
  - `true`：签到后调用远程接口 `/attendance/sign-in`

## 运行步骤

1. 打开微信开发者工具。
2. 导入目录：`wechat-miniapp-signin`。
3. 填你自己的 AppID（或先用测试号）。
4. 编译运行。

## 目录结构

```text
wechat-miniapp-signin/
  app.js
  app.json
  app.wxss
  config.js
  pages/
    home/      # 签到页
    records/   # 记录页
    settings/  # 设置页
  utils/
    storage.js
    request.js
    date.js
```
