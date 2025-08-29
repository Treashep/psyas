# -*- coding: utf-8 -*-
"""知识库服务独立集成测试（不依赖数据库）."""
import sys
from datetime import datetime


def print_separator(title):
    """打印分隔符."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def _run_framework_tests(knowledge_service):
    """运行框架匹配测试."""
    test_cases = [
        {
            "input": "我最近工作压力特别大，每天都感觉很焦虑",
            "expected_framework": "正念疗法",
            "description": "工作压力+焦虑",
        },
        {
            "input": "和男朋友分手了，感觉很难过很绝望",
            "expected_framework": "CBT",
            "description": "分手+抑郁",
        },
        {
            "input": "今天升职了，特别开心！",
            "expected_framework": "积极心理学",
            "description": "积极情绪",
        },
        {
            "input": "我不想活了，感觉没有意义",
            "expected_framework": "危机干预",
            "description": "危机情况",
        },
    ]

    successful_tests = 0

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}: {test_case['description']}")
        print(f"用户输入: {test_case['input']}")
        print(f"预期框架: {test_case['expected_framework']}")

        try:
            result = knowledge_service.analyze_user_input(test_case["input"])

            if result:
                print(f"匹配框架: {result.framework}")
                print(f"置信度: {result.confidence:.2f}")
                print(f"立即回应: {result.immediate_response}")

                if result.framework == test_case["expected_framework"]:
                    print("✅ 框架匹配正确")
                    successful_tests += 1
                else:
                    print("⚠️ 框架匹配不正确")
            else:
                print("❌ 未能生成匹配结果")

        except (ImportError, AttributeError, RuntimeError) as e:
            print(f"❌ 测试失败: {str(e)}")

    return successful_tests, len(test_cases)


def _run_crisis_detection_tests(knowledge_service):
    """运行危机检测测试."""
    crisis_texts = ["活着太痛苦了，想要结束", "我不想活了", "想要伤害自己"]

    crisis_detected = 0
    for text in crisis_texts:
        result = knowledge_service.analyze_user_input(text)
        if result and result.framework == "危机干预":
            crisis_detected += 1
            print(f"✅ 危机检测: '{text[:10]}...' -> 正确识别")
        else:
            print(f"❌ 危机检测: '{text[:10]}...' -> 未能识别")

    return crisis_detected, len(crisis_texts)


def _run_framework_info_tests(knowledge_service):
    """运行框架信息测试."""
    frameworks = ["CBT", "正念疗法", "人际关系疗法", "积极心理学"]
    framework_info_success = 0

    for framework in frameworks:
        info = knowledge_service.get_framework_info(framework)
        if info:
            framework_info_success += 1

    return framework_info_success, len(frameworks)


def _summarize_test_results(
    successful_tests,
    total_tests,
    crisis_detected,
    crisis_total,
    framework_info_success,
    frameworks_total,
    safety_test,
):
    """汇总测试结果."""
    print_separator("测试结果汇总")
    print(f"框架匹配测试: {successful_tests}/{total_tests} 通过")
    print(f"危机检测测试: {crisis_detected}/{crisis_total} 通过")
    print(f"框架信息测试: {framework_info_success}/{frameworks_total} 通过")
    print(f"安全指南测试: {'通过' if safety_test else '失败'}")

    overall_success = (
        successful_tests == total_tests
        and crisis_detected >= 2
        and framework_info_success == frameworks_total
        and safety_test
    )
    return overall_success


def test_knowledge_service_integration():
    """测试知识库服务的核心功能."""
    try:
        from psyas.services.knowledge_service import KnowledgeService

        print_separator("知识库服务核心功能测试")

        # 初始化知识库服务
        knowledge_service = KnowledgeService()
        print("✅ 知识库服务初始化成功")

        # 运行框架测试
        successful_tests, total_tests = _run_framework_tests(knowledge_service)

        print_separator("功能特性测试")

        # 运行危机检测测试
        crisis_detected, crisis_total = _run_crisis_detection_tests(knowledge_service)

        # 运行框架信息测试
        framework_info_success, frameworks_total = _run_framework_info_tests(
            knowledge_service
        )

        print(f"📚 框架信息获取: {framework_info_success}/{frameworks_total} 成功")

        # 测试安全指南
        safety_guide = knowledge_service.get_safety_guidelines()
        safety_test = len(safety_guide) >= 4  # 应该包含disclaimer, crisis_hotline等
        print(f"🛡️ 安全指南: {'✅ 完整' if safety_test else '❌ 不完整'}")

        # 汇总结果
        return _summarize_test_results(
            successful_tests,
            total_tests,
            crisis_detected,
            crisis_total,
            framework_info_success,
            frameworks_total,
            safety_test,
        )

    except (ImportError, AttributeError) as e:
        print(f"❌ 导入失败: {e}")
        return False
    except (RuntimeError, ValueError) as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """主测试流程."""
    print(f"知识库服务集成测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    success = test_knowledge_service_integration()

    if success:
        print("🎉 所有测试通过！知识库服务功能完整且正常工作。")
        print("\n🔗 集成建议:")
        print(
            "1. 在ConversationService中使用knowledge_service.analyze_user_input()增强回复"
        )
        print(
            "2. 在AnalysisService中使用knowledge_service.suggest_techniques()提供专业建议"
        )
        print("3. 添加危机检测机制到现有的对话流程中")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查知识库配置和数据文件。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
