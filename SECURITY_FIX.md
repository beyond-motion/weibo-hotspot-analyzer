# 安全修复说明

## 问题描述

在之前的提交中，天聚数行 API 密钥被硬编码在 `scripts/fetch_weibo_hot.py` 文件中：

```python
API_KEY = os.environ.get('TIANAPI_KEY', 'd67242c73185cde1f94039cb55e4a3ee')
```

这个密钥已经暴露在 git 提交历史中（commit `4145ded`），存在安全风险。

## 已完成的修复

✅ **代码修复**
- 移除了硬编码的 API 密钥
- 强制要求从环境变量读取 `TIANAPI_KEY`
- 更新了 `.gitignore`，添加 `.env` 和 `.env.local`
- 创建了 `.env.example` 作为配置模板
- 更新了 README.md 的 API 配置说明

## 后续需要的操作

### 1. 立即更换 API 密钥 🔴

由于旧密钥已经暴露，建议：

1. 登录天聚数行账户：https://www.tianapi.com/
2. 重新生成一个新的 API 密钥
3. 使用新密钥配置本地和 GitHub Secrets

### 2. 清理 Git 历史（可选）⚠️

如果希望从 git 历史中完全移除泄露的密钥，可以使用以下方法：

#### 方法 A：使用 git-filter-repo（推荐）

```bash
# 安装 git-filter-repo
pip install git-filter-repo

# 创建一个包含敏感内容的文件
echo "d67242c73185cde1f94039cb55e4a3ee" > /tmp/secrets.txt

# 从历史中移除
git filter-repo --replace-text /tmp/secrets.txt --force

# 强制推送到远程仓库（谨慎操作）
git push origin --force --all
git push origin --force --tags
```

#### 方法 B：使用 BFG Repo-Cleaner

```bash
# 下载 BFG
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# 创建密钥文件
echo "d67242c73185cde1f94039cb55e4a3ee" > secrets.txt

# 清理历史
java -jar bfg-1.14.0.jar --replace-text secrets.txt .git

# 清理和推送
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

### 3. 更新 GitHub Secrets

在 GitHub 仓库中配置新的 API 密钥：

1. 进入仓库的 Settings → Secrets and variables → Actions
2. 更新或添加以下 Secrets：
   - `TIANAPI_KEY`: 新的天聚数行 API 密钥
   - `API_ENDPOINT`: Claude API 端点
   - `API_KEY`: Claude API 密钥

### 4. 本地开发配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入新的 API 密钥
nano .env
```

## 最佳实践

✅ **正确做法**
- 使用环境变量存储敏感信息
- 将 `.env` 文件添加到 `.gitignore`
- 提供 `.env.example` 作为配置模板
- 在 CI/CD 中使用 Secrets 管理

❌ **错误做法**
- 硬编码 API 密钥到源代码
- 将配置文件提交到 git
- 在公开渠道分享密钥
- 使用默认密钥值

## 监控和检测

### 定期检查代码

```bash
# 检查是否有敏感信息泄露
git grep -i "api[_-]key\|secret\|password\|token"

# 检查环境变量使用
git grep "os.environ.get"
```

### 使用自动化工具

- [git-secrets](https://github.com/awslabs/git-secrets): 防止提交敏感信息
- [truffleHog](https://github.com/trufflesecurity/truffleHog): 扫描 git 历史中的密钥
- [detect-secrets](https://github.com/Yelp/detect-secrets): 预提交钩子检测

## 联系方式

如有安全问题，请通过以下方式报告：
- GitHub Issues（非敏感信息）
- 私密联系项目维护者（敏感漏洞）

---

**最后更新**: 2026-01-30
