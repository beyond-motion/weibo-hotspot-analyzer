# 📦 GitHub Actions 迁移 - 项目文件清单

## 🎯 已创建的文件

### 1. GitHub Actions 配置

**`.github/workflows/weibo-daily.yml`**
- GitHub Actions workflow 配置
- 每天 22:00 (北京时间) 自动执行
- 包含 6 个步骤：检出、设置环境、抓取热搜、Claude 分析、生成报告、提交代码

### 2. 核心脚本

**`scripts/claude_analysis.py`** ⭐ 新增
- 使用 Claude API 分析热搜创意
- 支持批量分析 TOP10 热搜
- 自动生成 3 个创意/热搜
- 输出结构化 JSON 数据

**`scripts/fetch_weibo_hot_v2.py`** ⭐ 升级
- 支持环境变量 `TIANAPI_KEY`
- 改进错误处理
- 自动保存最新文件名标记

**`scripts/generate_html_report_v2.py`** ⭐ 升级
- 适配 Claude 生成的创意数据
- 响应式设计
- 美化的样式和布局
- 支持统计和排行榜

### 3. 配置文件

**`.gitignore`**
- Python 缓存和虚拟环境
- 日志文件
- 临时数据文件
- macOS 系统文件

**`requirements.txt`**
- anthropic >= 0.18.0

### 4. 文档

**`README_GITHUB.md`**
- GitHub 仓库说明文档
- 功能介绍和使用方法
- GitHub Actions 配置说明

**`MIGRATION_GUIDE.md`**
- 详细迁移步骤
- 常见问题解答
- 成本估算

**`QUICKSTART.md`** ⭐ 推荐
- 6 步快速开始指南
- 验证清单
- 相关文档链接

**`migrate_to_github.sh`**
- 自动化迁移脚本
- 一键完成所有准备工作

---

## 🔑 GitHub Secrets 配置清单

### 必需的 Secrets

| Secret 名称 | 说明 | 示例值 | 来源 |
|------------|------|--------|------|
| `TIANAPI_KEY` | 天聚数行 API 密钥 | `<your_tianapi_key>` | [tianapi.com](https://www.tianapi.com/) |
| `ANTHROPIC_API_KEY` | Claude API 密钥 | `sk-ant-xxxxxx...` | [console.anthropic.com](https://console.anthropic.com/) |

### 可选的 Secrets

| Secret 名称 | 说明 | 用途 |
|------------|------|------|
| `SLACK_WEBHOOK` | Slack 通知 Webhook | 发送执行完成通知 |
| `EMAIL_NOTIFICATION` | 邮件地址 | 发送报告到邮箱 |

---

## 📁 目录结构对比

### 原始结构（本地 Skill）

```
.claude/skills/weibo_hotspot_analyzer/
├── scripts/
│   ├── fetch_weibo_hot.py           ← 原版
│   ├── generate_html_report.py      ← 原版
│   └── daily_weibo_analysis.sh      ← 本地定时脚本
├── templates/
├── logs/
├── SKILL.md
└── README.md
```

### 迁移后结构（GitHub 仓库）

```
weibo-hotspot-analyzer/              # 独立 GitHub 仓库
├── .github/
│   └── workflows/
│       └── weibo-daily.yml          ← 新增
├── scripts/
│   ├── fetch_weibo_hot.py           ← v2 版本（支持环境变量）
│   ├── claude_analysis.py           ← 新增
│   └── generate_html_report.py      ← v2 版本（适配 Claude 数据）
├── templates/
├── reports/                         ← 新增（GitHub Actions 生成）
│   └── 2026/01/
│       └── 2026-01-18_weibo_hotspot_report.html
├── .gitignore                       ← 新增
├── requirements.txt                 ← 新增
├── README_GITHUB.md                 ← 新增
├── QUICKSTART.md                    ← 新增
└── MIGRATION_GUIDE.md               ← 新增
```

---

## 🔄 数据流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions 触发                       │
│                 (每天 22:00 或手动触发)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: 抓取微博热搜                                        │
│ - 调用天聚数行 API                                          │
│ - 获取 TOP50 热搜                                           │
│ - 保存为 weibo_hotspots_YYYYMMDD_HHMMSS.json               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Claude AI 分析创意                                  │
│ - 读取热搜数据                                              │
│ - 调用 Claude API (3-5-sonnet)                              │
│ - 为每个热搜生成 3 个创意                                   │
│ - 保存为 weibo_ideas_YYYYMMDD_HHMMSS.json                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 生成 HTML 报告                                      │
│ - 读取创意数据                                              │
│ - 生成响应式 HTML                                           │
│ - 包含概览、详情、排行榜、统计                              │
│ - 保存为 weibo_hotspot_report_YYYYMMDD_HHMMSS.html         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: 提交到 GitHub                                       │
│ - 创建 reports/YYYY/MM/ 目录                                │
│ - 移动 HTML 文件到报告目录                                  │
│ - git commit && git push                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
                    ✅ 完成
              可在 GitHub 上查看报告
```

---

## 💰 成本估算

### 免费额度

| 服务 | 免费额度 | 实际使用 |
|-----|---------|---------|
| GitHub Actions | 2000 分钟/月 | ~30 分钟/月 ✅ |
| 天聚数行 API | 100 次/天 | 1 次/天 ✅ |

### 付费服务

| 服务 | 预计用量 | 月成本 |
|-----|---------|--------|
| Claude API | ~300K tokens/天 | $2-5/月 |
| **总计** | - | **$2-5/月** |

### 节省成本

相比本地运行：
- ✅ 无需服务器费用
- ✅ 无需电费
- ✅ 无需维护
- ✅ 自动备份到 Git

---

## 📊 执行时间统计

| 步骤 | 预计耗时 | 说明 |
|-----|---------|------|
| 环境设置 | ~30s | 安装依赖 |
| 抓取热搜 | ~5s | API 调用 |
| Claude 分析 | ~3-5min | 10个热搜 × ~20s/个 |
| 生成报告 | ~2s | HTML 生成 |
| Git 提交 | ~10s | Push 到仓库 |
| **总计** | **~4-6分钟** | 每天 1 次 |

---

## ✅ 下一步操作

### 方式 A: 使用迁移脚本（推荐）

```bash
cd /Users/wanglingwei/Movies/violinvault/SynologyDrive/Clipping/.claude/skills/weibo_hotspot_analyzer
bash migrate_to_github.sh
```

脚本会自动完成所有准备工作。

### 方式 B: 手动迁移

1. 创建 GitHub 仓库
2. 复制相关文件到新目录
3. 配置 GitHub Secrets
4. 推送代码
5. 测试 Workflow

详细步骤见 `MIGRATION_GUIDE.md`

---

## 🎓 学习资源

### Claude Agent SDK
- 官方文档: https://docs.anthropic.com/
- API 参考: https://docs.anthropic.com/api-reference
- Python SDK: https://github.com/anthropics/anthropic-sdk-python

### GitHub Actions
- 官方文档: https://docs.github.com/en/actions
- Workflow 语法: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- Secrets 管理: https://docs.github.com/en/actions/security-guides/encrypted-secrets

---

## 📞 支持与反馈

如有问题，请：
1. 查看 `MIGRATION_GUIDE.md` 的常见问题部分
2. 检查 GitHub Actions 执行日志
3. 提交 Issue 到 GitHub 仓库

---

**生成时间**: 2026-01-18
**版本**: v1.0.0
**作者**: Claude Code
