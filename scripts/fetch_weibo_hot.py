#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜API调用脚本 (GitHub Actions 版本)

功能：
- 调用天聚数行微博热搜API
- 解析JSON返回数据
- 输出结构化热搜信息
- 支持环境变量配置 API Key

用法：
python fetch_weibo_hot_v2.py

环境变量：
- TIANAPI_KEY: 天聚数行 API 密钥（可选，默认使用内置密钥）

输出：
- JSON格式的热搜榜单数据
- 包含热搜词、热度、标签等信息

作者：
Claude Code Skill Generator

版本：
v2.0.0 (2026-01-18) - GitHub Actions 迁移版本
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List
import urllib.request
import urllib.error


class WeiboHotspotFetcher:
    """微博热搜榜单获取器"""

    def __init__(self, api_key: str):
        """
        初始化获取器

        Args:
            api_key: 天聚数行API密钥
        """
        if not api_key:
            raise ValueError("API 密钥不能为空")

        self.api_key = api_key
        self.api_url = "https://apis.tianapi.com/weibohot/index"

    def fetch(self) -> Dict:
        """
        获取微博热搜榜单

        Returns:
            包含热搜数据和元信息的字典
            {
                "success": True/False,
                "code": 200,
                "message": "success",
                "data": [...],
                "fetch_time": "2025-01-04 10:30:00",
                "total": 50
            }
        """
        try:
            # 构建请求URL
            url = f"{self.api_url}?key={self.api_key}"

            # 发起HTTP GET请求
            with urllib.request.urlopen(url, timeout=10) as response:
                response_data = response.read().decode('utf-8')
                result = json.loads(response_data)

            # 检查返回状态码
            if result.get('code') != 200:
                return {
                    "success": False,
                    "code": result.get('code'),
                    "message": result.get('msg', 'Unknown error'),
                    "data": [],
                    "fetch_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "total": 0
                }

            # 解析热搜数据
            result_data = result.get('result', {})
            hotspot_list = result_data.get('list', []) if isinstance(result_data, dict) else result_data

            # 格式化数据
            formatted_data = []
            for idx, item in enumerate(hotspot_list, 1):
                hotword = item.get('hotword', '').strip()
                hotword_num_raw = item.get('hotwordnum', '0').strip()

                # 清理热度值中的非数字字符（如"剧集 1123860" -> "1123860"）
                hotword_num_clean = re.sub(r'[^\d]', '', hotword_num_raw)
                hotword_num_int = int(hotword_num_clean) if hotword_num_clean else 0

                formatted_data.append({
                    "rank": idx,
                    "hotword": hotword,
                    "hotword_num": hotword_num_raw,
                    "hotword_num_int": hotword_num_int,
                    "hot_tag": item.get('hottag', ''),
                    "weibo_url": f"https://s.weibo.com/weibo?q={urllib.parse.quote(hotword)}"
                })

            return {
                "success": True,
                "code": 200,
                "message": "success",
                "data": formatted_data,
                "fetch_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total": len(formatted_data)
            }

        except urllib.error.URLError as e:
            return {
                "success": False,
                "code": -1,
                "message": f"网络错误: {str(e)}",
                "data": [],
                "fetch_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total": 0
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "code": -2,
                "message": f"JSON解析错误: {str(e)}",
                "data": [],
                "fetch_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total": 0
            }
        except Exception as e:
            return {
                "success": False,
                "code": -3,
                "message": f"未知错误: {str(e)}",
                "data": [],
                "fetch_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total": 0
            }

    def print_summary(self, result: Dict):
        """
        打印热搜榜单摘要

        Args:
            result: fetch()方法返回的字典
        """
        if not result.get('success'):
            print(f"❌ 获取失败: {result.get('message')} (错误码: {result.get('code')})")
            sys.exit(1)

        print(f"\n✅ 成功获取微博热搜榜单")
        print(f"📅 抓取时间: {result['fetch_time']}")
        print(f"📊 热搜总数: {result['total']}")
        print(f"\n{'='*60}")

        # 打印TOP10
        print("\n🔥 热搜TOP10:")
        print("-" * 60)

        for item in result['data'][:10]:
            rank = item['rank']
            hotword = item['hotword']
            hotness = item['hotword_num']
            tag = item['hot_tag']

            print(f"{rank:2d}. {hotword}")
            print(f"    热度: {hotness} | 标签: {tag}")
            print(f"    链接: {item['weibo_url']}")
            print("-" * 60)

    def save_to_file(self, result: Dict, filename: str = None):
        """
        保存热搜数据到JSON文件

        Args:
            result: fetch()方法返回的字典
            filename: 输出文件名（可选）
        """
        if filename is None:
            filename = f"weibo_hotspots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n💾 数据已保存到: {filename}")

            # 保存文件名到 .latest_hotspots 文件，供后续脚本使用
            with open('.latest_hotspots', 'w') as f:
                f.write(filename)

        except Exception as e:
            print(f"\n❌ 保存文件失败: {str(e)}")
            sys.exit(1)


def main():
    """主函数"""
    print("=" * 60)
    print("微博热搜数据抓取器")
    print("=" * 60)

    # 从环境变量读取 API 密钥
    API_KEY = os.environ.get('TIANAPI_KEY')

    if not API_KEY:
        print("\n❌ 错误: 未设置 TIANAPI_KEY 环境变量")
        print("\n请设置环境变量:")
        print("  export TIANAPI_KEY='your-api-key'")
        print("\n或在 GitHub Secrets 中配置:")
        print("  TIANAPI_KEY = your_api_key")
        sys.exit(1)

    try:
        # 创建获取器实例
        fetcher = WeiboHotspotFetcher(API_KEY)

        # 获取热搜数据
        print("\n🌐 正在抓取微博热搜...")
        result = fetcher.fetch()

        # 打印摘要
        fetcher.print_summary(result)

        # 保存到文件
        fetcher.save_to_file(result)

        print("\n✅ 抓取完成!")
        sys.exit(0)

    except ValueError as e:
        print(f"\n❌ 错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
