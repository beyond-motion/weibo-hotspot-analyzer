# API 调用失败问题分析

## 🔍 问题摘要

**时间**: 2026-01-30 04:14 (UTC)  
**Workflow**: 微博热搜每日分析  
**Run ID**: 21504150539  
**状态**: ✅ 完成（但所有 AI 分析失败）

## ❌ 错误信息

```
❌ 分析失败: API 响应中未找到有效的 JSON 数据
```

**影响范围**: 所有 10 个热搜话题的 AI 分析都失败

## 🔎 问题分析

### 1. API 调用情况

根据日志显示：
- ✅ API 端点可访问：`https://nwcvxulatwfv.sg-members-1.clawcloudrun.com`
- ✅ 没有 HTTP 错误（401、403、500 等）
- ✅ 环境变量已正确配置（`API_ENDPOINT`, `API_KEY`, `API_MODEL`）
- ❌ **但返回的响应无法解析为有效的 JSON**

### 2. 可能的原因

#### 原因 A：API 返回格式错误（最可能）

Claude 模型返回的内容可能包含：
- 额外的解释文字（在 JSON 之外）
- Markdown 格式的代码块
- 不完整的 JSON 结构

**当前代码的解析逻辑**（`scripts/claude_analysis.py:281-316`）：
```python
def parse_response(self, content: str) -> List[Dict]:
    # 1. 尝试直接解析
    try:
        data = json.loads(content)
        return data.get('ideas', [])
    except json.JSONDecodeError:
        pass
    
    # 2. 尝试提取 JSON 代码块
    json_match = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', content)
    if not json_match:
        json_match = re.search(r'```\s*(\{[\s\S]*?\})\s*```', content)
    if not json_match:
        json_match = re.search(r'\{[\s\S]*"ideas"[\s\S]*\}', content)
    
    # 3. 如果都失败，抛出错误
    if not json_match:
        raise ValueError("API 响应中未找到有效的 JSON 数据")
```

#### 原因 B：API 端点配置问题

可能的配置问题：
- API 端点返回的不是 OpenAI 兼容格式
- `choices[0].message.content` 路径不正确
- API 需要额外的参数

#### 原因 C：模型名称错误

当前使用的模型：`claude-sonnet-4-5`
- 可能 API 不支持这个模型名称
- 需要确认正确的模型名称（如 `claude-3-5-sonnet-20241022`）

#### 原因 D：API 超时或限流

- 虽然没有明确的超时错误
- 但可能返回了空响应或错误页面

## 🛠️ 调试步骤

### 步骤 1：使用调试脚本测试 API

运行提供的调试脚本：

```bash
export API_ENDPOINT="https://nwcvxulatwfv.sg-members-1.clawcloudrun.com/antigravity/v1/chat/completions"
export API_KEY="your_api_key"
export API_MODEL="claude-sonnet-4-5"

python debug_api.py
```

这将显示：
- API 的原始响应
- JSON 解析结果
- 响应结构

### 步骤 2：检查 API 端点配置

访问 API 提供商的文档，确认：
1. 正确的端点 URL
2. 支持的模型名称
3. 请求格式要求
4. 响应格式说明

### 步骤 3：检查 GitHub Secrets

确保以下 Secrets 正确配置：

```
API_ENDPOINT = https://your-api-endpoint.com/v1/chat/completions
API_KEY = your_actual_api_key
API_MODEL = correct_model_name (可选)
```

## 💡 解决方案

### 解决方案 1：改进 JSON 解析逻辑（推荐）

更新 `claude_analysis.py` 的 `parse_response` 方法，增加调试输出和更宽松的解析：

```python
def parse_response(self, content: str) -> List[Dict]:
    """解析 API 响应，提取 JSON 数据"""
    
    # 调试：打印原始响应（前 200 字符）
    print(f"  📥 API 响应预览: {content[:200]}...")
    
    # 1. 尝试直接解析
    try:
        data = json.loads(content)
        if 'ideas' in data:
            return data['ideas']
    except json.JSONDecodeError:
        pass
    
    # 2. 尝试提取 JSON 代码块（支持多种格式）
    patterns = [
        r'```json\s*(\{[\s\S]*?\})\s*```',      # ```json {...} ```
        r'```\s*(\{[\s\S]*?\})\s*```',          # ``` {...} ```
        r'(\{[\s\S]*?"ideas"[\s\S]*?\})',       # 直接查找包含 "ideas" 的 JSON
        r'(\{[^{]*?"ideas"[^}]*?\[[^\]]*?\]\s*\})'  # 更宽松的匹配
    ]
    
    for pattern in patterns:
        json_match = re.search(pattern, content)
        if json_match:
            try:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                if 'ideas' in data:
                    return data['ideas']
            except (json.JSONDecodeError, IndexError):
                continue
    
    # 3. 如果都失败，打印完整响应并抛出错误
    print(f"  📄 完整响应内容:\n{content}")
    raise ValueError("API 响应中未找到有效的 JSON 数据")
```

### 解决方案 2：验证 API 配置

1. 检查 API 端点 URL 是否完整
2. 验证 API Key 是否有效
3. 确认模型名称正确

### 解决方案 3：切换到官方 Anthropic API

如果自定义 API 不稳定，可以切换到官方 API：

```bash
# 在 GitHub Secrets 中配置
ANTHROPIC_API_KEY = sk-ant-xxxxx
```

并使用 `scripts/claude_analysis_anthropic.py`（如果存在）

### 解决方案 4：添加重试机制

在 `call_api` 方法中添加重试逻辑：

```python
def call_api(self, prompt: str, max_retries: int = 3) -> str:
    """调用 API（带重试）"""
    for attempt in range(max_retries):
        try:
            # ... API 调用代码 ...
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️  尝试 {attempt + 1}/{max_retries} 失败，重试中...")
                time.sleep(2)
            else:
                raise
```

## 📊 历史数据

查看最近成功的运行：

| Run ID | 时间 | 状态 | 备注 |
|--------|------|------|------|
| 21482177424 | 18小时前 | ✅ 成功 | 7分40秒 |
| 21465326245 | 1天前 | ✅ 成功 | 7分6秒 |
| 21441919214 | 1天前 | ✅ 成功 | 10分42秒 |
| 21504150539 | 4小时前 | ⚠️  部分失败 | AI 分析失败 |

**观察**: 之前的运行都成功了，说明 API 配置本身是正确的，可能是：
- 临时的 API 故障
- 模型响应格式变化
- API 限流

## 🎯 下一步行动

### 立即执行：

1. **运行调试脚本**：
   ```bash
   python debug_api.py
   ```

2. **查看调试输出**，确定问题根源

3. **根据调试结果**，选择合适的解决方案

### 长期改进：

1. 添加更详细的日志输出
2. 实现重试机制
3. 添加 API 健康检查
4. 设置告警通知（API 失败时发送邮件/Slack 消息）

## 📝 相关文件

- `scripts/claude_analysis.py` - 主要的 AI 分析脚本
- `debug_api.py` - API 调试工具（新创建）
- `.github/workflows/weibo-daily.yml` - GitHub Actions 配置

## 🔗 相关链接

- [GitHub Actions Run](https://github.com/violin86318/weibo-hotspot-analyzer/actions/runs/21504150539)
- [Vercel 部署](https://weibo-hotspot-analyzer-im5y721k3-violin86318s-projects.vercel.app)

---

**最后更新**: 2026-01-30  
**状态**: 🔍 待调试
