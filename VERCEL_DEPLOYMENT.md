# Vercel 部署指南

## 🌟 为什么选择 Vercel？

相比 GitHub Pages，Vercel 有以下优势：

| 特性 | GitHub Pages | Vercel |
|-----|--------------|--------|
| **私有仓库支持** | ❌ 需要付费 | ✅ 免费支持 |
| **部署速度** | 2-5 分钟 | 10-30 秒 |
| **自定义域名** | ✅ 支持 | ✅ 支持（更简单）|
| **HTTPS** | ✅ 自动 | ✅ 自动 |
| **CDN** | ✅ 全球 | ✅ 全球（更快）|
| **预览部署** | ❌ | ✅ 每个 PR |
| **构建日志** | 有限 | 详细 |

## 🚀 部署步骤

### 1️⃣ 访问 Vercel

打开浏览器，访问：https://vercel.com

### 2️⃣ 使用 GitHub 登录

- 点击 "Sign Up" 或 "Login"
- 选择 "Continue with GitHub"
- 授权 Vercel 访问你的 GitHub 账户

### 3️⃣ 导入项目

1. 点击 "Add New..." → "Project"

2. 在项目列表中找到 `weibo-hotspot-analyzer`
   - 如果没看到，点击 "Adjust GitHub App Permissions" 授权访问

3. 点击 "Import"

### 4️⃣ 配置项目

**Framework Preset**: 选择 `Other`（我们不需要构建）

**Root Directory**: 保持默认 `./`

**Build and Output Settings**:
- Build Command: 留空或 `echo "No build needed"`
- Output Directory: 留空（Vercel 会自动检测 `vercel.json`）
- Install Command: 留空

**Environment Variables**: 不需要（我们用 GitHub Actions 生成报告）

### 5️⃣ 点击 Deploy

等待 10-30 秒，Vercel 会自动部署你的网站！

### 6️⃣ 获取你的网站地址

部署完成后，你会得到一个域名，类似：
```
https://weibo-hotspot-analyzer.vercel.app
```

或者
```
https://weibo-hotspot-analyzer-violin86318.vercel.app
```

## 🔄 自动更新机制

配置好后，**每次 GitHub Actions 运行并推送新报告**，Vercel 会自动：
1. 检测到 git push
2. 触发重新部署
3. 10-30 秒后网站更新

**无需任何额外操作！**

## 🎯 工作流程

```
┌─────────────────────────────────────┐
│  GitHub Actions                     │
│  (每天 10:00 和 22:00)              │
│                                     │
│  1. 抓取微博热搜                    │
│  2. Claude AI 分析                  │
│  3. 生成 HTML 报告                  │
│  4. 提交到 GitHub (reports/)        │
└──────────────┬──────────────────────┘
               │ git push
               ▼
┌─────────────────────────────────────┐
│  Vercel                             │
│  (自动检测 push)                    │
│                                     │
│  1. 拉取最新代码                    │
│  2. 读取 vercel.json                │
│  3. 部署 reports/ 目录              │
│  4. 更新 CDN 缓存                   │
└──────────────┬──────────────────────┘
               │
               ▼
     ✅ 网站自动更新完成
     https://your-site.vercel.app
```

## 🛠️ 高级配置

### 自定义域名

1. 在 Vercel 项目设置中，点击 "Domains"
2. 添加你的域名（如 `weibo.yourdomain.com`）
3. 按照提示配置 DNS 记录：
   ```
   Type: CNAME
   Name: weibo
   Value: cname.vercel-dns.com
   ```

### 环境变量（可选）

如果你想在 Vercel 中运行构建（不推荐，因为我们用 GitHub Actions）：
1. 项目设置 → Environment Variables
2. 添加 `TIANAPI_KEY`, `API_KEY` 等

### 预览部署

每次创建 Pull Request 时，Vercel 会自动创建一个预览链接，可以在合并前查看效果！

## 📊 监控和分析

Vercel 提供详细的分析：
- 访问量统计
- 响应时间
- 错误日志
- 部署历史

访问项目面板查看：https://vercel.com/dashboard

## 🔒 保持仓库私有

Vercel 最大的优势：**即使仓库是 private，网站依然可以公开访问！**

你可以：
1. 将 GitHub 仓库改为 Private
2. API Keys 和代码保持私密
3. 生成的 HTML 报告通过 Vercel 公开分享

## ❌ 禁用 GitHub Pages（可选）

如果你完全迁移到 Vercel，可以：
1. 访问：https://github.com/violin86318/weibo-hotspot-analyzer/settings/pages
2. 取消勾选 GitHub Pages 的启用

## 🆚 对比总结

| 场景 | 推荐方案 |
|-----|---------|
| 仓库是 public，不在意速度 | GitHub Pages |
| 仓库是 private（免费账户）| ✅ **Vercel** |
| 需要快速部署 | ✅ **Vercel** |
| 需要预览部署 | ✅ **Vercel** |
| 需要详细分析 | ✅ **Vercel** |

## 📝 提交代码

配置完成后，提交更改：

```bash
git add .github/workflows/weibo-daily.yml vercel.json VERCEL_DEPLOYMENT.md
git commit -m "🚀 Migrate to Vercel deployment

- Simplified GitHub Actions workflow
- Removed GitHub Pages deployment steps
- Added Vercel configuration
- Added deployment guide

Co-Authored-By: Warp <agent@warp.dev>"
git push
```

## 🎉 完成！

现在你的网站将自动通过 Vercel 部署，无需担心 GitHub Pages 的限制！

---

**最后更新**: 2026-01-30
