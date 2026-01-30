# REFERENCE_API.md - API接口与模板规范

本文档包含微博热搜API接口说明、HTML报告模板规范、评分标准详解。

---

## 微博热搜API接口

### 接口基本信息

| 项目 | 内容 |
|------|------|
| **接口名称** | 微博热搜榜API |
| **服务提供商** | 天聚数行TianAPI |
| **接口地址** | `https://apis.tianapi.com/weibohot/index` |
| **请求方式** | GET/POST |
| **返回格式** | UTF-8 JSON |
| **更新频率** | 每30分钟 |
| **数据范围** | TOP50热搜话题 |

### 请求参数

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|---------|------|
| `key` | string | ✅ 是 | API密钥（注册后获得） |

**请求示例**：
```
https://apis.tianapi.com/weibohot/index?key=<your_api_key>
```

### 返回参数

#### 公共参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `code` | int | 状态码（200=成功） |
| `msg` | string | 错误信息 |
| `result` | object | 返回结果集 |

#### 应用参数（result数组内）

| 参数名 | 类型 | 示例值 | 说明 |
|--------|------|--------|------|
| `hotword` | string | "失踪女童确认曾在漳州出现" | 热搜话题 |
| `hotwordnum` | string | "129940" | 热搜指数 |
| `hottag` | string | "热" | 热搜标签（热/新/爆等） |

### 返回示例

```json
{
  "code": 200,
  "msg": "success",
  "result": [
    {
      "hotword": "失踪女童确认曾在漳州出现",
      "hotwordnum": "129940",
      "hottag": "热"
    },
    {
      "hotword": "春节档电影票房破百亿",
      "hotwordnum": "256780",
      "hottag": "爆"
    }
  ]
}
```

### 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 200 | 成功 | - |
| 230 | key错误或为空 | 检查API密钥是否正确 |
| 150 | 可用次数不足 | 等待次日重置或升级会员 |
| 130 | 调用频率超限 | 降低请求频率 |
| 250 | 数据返回为空 | 稍后重试或检查API状态 |

### 调用限制

| 会员等级 | 每日调用量 | QPS限制 | 价格 |
|---------|-----------|---------|------|
| 普通会员 | 100次 | 5-10 | 免费 |
| 高级会员 | 10,000次 | 20 | ¥20/月 |
| 黄金会员 | 500,000次 | 30 | ¥65/月 |
| 钻石会员 | 不限次 | 60 | ¥1690/年 |

### 热搜链接格式

单个热搜的微博搜索链接：
```
https://s.weibo.com/weibo?q=<热搜词URL编码>
```

例如：`https://s.weibo.com/weibo?q=%E5%A4%B1%E8%B8%AA%E5%A5%B3%E7%AB%A5`

---

## HTML报告模板规范

### 文件结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析报告</title>
    <style>/* CSS样式 */</style>
</head>
<body>
    <div class="container">
        <!-- 报告内容 -->
    </div>
    <script>/* JavaScript逻辑 */</script>
</body>
</html>
```

### 配色方案（活力橙主题）

| 用途 | 颜色代码 | CSS变量 |
|------|---------|---------|
| **主色（活力橙）** | `#FF6B35` | `--primary-color` |
| **辅助色** | `#FF8C42` | `--secondary-color` |
| **强调色（优秀）** | `#FFD23F` | `--accent-excellent` |
| **良好色** | `#06A77D` | `--accent-good` |
| **背景色** | `#FFF8F0` | `--bg-color` |
| **文字色** | `#2D3142` | `--text-color` |
| **卡片背景** | `#FFFFFF` | `--card-bg` |

### 排版规范

#### 字体大小

- **标题（h1）**：28px（手机）/ 36px（桌面）
- **副标题（h2）**：22px（手机）/ 28px（桌面）
- **小标题（h3）**：18px（手机）/ 20px（桌面）
- **正文**：14px（手机）/ 16px（桌面）
- **小字**：12px

#### 间距规范

- **页面边距**：16px（手机）/ 40px（桌面）
- **卡片间距**：16px（手机）/ 24px（桌面）
- **元素内边距**：12px（手机）/ 16px（桌面）
- **章节间距**：32px（手机）/ 48px（桌面）

### 响应式断点

```css
/* 手机 */
@media (max-width: 768px) { }

/* 平板 */
@media (min-width: 769px) and (max-width: 1024px) { }

/* 桌面 */
@media (min-width: 1025px) { }
```

### 内容区域规范

#### 1. 报告头部

```html
<header class="report-header">
    <h1>微博热搜产品创意分析报告</h1>
    <div class="meta-info">
        <span class="date">生成日期：2025-01-04</span>
        <span class="count">热搜总数：50</span>
        <span class="duration">分析耗时：15分钟</span>
    </div>
</header>
```

#### 2. 热搜概览（TOP10）

```html
<section class="hotspot-overview">
    <h2>📊 热搜TOP10概览</h2>
    <div class="hotspot-list">
        <!-- 10个热搜卡片，每个包含：排名、热搜词、热度、标签 -->
    </div>
</section>
```

#### 3. 详细分析（每个热搜）

