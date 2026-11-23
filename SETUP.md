# 情侣出行决策 Agent — 搭建与上线手册

本项目根据《EdgeOne Makers - WorkBuddy 智能体搭建手册》把 OpenAI Agents Starter(Python) 改造成一个**可查询附近商场、结合品牌偏好生成推荐的在线 Agent**，并部署上线。

代码部分（Agent 工具、系统指令、前端文案、部署工作流）已全部改好。下面 5 件事需要**你本人**完成——AI 可以帮你改代码，但无法替你持有真实密钥、授权账号或点击控制台。

---

## 一、Fork 仓库 + EdgeOne Makers 授权 GitHub

> ⚠️ 当前项目代码是从公开模板 fork 拉取到本地的，`git remote origin` 指向的是别人的仓库（你**没有** push 权限）。开始部署前，务必先把 origin 改成你自己的仓库，否则第六步 `git push` 会失败。

```bash
# 1) 在 GitHub 网页上新建一个空仓库，例如 love-travel-agent
# 2) 在项目目录执行，把 origin 换成你自己的仓库地址
git remote set-url origin https://github.com/<你的用户名>/love-travel-agent.git
git remote -v    # 确认已指向你自己的仓库
```

1. 登录 GitHub，Fork 本仓库到你自己的账号（或把当前项目 `git push` 到一个你自己的新仓库）。
2. 打开 [EdgeOne Makers 控制台](https://console.cloud.tencent.com/edgeone/makers)，用腾讯云账号登录并开通 Makers。
3. 进入 **服务总览 → 代码仓库授权**，点击「授权 GitHub」，完成授权。
4. 点击「立即创建」创建 Agent 项目，配置建议如下：
   - 项目名称：`love-travel-agent`
   - 运行环境：Python 3.11
   - 仓库来源：从 GitHub 仓库，选择你刚才 Fork 的仓库
   - 加速区域：全球可用区（含中国大陆）
5. 创建完成后，进入项目概览页，记下预览地址。

---

## 二、申请三个密钥（Key / Token）

### 1. AI 网关 Key（模型调用）
1. Makers 控制台 → **Models → API Key** → 新建 Key。
2. 复制生成的 Key，记为 `AI_GATEWAY_API_KEY`。
3. Base URL 固定为 `https://ai-gateway.edgeone.link/v1`，模型默认 `@makers/deepseek-v4-flash`（内置免费额度，新用户可按官方活动页领 50 万 Token）。
   > 邀请码活动（可选）：官方活动页「点亮 star & 邀请码」，按页面提示操作领取免费额度。

### 2. 高德地图 Key（Web 服务）
1. 打开 [高德开放平台控制台](https://console.amap.com/dev/key/app)。
2. 创建应用 → 添加 Key，**服务平台务必选择「Web服务」**（不是 Web端/JS）。
3. 复制 Key，记为 `AMAP_API_KEY`。
   > 注意：Web 服务 Key 与 JS Key 不通用，这里必须用 Web 服务类型，否则地图接口会报 `INVALID_USER_KEY`。

### 3. EdgeOne API Token（自动部署）
1. Makers 控制台 → **API Token** → 创建 API Token（描述随意，如 `github-actions`）。
2. 复制 Token，记为 `EDGEONE_API_TOKEN`。
3. GitHub 仓库 → **Settings → Secrets and variables → Actions → New repository secret**：
   - Name: `EDGEONE_API_TOKEN`
   - Secret: 粘贴上一步的 Token
   - 保存。

> **安全提醒**：任何 Key / Token 都不要写进前端代码或提交到仓库；分享截图时请打码。本地 `.env` 已加入 `.gitignore`，不会被提交。

---

## 三、配置环境变量

### 本地开发（`.env`）
在项目根目录创建 `.env`（可复制 `.env.example`），填入：

```ini
AI_GATEWAY_API_KEY=你的AI网关Key
AI_GATEWAY_BASE_URL=https://ai-gateway.edgeone.link/v1
AI_GATEWAY_MODEL=@makers/deepseek-v4-flash
AMAP_API_KEY=你的高德Web服务Key
```

### 线上运行（EdgeOne Makers 控制台）
Makers 控制台 → 你的项目 → **环境变量 / Settings**，添加同样四个变量（变量名一致），值填真实密钥。线上环境变量与本地 `.env` 是两处独立配置，都需要填。

---

## 四、本地体验

前置依赖：Node.js ≥ 18、Python ≥ 3.10、EdgeOne CLI。

```bash
npm install
pip install -r requirements.txt
# 已按上面第三节配置好 .env
npm i -g edgeone
edgeone makers dev
```

浏览器打开 `http://localhost:8080`，可以试着输入手册里的示例：

> 我在红莲南路地铁站附近，想找既有倍轻松又有西厅村屋的近一点的商场，帮我推荐。

观察工具指示灯是否依次亮起：地点解析 → 关键词搜索 / 附近商场 → 距离计算。

---

## 五、Push 触发部署 + 新建部署上线

```bash
git add .
git commit -m "feat: 情侣出行决策 Agent - 接入高德地图"
git push origin main
```

push 到 `main` 后，`/.github/workflows/deploy.yml` 会自动触发构建部署（依赖第二节配置的 `EDGEONE_API_TOKEN` Secret）。

回到 Makers 控制台 → **部署管理**，可看到自动部署状态；如需手动重建，点击「新建部署」→ 确认。

部署成功后：
- 用临时预览链接做最终验证（默认域名链接有时效限制）；
- 需要正式对外提供服务时，在「域名管理」添加自定义域名。

---

## 常见问题

| 现象 | 原因 / 处理 |
|------|-------------|
| 地图工具返回 `INVALID_USER_KEY` | 高德 Key 类型不对，必须用「Web服务」Key |
| 地图工具返回 `AMAP_API_KEY 未配置` | 本地 `.env` 或线上环境变量没填 `AMAP_API_KEY` |
| 模型报鉴权错误 | `AI_GATEWAY_API_KEY` 填错或未在 Makers Models 创建 |
| 自动部署没触发 | GitHub Secrets 里没配 `EDGEONE_API_TOKEN`，或 push 的不是 `main` 分支 |
| 前端工具灯不亮 | 工具调用名与 `src/App.tsx` 的 `LAMP_IDS` 不一致（本项目已对齐） |
