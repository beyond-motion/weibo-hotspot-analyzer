# GitHub Pages 配置指南

## 问题诊断

如果你的 GitHub Pages 显示 404 错误，可能的原因：

1. ❌ **仓库是私有的**（免费账户不支持）
2. ❌ **GitHub Pages 未启用**
3. ❌ **Pages 构建失败**
4. ❌ **DNS/CNAME 配置错误**

## ✅ 解决步骤

### 第一步：确认仓库可见性

- **免费账户**：仓库必须是 **Public**
- **付费账户**（GitHub Pro+）：可以使用 Private 仓库

检查方式：
```bash
gh repo view --json isPrivate
```

如果是 `"isPrivate": true` 且你是免费账户，需要将仓库改为 Public：
1. Settings → 滚动到底部 "Danger Zone"
2. Change visibility → Change to public

### 第二步：启用 GitHub Pages

1. 访问：https://github.com/violin86318/weibo-hotspot-analyzer/settings/pages

2. 在 "Build and deployment" 部分：
   - **Source**: 选择 `GitHub Actions`（重要！）
   - 不要选择 "Deploy from a branch"

3. 点击保存

### 第三步：验证 Pages 配置

检查 Pages 是否已启用：
```bash
gh api repos/violin86318/weibo-hotspot-analyzer/pages
```

成功响应示例：
```json
{
  "url": "https://violin86318.github.io/weibo-hotspot-analyzer/",
  "status": "built",
  "html_url": "https://violin86318.github.io/weibo-hotspot-analyzer/"
}
```

### 第四步：手动触发 Workflow

```bash
gh workflow run weibo-daily.yml
```

或者在 GitHub 网页上：
1. Actions 标签页
2. 左侧选择 "微博热搜每日分析"
3. 右侧点击 "Run workflow"

### 第五步：检查部署状态

```bash
# 查看最近的运行
gh run list --workflow="weibo-daily.yml" --limit 5

# 查看特定运行的日志
gh run view <RUN_ID> --log
```

确保两个 job 都成功：
- ✅ `weibo-analysis` - 生成报告
- ✅ `deploy` - 部署到 Pages

## 🌐 访问你的网站

配置成功后，你的网站将在以下地址可用：

**主域名**：https://violin86318.github.io/weibo-hotspot-analyzer/

**自定义域名**（可选）：
如果你配置了 CNAME（如 `weibo.violin86318.github.io`），确保：
1. CNAME 文件存在于部署的 pages 目录
2. DNS 记录正确配置

## 📋 快速检查清单

- [ ] 仓库是 Public（或有 GitHub Pro）
- [ ] Settings → Pages 中 Source 设置为 "GitHub Actions"
- [ ] Workflow 至少成功运行过一次
- [ ] `deploy` job 显示成功
- [ ] 等待 2-5 分钟让 Pages 完成部署

## 🔧 常见问题

### 问题 1：404 Not Found

**可能原因**：
- Pages 未启用
- 部署失败
- 文件路径不正确

**解决**：
1. 检查 Actions 标签页是否有错误
2. 确认 `pages` 目录包含 `index.html`
3. 重新运行 workflow

### 问题 2：自定义域名不工作

**解决**：
1. 确保 CNAME 文件存在
2. 检查 DNS 记录：`dig weibo.violin86318.github.io`
3. 等待 DNS 传播（最多 24 小时）

### 问题 3：仓库是私有的

**选项 A**：改为 Public（免费）
**选项 B**：升级到 GitHub Pro（$4/月）
**选项 C**：使用 Vercel 托管（免费，支持私有仓库）

## 📊 Workflow 执行时间

- **定时执行**：
  - 北京时间 10:00 (UTC 02:00)
  - 北京时间 22:00 (UTC 14:00)

- **手动触发**：随时可以在 Actions 页面点击 "Run workflow"

## 🆘 需要帮助？

如果问题仍未解决，检查：

```bash
# 查看最新的 workflow 日志
gh run view --log

# 检查 Pages 部署状态
gh api repos/violin86318/weibo-hotspot-analyzer/pages/builds/latest
```

---

**最后更新**: 2026-01-30