```html
<section class="hotspot-detail">
    <div class="hotspot-header">
        <span class="rank">#1</span>
        <h3 class="hotword">春节档电影票房破百亿</h3>
        <span class="hotness">热度：256,780</span>
        <span class="tag">爆</span>
    </div>

    <div class="event-timeline">
        <h4>📅 事件脉络</h4>
        <ul class="timeline">
            <li><strong>2025-01-01</strong>：春节档电影开始预售</li>
            <li><strong>2025-01-03</strong>：多部影片票房破10亿</li>
            <li><strong>2025-01-04</strong>：总票房突破100亿</li>
        </ul>
    </div>

    <div class="product-ideas">
        <h4>💡 产品创意</h4>
        <div class="idea-card excellent"> <!-- 优秀创意 -->
            <div class="idea-header">
                <span class="idea-name">🎬 影票拼团小程序</span>
                <span class="score">92分 <span class="badge excellent">优秀</span></span>
            </div>
            <div class="idea-body">
                <p><strong>核心功能：</strong></p>
                <ul>
                    <li>多人拼团购票优惠（3-10人团）</li>
                    <li>智能推荐热门场次和座位</li>
                    <li>影后评分和讨论区</li>
                    <li>会员积分兑换爆米花套餐</li>
                </ul>
                <p><strong>目标用户：</strong></p>
                <p>18-35岁年轻观影群体，喜欢社交分享，对价格敏感但追求体验。</p>
            </div>
        </div>

        <div class="idea-card good"> <!-- 良好创意 -->
            <!-- 创意内容 -->
        </div>
    </div>
</section>
```

#### 4. 创意排行榜

```html
<section class="idea-ranking">
    <h2>🏆 产品创意排行榜</h2>
    <div class="ranking-list">
        <!-- 所有创意按评分降序展示 -->
    </div>
</section>
```

#### 5. 数据统计

```html
<section class="statistics">
    <h2>📈 数据统计</h2>
    <div class="stat-grid">
        <div class="stat-item">
            <span class="stat-value">150</span>
            <span class="stat-label">创意总数</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">45</span>
            <span class="stat-label">优秀创意（>80分）</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">78.5</span>
            <span class="stat-label">平均评分</span>
        </div>
    </div>
</section>
```

### 交互功能

#### 搜索过滤

```javascript
// 实时搜索功能
function filterHotspots(keyword) {
    // 根据关键词过滤热搜
}
```

#### 排序功能

```javascript
// 按热度/评分排序
function sortBy(criteria) {
    // 'hotness' 或 'score'
}
```

#### 折叠展开

```javascript
// 长列表自动折叠
function toggleDetail(id) {
    // 展开/收起详情
}
```

---

## 评分标准详解

### 评分公式

```
综合评分 = 有趣度 × 0.8 + 有用度 × 0.2
```

### 有趣度评分标准（80分权重）

| 维度 | 评分点 | 分值范围 |
|------|--------|---------|
| **创意新颖性** | 是否有创新点、差异化 | 0-25分 |
| **话题热度** | 当前社交媒体讨论量 | 0-25分 |
| **用户参与度** | 互动性、UGC潜力 | 0-20分 |
| **传播潜力** | 病毒式传播可能性 | 0-30分 |

**有趣度总分**：0-100分

#### 评分示例

- **25-30分（传播潜力）**：具备强社交属性，易于二次创作
- **20-25分（创意新颖性）**：有独特切入点，非传统产品形态
- **18-20分（用户参与度）**：高频互动，用户可贡献内容
- **20-25分（话题热度）**：热搜榜前列，讨论量>100万

### 有用度评分标准（20分权重）

| 维度 | 评分点 | 分值范围 |
|------|--------|---------|
| **实用价值** | 解决实际问题的程度 | 0-8分 |
| **需求强度** | 用户刚需程度 | 0-7分 |
| **市场痛点** | 解决现有产品不足 | 0-5分 |

**有用度总分**：0-20分

#### 评分示例

- **6-8分（实用价值）**：直接解决用户痛点，高频使用场景
- **5-7分（需求强度）**：强需求，用户愿意付费
- **4-5分（市场痛点）**：填补市场空白，优于现有方案

### 等级划分

| 等级 | 分数范围 | 标识颜色 | 说明 |
|------|---------|---------|------|
| **优秀** | >80分 | 金黄色 | 高有趣度+高实用价值，优先推荐 |
| **良好** | 60-80分 | 绿色 | 有潜力，可考虑开发 |
| **普通** | <60分 | 灰色 | 需要优化或暂缓 |

### 评分注意事项

1. **权重偏向**：有趣度占80%，因为热点产品依赖话题性和传播力
2. **动态调整**：评分基于当前信息，后续可能调整
3. **主观性**：AI评分有主观性，仅作参考
4. **市场验证**：高分创意需进一步市场验证

---

## Web Search使用规范

### 搜索关键词格式

```javascript
// 基础搜索
`"${hotword}" 事件 背景`

// 时间限定
`"${hotword}" 最新进展 2025`

// 多维度搜索
`"${hotword}" 影响分析 用户讨论`
```

### 搜索结果筛选

- 优先选择权威新闻源（新华社、人民日报等）
- 关注事件时间线信息
- 收集用户评论和讨论热点
- 提取关键数据（时间、地点、涉及主体）

### 搜索频率控制

- 每个热搜搜索3-5次
- 避免重复搜索相同内容
- 控制总体搜索次数（节省token）

---

## 开发调试建议

### 本地测试

```bash
# 测试API调用
python scripts/fetch_weibo_hot.py

# 验证HTML渲染
# 直接在浏览器打开生成的HTML文件
```

### 常见问题

1. **中文乱码**：确保文件保存为UTF-8编码
2. **样式错乱**：检查CSS是否完整加载
3. **脚本错误**：查看浏览器控制台错误信息
4. **数据为空**：验证API返回的数据格式

### 优化建议

1. **性能优化**：使用虚拟滚动处理长列表
2. **离线访问**：考虑使用Service Worker
3. **数据缓存**：避免重复调用API
4. **移动端优化**：减少动画效果，提升加载速度
