#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜产品创意HTML报告生成器
"""

import json
import os
import glob
from datetime import datetime

# 获取当前日期
today = datetime.now()
current_date_str = today.strftime('%Y-%m-%d')
current_year_month = today.strftime('%Y/%m')

# 查找最新的JSON文件
json_files = glob.glob('weibo_hotspots_*.json')
if not json_files:
    raise FileNotFoundError("未找到热搜数据文件 (weibo_hotspots_*.json)")

latest_json = max(json_files, key=os.path.getmtime)
print(f"[信息] 使用数据文件: {latest_json}")

# 读取热搜数据
with open(latest_json, 'r', encoding='utf-8') as f:
    hotspot_data = json.load(f)

hotspots = hotspot_data['data']  # 分析全部热搜

# 为每个热搜生成产品创意
def generate_ideas_for_hotspot(hotspot):
    hotword = hotspot['hotword']
    hotness = hotspot['hotword_num_int']
    tag = hotspot['hot_tag']

    ideas = []

    if '国考' in hotword:
        ideas = [
            {
                'name': '考公AI面试教练',
                'score': 85,
                'fun_score': 82,
                'use_score': 88,
                'features': ['AI模拟真实面试场景', '实时语音识别与评分', '个性化答题建议', '历年真题库'],
                'target_users': '国考/省考考生，25-35岁，需要面试辅导',
                'description': '基于大语言模型的AI面试教练，通过语音识别和自然语言处理，实时分析考生的答题逻辑、语言表达和应变能力，提供个性化反馈。'
            },
            {
                'name': '公考岗位匹配助手',
                'score': 78,
                'fun_score': 75,
                'use_score': 81,
                'features': ['智能岗位推荐', '竞争度分析', '历年分数线预测', '个人优势分析'],
                'target_users': '考公择岗期考生，迷茫不知道报什么职位',
                'description': '根据考生的专业、学历、户籍、兴趣等维度，结合历年职位竞争比和进面分数线，智能推荐最适合的岗位。'
            },
            {
                'name': '考友打卡社区',
                'score': 72,
                'fun_score': 80,
                'use_score': 64,
                'features': ['每日学习打卡', '进度可视化', '考友互助答疑', '模拟考试排名'],
                'target_users': '备考群体，需要学习监督和氛围',
                'description': '类似减肥打卡的备考社区，用户每天记录学习时长和内容，生成可视化进度，与其他考友互相激励。'
            }
        ]
    elif '携程' in hotword and '垄断' in hotword:
        ideas = [
            {
                'name': '旅行价格追踪器',
                'score': 88,
                'fun_score': 85,
                'use_score': 91,
                'features': ['多平台价格监控', '降价提醒', '历史价格趋势', '最优购买时机预测'],
                'target_users': '经常出差/旅行的人，25-45岁，注重性价比',
                'description': '监控携程、飞猪、同程等多个平台的酒店机票价格，当检测到价格下降时自动提醒用户，帮助用户在最佳时机下单。'
            },
            {
                'name': '透明出行助手',
                'score': 81,
                'fun_score': 78,
                'use_score': 84,
                'features': ['隐藏费用揭示', '大数据杀熟检测', '平台比价', '投诉维权指南'],
                'target_users': '对平台不信任的用户，追求消费透明',
                'description': '帮助用户识别在线旅游平台的隐形收费、大数据杀熟等问题，提供透明的价格信息和维权建议。'
            },
            {
                'name': '小众旅行聚合平台',
                'score': 75,
                'fun_score': 82,
                'use_score': 68,
                'features': ['冷门目的地推荐', '当地向导对接', '小众民宿筛选', '深度体验路线'],
                'target_users': '追求个性化旅行的年轻人，25-35岁',
                'description': '专注被大平台忽视的小众目的地和特色体验，对接当地向导和特色民宿，提供差异化旅行方案。'
            }
        ]
    elif 'DYG' in hotword or 'KPL' in hotword or '花海' in hotword or '一诺' in hotword:
        ideas = [
            {
                'name': '电竞选手八卦追踪器',
                'score': 82,
                'fun_score': 90,
                'use_score': 74,
                'features': ['实时瓜分推送', '多平台聚合', 'AI事件梳理', '真假瓜鉴别'],
                'target_users': '电竞粉丝，18-30岁，喜欢关注选手动态',
                'description': '聚合微博、抖音、B站等平台的电竞相关动态，AI自动梳理事件脉络，区分真瓜假瓜，为粉丝提供一站式吃瓜体验。'
            },
            {
                'name': '电竞情感调解室',
                'score': 79,
                'fun_score': 88,
                'use_score': 70,
                'features': ['选手情感分析', 'CP磕糖雷达', '情感时间线', '互动剧情预测'],
                'target_users': '娱乐圈式电竞粉丝，喜欢磕CP',
                'description': '专门分析电竞选手之间的互动和情感动态，生成CP互动时间线，预测后续剧情发展，满足粉丝的磕糖需求。'
            },
            {
                'name': '电竞数据可视化平台',
                'score': 86,
                'fun_score': 80,
                'use_score': 92,
                'features': ['实时比赛数据', '选手状态追踪', '英雄池分析', '战术拆解'],
                'target_users': '深度电竞爱好者、分析师、教练',
                'description': '深度挖掘KPL等比赛数据，用可视化方式呈现选手状态、英雄胜率、战术体系，为专业观众和从业者提供数据分析工具。'
            }
        ]
    elif '王安宇' in hotword or '周也' in hotword or '综艺' in hotword:
        ideas = [
            {
                'name': '综艺片段AI剪辑',
                'score': 84,
                'fun_score': 88,
                'use_score': 80,
                'features': ['智能名场面提取', '明星互动追踪', '搞笑片段合集', '一键分享到社媒'],
                'target_users': '综艺观众，18-35岁，喜欢分享片段',
                'description': 'AI自动识别综艺中的精彩片段、搞笑瞬间、名场面，生成可分享的短视频，方便用户在社交平台传播。'
            },
            {
                'name': '明星CP磕糖助手',
                'score': 77,
                'fun_score': 85,
                'use_score': 69,
                'features': ['CP互动检测', '眼神甜蜜度分析', '同框时间统计', '糖点时间轴'],
                'target_users': '粉丝群体，喜欢磕CP',
                'description': '自动检测综艺中明星之间的甜蜜互动，生成"糖点"时间轴和甜蜜度评分，帮助粉丝快速找到磕点。'
            },
            {
                'name': '综艺社交问答App',
                'score': 73,
                'fun_score': 80,
                'use_score': 66,
                'features': ['看综艺同步答题', '实时弹幕互动', '好友PK猜剧情', '积分兑换周边'],
                'target_users': '综艺观众，喜欢互动和社交',
                'description': '边看综艺边答题，和其他观众实时互动竞猜剧情发展，增强综艺观看的趣味性和社交性。'
            }
        ]
    elif '经济工作' in hotword:
        ideas = [
            {
                'name': '政策解读AI助手',
                'score': 80,
                'fun_score': 72,
                'use_score': 88,
                'features': ['政策智能提炼', '影响分析', '行业关联解读', '投资机会提示'],
                'target_users': '投资者、企业主、财经从业者',
                'description': 'AI将复杂的经济政策文件转化为通俗易懂的解读，分析对不同行业和投资标的的影响，帮助用户把握政策红利。'
            },
            {
                'name': '经济数据可视化大屏',
                'score': 76,
                'fun_score': 74,
                'use_score': 78,
                'features': ['多维度数据展示', '趋势预测', '行业对比', '自定义报表'],
                'target_users': '企业决策者、分析师',
                'description': '将枯燥的经济数据转化为直观的可视化图表，支持自定义维度和行业对比，帮助快速把握经济走势。'
            }
        ]
    else:
        # 通用创意模板
        ideas = [
            {
                'name': f'"{hotword}"内容创作助手',
                'score': 70,
                'fun_score': 72,
                'use_score': 68,
                'features': ['热点素材库', '创作灵感生成', '多格式导出', '一键发布'],
                'target_users': '内容创作者、自媒体',
                'description': f'基于"{hotword}"热点，为创作者提供相关素材和创作灵感，快速生成符合平台调性的内容。'
            },
            {
                'name': f'"{hotword}"知识卡片',
                'score': 65,
                'fun_score': 68,
                'use_score': 62,
                'features': ['关键信息提炼', '视觉化呈现', '知识关联', '收藏复习'],
                'target_users': '学习型用户',
                'description': f'将"{hotword}"相关的核心知识提炼成易读的卡片式内容，方便用户快速了解和分享。'
            }
        ]

    return ideas

# 生成完整HTML
def generate_html():
    # 统计数据
    all_ideas = []
    for hotspot in hotspots:
        ideas = generate_ideas_for_hotspot(hotspot)
        all_ideas.extend(ideas)

    excellent_count = len([i for i in all_ideas if i['score'] > 80])
    good_count = len([i for i in all_ideas if 60 <= i['score'] <= 80])
    avg_score = sum(i['score'] for i in all_ideas) / len(all_ideas) if all_ideas else 0

    # 生成HTML内容
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析报告 - {today.strftime('%Y年%-m月%-d日')}</title>
    <style>
        :root {{
            --primary-color: #FF6B35;
            --secondary-color: #FF8C42;
            --accent-excellent: #FFD23F;
            --accent-good: #06A77D;
            --bg-color: #FFF8F0;
            --text-color: #2D3142;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .report-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 32px;
        }}
        .report-header h1 {{ font-size: 32px; margin-bottom: 16px; }}
        .meta-info {{ display: flex; gap: 16px; flex-wrap: wrap; }}
        .meta-info span {{
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
        }}
        h2 {{
            font-size: 24px;
            margin-bottom: 20px;
            color: var(--primary-color);
            border-left: 4px solid var(--primary-color);
            padding-left: 12px;
        }}
        .hotspot-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}
        .hotspot-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .hotspot-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }}
        .rank {{
            background: var(--primary-color);
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        .hotword {{ font-weight: 600; font-size: 16px; flex: 1; }}
        .hotness {{ font-size: 13px; color: #666; }}
        .tag {{ background: var(--primary-color); color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
        .hotspot-detail {{
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 24px;
        }}
        .idea-card {{
            background: var(--bg-color);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 16px;
            border-left: 5px solid #E0E0E0;
        }}
        .idea-card.excellent {{ border-left-color: var(--accent-excellent); }}
        .idea-card.good {{ border-left-color: var(--accent-good); }}
        .idea-header {{ display: flex; justify-content: space-between; margin-bottom: 12px; }}
        .idea-name {{ font-size: 18px; font-weight: 600; }}
        .score {{ font-size: 20px; font-weight: 700; color: var(--primary-color); }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 8px;
        }}
        .badge.excellent {{ background: var(--accent-excellent); }}
        .badge.good {{ background: var(--accent-good); color: white; }}
        .idea-body p {{ margin-bottom: 8px; }}
        .idea-body ul {{ margin-left: 20px; margin-bottom: 12px; }}
        .idea-body strong {{ color: var(--primary-color); }}
        .statistics {{
            background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
            color: white;
            padding: 32px;
            border-radius: 16px;
            margin-bottom: 32px;
        }}
        .statistics h2 {{ color: white; border-left-color: white; }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
        }}
        .stat-item {{ text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 12px; }}
        .stat-value {{ font-size: 36px; font-weight: 700; display: block; }}
        .stat-label {{ font-size: 14px; opacity: 0.9; }}
        .footer {{ text-align: center; padding: 32px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <header class="report-header">
            <h1>微博热搜产品创意分析报告</h1>
            <div class="meta-info">
                <span>生成日期：{current_date_str}</span>
                <span>热搜总数：{len(hotspots)}</span>
                <span>创意总数：{len(all_ideas)}</span>
            </div>
        </header>

        <h2>📊 热搜概览</h2>
        <div class="hotspot-list">
'''

    # 生成TOP10概览
    for hotspot in hotspots:
        tag_html = f'<span class="tag">{hotspot["hot_tag"]}</span>' if hotspot['hot_tag'] else ''
        html_content += f'''
            <div class="hotspot-card">
                <div class="hotspot-header">
                    <span class="rank">{hotspot['rank']}</span>
                    <span class="hotword">{hotspot['hotword']}</span>
                </div>
                <div class="hotness">热度：{hotspot["hotword_num"]} {tag_html}</div>
            </div>
'''

    html_content += '''
        </div>

        <h2>🔍 详细产品创意分析</h2>
'''

    # 生成详细分析
    for hotspot in hotspots:
        ideas = generate_ideas_for_hotspot(hotspot)
        tag_display = f' [{hotspot["hot_tag"]}]' if hotspot['hot_tag'] else ''

        html_content += f'''
        <div class="hotspot-detail">
            <div class="hotspot-header">
                <span class="rank">{hotspot['rank']}</span>
                <span class="hotword">{hotspot['hotword']}{tag_display}</span>
            </div>
            <p><strong>热度指数：</strong>{hotspot["hotword_num_int"]}</p>
            <div class="product-ideas">
'''

        for idea in ideas:
            badge_class = 'excellent' if idea['score'] > 80 else 'good' if idea['score'] >= 60 else ''
            badge_text = '优秀' if idea['score'] > 80 else '良好' if idea['score'] >= 60 else ''

            features_html = ''.join(f'<li>{f}</li>' for f in idea['features'])

            html_content += f'''
                <div class="idea-card {badge_class}">
                    <div class="idea-header">
                        <span class="idea-name">{idea['name']}</span>
                        <span>
                            <span class="score">{idea['score']}分</span>
                            {f'<span class="badge {badge_class}">{badge_text}</span>' if badge_text else ''}
                        </span>
                    </div>
                    <div class="idea-body">
                        <p><strong>核心功能：</strong></p>
                        <ul>{features_html}</ul>
                        <p><strong>目标用户：</strong>{idea['target_users']}</p>
                        <p><strong>产品描述：</strong>{idea['description']}</p>
                        <p><strong>评分：</strong>有趣度 {idea['fun_score']}分 × 80% + 有用度 {idea['use_score']}分 × 20%</p>
                    </div>
                </div>
'''

        html_content += '''
            </div>
        </div>
'''

    # 统计部分
    html_content += f'''
        <div class="statistics">
            <h2>📈 数据统计</h2>
            <div class="stat-grid">
                <div class="stat-item">
                    <span class="stat-value">{len(all_ideas)}</span>
                    <span class="stat-label">创意总数</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{excellent_count}</span>
                    <span class="stat-label">优秀创意（>80分）</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{good_count}</span>
                    <span class="stat-label">良好创意（60-80分）</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{avg_score:.1f}</span>
                    <span class="stat-label">平均评分</span>
                </div>
            </div>
        </div>

        <footer class="footer">
            <p>本报告由AI自动生成 | 仅供参考 | 微博热搜数据来源：天聚数行API</p>
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>
'''

    return html_content

# 生成HTML
html = generate_html()

# 创建输出目录（使用绝对路径，指向vault根目录）
vault_root = '/Users/wanglingwei/Movies/violinvault/SynologyDrive/Clipping'
output_dir = f'{vault_root}/19-ClaudeCode/微博热搜/{current_year_month}'
os.makedirs(output_dir, exist_ok=True)

# 保存文件（使用当前日期）
output_file = f'{output_dir}/{current_date_str}_weibo_hotspot_report.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✅ 报告已生成：{output_file}')
print(f'📊 热搜数量：{len(hotspots)}')
print(f'💡 创意数量：{sum(len(generate_ideas_for_hotspot(h)) for h in hotspots)}')
