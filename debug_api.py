#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 调试脚本 - 测试 Claude API 连接和响应

用法:
export API_ENDPOINT="your_api_endpoint"
export API_KEY="your_api_key"
python debug_api.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

def test_api():
    """测试 API 连接"""
    endpoint = os.environ.get('API_ENDPOINT')
    api_key = os.environ.get('API_KEY')
    model = os.environ.get('API_MODEL', 'claude-sonnet-4-5')
    
    if not endpoint or not api_key:
        print("❌ 错误: 请设置 API_ENDPOINT 和 API_KEY 环境变量")
        sys.exit(1)
    
    print("=" * 60)
    print("Claude API 调试工具")
    print("=" * 60)
    print(f"\n📡 API 端点: {endpoint}")
    print(f"🤖 模型: {model}")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-5:]}")
    
    # 简单的测试请求
    test_prompt = "请返回一个JSON格式的数据：{\"test\": \"success\", \"message\": \"API正常工作\"}"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": test_prompt}
        ],
        "stream": False
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"\n📤 发送测试请求...")
    print(f"   Prompt: {test_prompt}")
    
    try:
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            status = response.status
            response_data = response.read().decode('utf-8')
            
        print(f"\n✅ HTTP 状态码: {status}")
        print(f"\n📥 原始响应 (前 500 字符):")
        print("-" * 60)
        print(response_data[:500])
        if len(response_data) > 500:
            print(f"\n... (还有 {len(response_data) - 500} 个字符)")
        print("-" * 60)
        
        # 尝试解析 JSON
        try:
            result = json.loads(response_data)
            print(f"\n✅ JSON 解析成功")
            print(f"\n📊 响应结构:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])
            
            # 检查是否有 OpenAI 格式的 choices
            if 'choices' in result:
                print(f"\n✅ 找到 'choices' 字段")
                if len(result['choices']) > 0:
                    content = result['choices'][0].get('message', {}).get('content', '')
                    print(f"\n📝 AI 返回内容:")
                    print("-" * 60)
                    print(content[:500])
                    print("-" * 60)
                else:
                    print(f"\n⚠️  'choices' 数组为空")
            else:
                print(f"\n❌ 未找到 'choices' 字段")
                print(f"\n可用的字段: {list(result.keys())}")
                
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON 解析失败: {e}")
            print(f"\n这可能是问题所在！API 返回的不是有效的 JSON。")
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"\n❌ HTTP 错误 {e.code}")
        print(f"\n错误响应:")
        print(error_body)
        sys.exit(1)
        
    except urllib.error.URLError as e:
        print(f"\n❌ 网络错误: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ 未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print(f"\n" + "=" * 60)
    print("✅ 调试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
