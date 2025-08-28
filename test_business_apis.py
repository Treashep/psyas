# -*- coding: utf-8 -*-
"""业务接口功能测试脚本."""
import json
import sys
from datetime import datetime

import requests

# 配置
BASE_URL = "http://localhost:5000"
TEST_USER_ID = 1


def print_separator(title):
    """打印分隔符."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def test_conversation_status():
    """测试对话服务状态."""
    print_separator("测试对话服务状态")

    try:
        url = f"{BASE_URL}/api/conversation/status"
        response = requests.get(url)

        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_analysis_status():
    """测试分析服务状态."""
    print_separator("测试分析服务状态")

    try:
        url = f"{BASE_URL}/api/analysis/status"
        response = requests.get(url)

        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_chat_api():
    """测试对话接口."""
    print_separator("测试对话接口")

    try:
        url = f"{BASE_URL}/api/conversation/chat"
        data = {"user_id": TEST_USER_ID, "message": "我最近感觉很焦虑，工作压力很大"}

        response = requests.post(
            url, json=data, headers={"Content-Type": "application/json"}
        )

        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 200:
            return response.json().get("data", {}).get("conversation_id")
        return None
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return None


def test_analysis_api(conversation_id=None):
    """测试分析接口."""
    print_separator("测试分析接口")

    try:
        url = f"{BASE_URL}/api/analysis/analyze"
        data = {"user_id": TEST_USER_ID}
        if conversation_id:
            data["conversation_id"] = conversation_id

        response = requests.post(
            url, json=data, headers={"Content-Type": "application/json"}
        )

        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 200:
            return response.json().get("data", {}).get("analysis_id")
        return None
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return None


def test_conversation_history():
    """测试对话历史接口."""
    print_separator("测试对话历史接口")

    try:
        url = f"{BASE_URL}/api/conversation/history/{TEST_USER_ID}"
        response = requests.get(url)

        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_analysis_results():
    """测试分析结果列表接口."""
    print_separator("测试分析结果列表接口")

    try:
        url = f"{BASE_URL}/api/analysis/results/{TEST_USER_ID}"
        response = requests.get(url)

        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def test_analysis_summary():
    """测试分析摘要接口."""
    print_separator("测试分析摘要接口")

    try:
        url = f"{BASE_URL}/api/analysis/summary/{TEST_USER_ID}"
        response = requests.get(url)

        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


def main():
    """主测试流程."""
    print(f"开始业务接口功能测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试目标服务器: {BASE_URL}")
    print(f"测试用户ID: {TEST_USER_ID}")

    test_results = []

    # 1. 测试服务状态
    test_results.append(("对话服务状态", test_conversation_status()))
    test_results.append(("分析服务状态", test_analysis_status()))

    # 2. 测试核心业务流程
    conversation_id = test_chat_api()
    test_results.append(("对话接口", conversation_id is not None))

    if conversation_id:
        analysis_id = test_analysis_api(conversation_id)
        test_results.append(("分析接口", analysis_id is not None))
    else:
        print("⚠️ 跳过分析接口测试，因为对话接口测试失败")
        test_results.append(("分析接口", False))

    # 3. 测试查询接口
    test_results.append(("对话历史接口", test_conversation_history()))
    test_results.append(("分析结果列表接口", test_analysis_results()))
    test_results.append(("分析摘要接口", test_analysis_summary()))

    # 输出测试结果汇总
    print_separator("测试结果汇总")
    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n总计: {passed}/{total} 个测试通过")

    if passed == total:
        print("🎉 所有测试通过！业务接口功能正常。")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查服务器状态和数据库连接。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
