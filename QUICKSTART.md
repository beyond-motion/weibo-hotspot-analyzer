# 🚀 GitHub Actions 迁移 - 快速开始

## 📋 前置准备

### 1️⃣ 运行迁移脚本

```bash
cd /Users/wanglingwei/Movies/violinvault/SynologyDrive/Clipping/.claude/skills/weibo_hotspot_analyzer
bash migrate_to_github.sh
```

脚本会：
- ✅ 复制项目到 `/tmp/weibo-hotspot-analyzer`
- ✅ 更新脚本文件到 v2 版本
- ✅ 创建 GitHub Actions 配置
- ✅ 初始化 Git 仓库
- ✅ 生成迁移指南

### 2️⃣ 创建 GitHub 仓库

访问 https://github.com/new 创建新仓库：
- **仓库名**: `weibo-hotspot-analyzer`
- **可见性**: Public 或 Private
- **不要**初始化 README（因为我们已有代码）

### 3️⃣ 配置 GitHub Secrets

在新建的仓库中配置 Secrets：

**路径**: Settings → Secrets and variables → Actions → New repository secret

#### Secret 1: TIANAPI_KEY

```
名称: TIANAPI_KEY
值: <你的天聚数行 API 密钥>
```

⚠️ **安全提示**：使用你自己的 API 密钥，不要使用示例中的密钥。
获取地址：https://www.tianapi.com/

#### Secret 2: ANTHROPIC_API_KEY

```
名称: ANTHROPIC_API_KEY
值: sk-ant-xxxxxx...
```

获取 Claude API Key: https://console.anthropic.com/

### 4️⃣ 推送代码到 GitHub

```bash
# 进入迁移后的目录
cd /tmp/weibo-hotspot-analyzer

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer.git

# 提交所有文件
git add .
git commit -m "Initial commit: 微博热搜分析器 with GitHub Actions"

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 5️⃣ 测试 Workflow

1. 访问 Actions 页面：
   ```
   https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer/actions
   ```

2. 点击左侧的 **weibo-daily** workflow

3. 点击右侧的 **Run workflow** 按钮

4. 选择分支，点击绿色的 **Run workflow** 确认

5. 等待执行完成，查看日志

### 6️⃣ 查看生成的报告

成功后，在仓库的 **reports** 目录查看报告：

```
reports/2026/01/2026-01-18_weibo_hotspot_report.html
```

可以直接在 GitHub 上预览 HTML 文件！

---

## 🔧 手动配置（可选）

如果你想手动创建文件而不是使用迁移脚本：

### 文件清单

| 文件路径 | 说明 |
|---------|------|
| `.github/workflows/weibo-daily.yml` | GitHub Actions 配置 |
| `scripts/claude_analysis.py` | Claude AI 分析脚本 |
| `scripts/fetch_weibo_hot_v2.py` | 热搜抓取脚本 v2 |
| `scripts/generate_html_report_v2.py` | 报告生成脚本 v2 |
| `.gitignore` | Git 忽略规则 |
| `requirements.txt` | Python 依赖 |
| `README_GITHUB.md` | GitHub 仓库说明 |
| `MIGRATION_GUIDE.md` | 详细迁移指南 |

### 文件结构

```
weibo-hotspot-analyzer/
├── .github/
│   └── workflows/
│       └── weibo-daily.yml          ← GitHub Actions 配置
├── scripts/
│   ├── fetch_weibo_hot.py           ← 使用 v2 版本
│   ├── claude_analysis.py           ← 新增
│   └── generate_html_report.py      ← 使用 v2 版本
├── reports/                         ← GitHub Actions 自动生成
│   └── 2026/01/
├── templates/
│   └── report_template.html
├── .gitignore
├── requirements.txt
├── README_GITHUB.md
└── MIGRATION_GUIDE.md
```

---

## 📊 执行时间说明

**默认配置**: 每天北京时间 22:00 自动执行

修改执行时间，编辑 `.github/workflows/weibo-daily.yml`:

```yaml
schedule:
  # 每天 UTC 14:00 (北京时间 22:00)
  - cron: '0 14 * * *'

  # 其他示例：
  # - cron: '0 6 * * *'   # 北京时间 14:00
  # - cron: '0 2 * * *'   # 北京时间 10:00
  # - cron: '0 */6 * * *' # 每6小时一次
```

Cron 格式：`分 时 日 月 周`

---

## ✅ 验证清单

迁移完成后，检查以下项目：

- [ ] GitHub 仓库已创建
- [ ] 代码已推送到 GitHub
- [ ] TIANAPI_KEY 已配置
- [ ] ANTHROPIC_API_KEY 已配置
- [ ] Workflow 手动执行成功
- [ ] 报告已生成到 reports 目录
- [ ] 可以在 GitHub 上预览 HTML 报告

---

## 🎉 完成！

现在你的微博热搜分析器已经完全自动化了！

每天 22:00，GitHub Actions 会自动：
1. 抓取微博热搜数据
2. 调用 Claude 分析创意
3. 生成 HTML 报告
4. 提交到 Git 仓库

你可以随时访问 GitHub 仓库查看最新报告！

---

## 📝 相关文档

- [详细迁移指南](MIGRATION_GUIDE.md)
- [GitHub 仓库说明](README_GITHUB.md)
- [Claude API 文档](https://docs.anthropic.com/)
- [天聚数行 API 文档](https://www.tianapi.com/)

---

**生成时间**: 2026-01-18
**版本**: v1.0.0
