#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜产品创意HTML报告生成器 (GitHub Actions 版本)

功能：
- 读取 Claude 生成的创意数据
- 生成精美的 HTML 报告
- 支持响应式设计

用法：
python generate_html_report_v2.py

输入：
- weibo_ideas_*.json (Claude 分析生成的创意数据)

输出：
- weibo_hotspot_report_YYYYMMDD_HHMMSS.html

版本：
v2.0.0 (2026-01-18) - GitHub Actions 迁移版本
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List


class HTMLReportGenerator:
    """HTML 报告生成器"""

    def __init__(self):
        self.hotspots_data = None
        self.ideas_data = None

    def load_latest_data(self):
        """加载最新的热搜和创意数据"""
        import glob

        # 查找最新的创意数据文件
        ideas_files = glob.glob('weibo_ideas_*.json')
        if not ideas_files:
            raise FileNotFoundError("未找到创意数据文件，请先运行 claude_analysis.py")

        latest_ideas = max(ideas_files, key=os.path.getctime)
        print(f"📂 读取创意文件: {latest_ideas}")

        with open(latest_ideas, 'r', encoding='utf-8') as f:
            self.ideas_data = json.load(f)

        # 查找最新的热搜数据文件
        hotspots_files = glob.glob('weibo_hotspots_*.json')
        if hotspots_files:
            latest_hotspots = max(hotspots_files, key=os.path.getctime)
            print(f"📂 读取热搜文件: {latest_hotspots}")

            with open(latest_hotspots, 'r', encoding='utf-8') as f:
                self.hotspots_data = json.load(f)

    def get_hotspot_info(self, hotword: str) -> Dict:
        """获取热搜信息"""
        if not self.hotspots_data:
            return {}

        for hotspot in self.hotspots_data.get('data', []):
            if hotspot['hotword'] == hotword:
                return hotspot
        return {}

    def generate_html(self) -> str:
        """生成 HTML 内容"""
        if not self.ideas_data:
            raise ValueError("未加载创意数据")

        ideas = self.ideas_data.get('ideas', [])
        stats = self.ideas_data.get('statistics', {})

        # 按热搜分组
        ideas_by_hotspot = {}
        for idea in ideas:
            hotword = idea.get('hotword', '未知话题')
            if hotword not in ideas_by_hotspot:
                ideas_by_hotspot[hotword] = []
            ideas_by_hotspot[hotword].append(idea)

        # 按热搜排序（根据第一个创意的 rank）
        sorted_hotspots = sorted(
            ideas_by_hotspot.items(),
            key=lambda x: x[1][0].get('rank', 999) if x[1] else 999
        )

        # 生成 HTML
        html = self._generate_html_header()
        html += self._generate_overview_section(sorted_hotspots[:10])
        html += self._generate_details_section(sorted_hotspots)
        html += self._generate_ranking_section(ideas)
        html += self._generate_statistics_section(stats)
        html += self._generate_footer()

        return html

    def _generate_html_header(self) -> str:
        """生成 HTML 头部"""
        generate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析报告 - {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        :root {{
            --primary-color: #FF6B35;
            --secondary-color: #FF8C42;
            --accent-excellent: #FFD23F;
            --accent-good: #06A77D;
            --accent-normal: #6C757D;
            --bg-color: #FFF8F0;
            --text-color: #2D3142;
            --card-bg: #FFFFFF;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .report-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 32px;
            box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
        }}

        .report-header h1 {{
            font-size: 32px;
            margin-bottom: 16px;
            font-weight: 700;
        }}

        .meta-info {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .meta-info span {{
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
        }}

        h2 {{
            font-size: 24px;
            margin-bottom: 20px;
            color: var(--primary-color);
            border-left: 4px solid var(--primary-color);
            padding-left: 12px;
            margin-top: 32px;
        }}

        .hotspot-list {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}

        .hotspot-card {{
            background: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .hotspot-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        }}

        .hotspot-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

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
            font-size: 14px;
            flex-shrink: 0;
        }}

        .hotword {{
            font-weight: 600;
            font-size: 16px;
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .hotness {{
            font-size: 13px;
            color: #666;
        }}

        .hotspot-summary {{
            margin-top: 8px;
            font-size: 13px;
            color: #555;
            line-height: 1.5;
            font-style: italic;
        }}

        .tag {{
            background: var(--primary-color);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }}

        .hotspot-detail {{
            background: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            margin-bottom: 24px;
        }}

        .hotspot-title {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 2px solid #f0f0f0;
        }}

        .idea-card {{
            background: var(--bg-color);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 16px;
            border-left: 5px solid #E0E0E0;
            transition: all 0.2s;
        }}

        .idea-card:hover {{
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        .idea-card.excellent {{
            border-left-color: var(--accent-excellent);
            background: linear-gradient(to right, rgba(255, 210, 63, 0.1), transparent);
        }}

        .idea-card.good {{
            border-left-color: var(--accent-good);
            background: linear-gradient(to right, rgba(6, 167, 125, 0.05), transparent);
        }}

        .idea-card.normal {{
            border-left-color: var(--accent-normal);
        }}

        .idea-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .idea-name {{
            font-size: 18px;
            font-weight: 600;
            color: var(--text-color);
        }}

        .score-info {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .score {{
            font-size: 20px;
            font-weight: 700;
            color: var(--primary-color);
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}

        .badge.excellent {{
            background: var(--accent-excellent);
            color: #333;
        }}

        .badge.good {{
            background: var(--accent-good);
            color: white;
        }}

        .badge.normal {{
            background: var(--accent-normal);
            color: white;
        }}

        .idea-body p {{
            margin-bottom: 8px;
            font-size: 14px;
        }}

        .idea-body strong {{
            color: var(--primary-color);
            font-weight: 600;
        }}

        .idea-body ul {{
            margin-left: 20px;
            margin-bottom: 12px;
        }}

        .idea-body li {{
            margin-bottom: 4px;
            font-size: 14px;
        }}

        .score-breakdown {{
            font-size: 13px;
            color: #666;
            font-style: italic;
        }}

        .statistics {{
            background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
            color: white;
            padding: 32px;
            border-radius: 16px;
            margin-bottom: 32px;
            box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
        }}

        .statistics h2 {{
            color: white;
            border-left-color: white;
            margin-top: 0;
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
        }}

        .stat-item {{
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}

        .stat-value {{
            font-size: 36px;
            font-weight: 700;
            display: block;
            margin-bottom: 8px;
        }}

        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}

        .ranking-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .ranking-item {{
            background: var(--card-bg);
            padding: 16px 20px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }}

        .ranking-rank {{
            font-size: 24px;
            font-weight: 700;
            width: 40px;
            text-align: center;
        }}

        .ranking-rank.gold {{ color: #FFD700; }}
        .ranking-rank.silver {{ color: #C0C0C0; }}
        .ranking-rank.bronze {{ color: #CD7F32; }}

        .ranking-info {{
            flex: 1;
        }}

        .ranking-name {{
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 4px;
        }}

        .ranking-hotword {{
            font-size: 13px;
            color: #666;
        }}

        .ranking-score {{
            font-size: 24px;
            font-weight: 700;
            color: var(--primary-color);
        }}

        .footer {{
            text-align: center;
            padding: 32px;
            color: #666;
            font-size: 14px;
        }}

        @media (max-width: 768px) {{
            .report-header {{ padding: 24px; }}
            .report-header h1 {{ font-size: 24px; }}
            .hotspot-list {{ grid-template-columns: 1fr; }}
            .idea-header {{ flex-direction: column; align-items: flex-start; }}
            .stat-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="report-header">
            <h1>🤖 微博热搜产品创意分析报告</h1>
            <div class="meta-info">
                <span>📅 生成日期：{datetime.now().strftime('%Y-%m-%d')}</span>
                <span>🔥 热搜总数：{len(self.ideas_data.get('ideas', [])) // 3 if self.ideas_data else 0}</span>
                <span>💡 创意总数：{self.ideas_data.get('statistics', {}).get('total', 0) if self.ideas_data else 0}</span>
                <span>⏰ 生成时间：{generate_time}</span>
            </div>
        </header>
'''

    def _generate_overview_section(self, top_hotspots) -> str:
        """生成概览部分"""
        html = '''
        <h2>📊 热搜TOP10概览</h2>
        <div class="hotspot-list">
'''

        for hotword, ideas in top_hotspots:
            if not ideas:
                continue

            idea = ideas[0]
            hotspot_info = self.get_hotspot_info(hotword)
            tag = hotspot_info.get('hot_tag', '')
            hotness = hotspot_info.get('hotword_num', idea.get('hotness', ''))
            summary = idea.get('hotspot_summary', '')  # 获取热搜描述

            tag_html = f'<span class="tag">{tag}</span>' if tag else ''
            summary_html = f'<div class="hotspot-summary">{summary}</div>' if summary else ''

            html += f'''
            <div class="hotspot-card">
                <div class="hotspot-header">
                    <span class="rank">{idea.get('rank', '?')}</span>
                    <span class="hotword">{hotword}</span>
                </div>
                <div class="hotness">热度：{hotness} {tag_html}</div>
                {summary_html}
            </div>
'''

        html += '\n        </div>\n'
        return html

    def _generate_details_section(self, sorted_hotspots) -> str:
        """生成详细分析部分"""
        html = '\n        <h2>🔍 详细产品创意分析</h2>\n'

        for hotword, ideas in sorted_hotspots:
            if not ideas:
                continue

            idea = ideas[0]
            hotspot_info = self.get_hotspot_info(hotword)
            tag = hotspot_info.get('hot_tag', '')
            hotness = hotspot_info.get('hotword_num_int', idea.get('hotness', 0))

            tag_display = f' <span class="tag">{tag}</span>' if tag else ''

            html += f'''
        <div class="hotspot-detail">
            <div class="hotspot-title">
                <span class="rank">{idea.get('rank', '?')}</span>
                <span class="hotword" style="font-size: 18px;">{hotword}{tag_display}</span>
            </div>
            <p><strong>🔥 热度指数：</strong>{hotness:,}</p>
            <div class="product-ideas">
'''

            for idea_data in ideas:
                score = idea_data.get('score', 0)
                badge_class = 'excellent' if score > 80 else 'good' if score >= 60 else 'normal'
                badge_text = '优秀' if score > 80 else '良好' if score >= 60 else '普通'

                features = idea_data.get('features', [])
                features_html = '\n                    '.join([f'<li>{f}</li>' for f in features])

                html += f'''
                <div class="idea-card {badge_class}">
                    <div class="idea-header">
                        <span class="idea-name">{idea_data.get('name', '未知创意')}</span>
                        <div class="score-info">
                            <span class="score">{score}分</span>
                            <span class="badge {badge_class}">{badge_text}</span>
                        </div>
                    </div>
                    <div class="idea-body">
                        <p><strong>💎 核心功能：</strong></p>
                        <ul>
                            {features_html}
                        </ul>
                        <p><strong>👥 目标用户：</strong>{idea_data.get('target_users', '未指定')}</p>
                        <p><strong>📝 产品描述：</strong>{idea_data.get('description', '无描述')}</p>
                        <p class="score-breakdown">
                            评分：有趣度 {idea_data.get('fun_score', 0)}分 × 80% + 有用度 {idea_data.get('use_score', 0)}分 × 20%
                        </p>
                    </div>
                </div>
'''

            html += '\n            </div>\n        </div>\n'

        return html

    def _generate_ranking_section(self, ideas: List[Dict]) -> str:
        """生成排行榜部分"""
        # 按评分排序
        sorted_ideas = sorted(ideas, key=lambda x: x.get('score', 0), reverse=True)[:20]

        html = '\n        <h2>🏆 产品创意排行榜 (TOP20)</h2>\n        <div class="ranking-list">\n'

        for idx, idea in enumerate(sorted_ideas, 1):
            rank_class = ''
            if idx == 1:
                rank_class = 'gold'
            elif idx == 2:
                rank_class = 'silver'
            elif idx == 3:
                rank_class = 'bronze'

            rank_display = f'#{idx}' if idx <= 3 else f'{idx}'

            html += f'''
            <div class="ranking-item">
                <span class="ranking-rank {rank_class}">{rank_display}</span>
                <div class="ranking-info">
                    <div class="ranking-name">{idea.get('name', '未知')}</div>
                    <div class="ranking-hotword">来源：{idea.get('hotword', '未知热搜')}</div>
                </div>
                <span class="ranking-score">{idea.get('score', 0)}分</span>
            </div>
'''

        html += '\n        </div>\n'
        return html

    def _generate_statistics_section(self, stats: Dict) -> str:
        """生成统计部分"""
        html = f'''
        <div class="statistics">
            <h2>📈 数据统计</h2>
            <div class="stat-grid">
                <div class="stat-item">
                    <span class="stat-value">{stats.get('total', 0)}</span>
                    <span class="stat-label">创意总数</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{stats.get('excellent', 0)}</span>
                    <span class="stat-label">优秀创意 (&gt;80分)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{stats.get('good', 0)}</span>
                    <span class="stat-label">良好创意 (60-80分)</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{stats.get('avg_score', 0):.1f}</span>
                    <span class="stat-label">平均评分</span>
                </div>
            </div>
        </div>
'''
        return html

    def _generate_footer(self) -> str:
        """生成页脚"""
        return '''
        <footer class="footer">
            <p>🤖 本报告由 AI 自动生成 | 仅供参考</p>
            <p>数据来源：天聚数行 API | AI 分析：Claude 3.5 Sonnet</p>
            <p>生成时间：{generate_time}</p>
        </footer>
    </div>
</body>
</html>
'''.format(generate_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def save_to_file(self, html_content: str, filename: str = None):
        """保存 HTML 到文件"""
        if filename is None:
            filename = f"weibo_hotspot_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"\n✅ HTML 报告已生成: {filename}")
        print(f"📊 文件大小: {os.path.getsize(filename) / 1024:.1f} KB")

        return filename


def main():
    """主函数"""
    print("=" * 60)
    print("HTML 报告生成器")
    print("=" * 60)

    try:
        generator = HTMLReportGenerator()

        # 加载数据
        print("\n📂 加载数据...")
        generator.load_latest_data()

        # 生成 HTML
        print("\n🎨 生成 HTML 报告...")
        html_content = generator.generate_html()

        # 保存文件
        output_file = generator.save_to_file(html_content)

        print("\n✅ 报告生成完成!")
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"\n❌ 错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
