# -*- coding: utf-8 -*-
"""知识库服务测试脚本."""
import sys
from datetime import datetime

# 尝试导入服务模块
try:
    from psyas.services.knowledge_service import KnowledgeService
except ImportError as e:
    print(f"警告：服务模块导入失败: {e}")


def print_separator(title):
    """打印分隔符."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def _test_basic_functionality(knowledge_service):
    """测试基础功能."""
    print("✅ 知识库服务初始化成功")

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
            "input": "跟室友总是吵架，觉得很愤怒",
            "expected_framework": "正念疗法",
            "description": "人际冲突+愤怒",
        },
        {
            "input": "今天升职了，特别开心！",
            "expected_framework": "积极心理学",
            "description": "积极情绪",
        },
        {
            "input": "感觉一个人很孤独，没人理解我",
            "expected_framework": "人际关系疗法",
            "description": "孤独情绪",
        },
    ]

    successful_tests = 0

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['description']}")
        print(f"用户输入: {test_case['input']}")

        try:
            result = knowledge_service.analyze_user_input(test_case["input"])

            if result:
                print(f"  🎯 匹配框架: {result.framework}")
                print(f"  📊 置信度: {result.confidence:.2f}")
                print(f"  💬 立即回应: {result.immediate_response}...")
                print(
                    f"  ❓ 后续问题: {result.follow_up_questions[0] if result.follow_up_questions else '无'}"
                )
                print(f"  🛠️ 技巧数量: {len(result.techniques)}")

                if result.framework == test_case["expected_framework"]:
                    print("  ✅ 框架匹配正确")
                    successful_tests += 1
                else:
                    print(f"  ⚠️ 框架不匹配，预期: {test_case['expected_framework']}")
            else:
                print("  ❌ 未返回结果")

        except (ImportError, AttributeError, RuntimeError) as exc:
            print(f"  ❗ 测试失败: {str(exc)}")

    return successful_tests, len(test_cases)


def _test_crisis_detection(knowledge_service):
    """测试危机检测功能."""
    crisis_inputs = [
        "我不想活了，感觉没有意义",
        "想要伤害自己",
        "活着太痛苦了，想要结束",
    ]

    crisis_detected = 0

    for crisis_input in crisis_inputs:
        print(f"\n输入: {crisis_input}")

        try:
            result = knowledge_service.analyze_user_input(crisis_input)

            if result and result.framework == "危机干预":
                print("  ✅ 正确识别为危机情况")
                print(f"  🆘 回应: {result.immediate_response}...")
                crisis_detected += 1
            else:
                print("  ❌ 未能识别危机情况")

        except (ImportError, AttributeError, RuntimeError) as exc:
            print(f"  ❗ 测试失败: {str(exc)}")

    return crisis_detected


def _test_framework_info(knowledge_service):
    """测试框架信息获取."""
    frameworks = ["CBT", "正念疗法", "人际关系疗法", "积极心理学"]

    for framework in frameworks:
        try:
            info = knowledge_service.get_framework_info(framework)
            if info:
                print(f"  ✅ {framework}: {info['name']} - {info['description']}...")
            else:
                print(f"  ❌ {framework}: 未找到信息")

        except (ImportError, AttributeError, RuntimeError) as exc:
            print(f"  ❗ 获取框架信息失败: {str(exc)}")


def _test_safety_guidelines(knowledge_service):
    """测试安全指南."""
    try:
        safety_guide = knowledge_service.get_safety_guidelines()

        print(f"  ✅ 免责声明: {safety_guide.get('disclaimer', '未设置')}...")
        print(f"  📞 危机热线: {safety_guide.get('crisis_hotline', '未设置')}")
        print(f"  🚫 安全边界: {len(safety_guide.get('boundaries', []))} 项")

        return len(safety_guide) >= 4

    except (ImportError, AttributeError, RuntimeError) as exc:
        print(f"  ❗ 获取安全指南失败: {str(exc)}")
        return False


def _test_integration(knowledge_service):
    """测试集成功能."""
    original_response = "我能感受到你的担心和不安。"
    user_input = "我最近很焦虑"

    try:
        enhanced_response = knowledge_service.enhance_response_with_knowledge(
            original_response, user_input, "焦虑"
        )

        print(f"  原始回应: {original_response}")
        print(f"  增强回应: {enhanced_response}")
        print("  ✅ 集成测试成功")
        return True

    except (ImportError, AttributeError, RuntimeError) as exc:
        print(f"  ❗ 集成测试失败: {str(exc)}")
        return False


def test_knowledge_service():
    """知识库服务综合测试."""
    try:
        knowledge_service = KnowledgeService()

        # 基础功能测试
        print_separator("测试用例结果")
        successful_tests, total_tests = _test_basic_functionality(knowledge_service)

        # 危机检测测试
        print_separator("危机检测测试")
        crisis_detected = _test_crisis_detection(knowledge_service)

        # 框架信息测试
        print_separator("框架信息测试")
        _test_framework_info(knowledge_service)

        # 安全指南测试
        print_separator("安全指南测试")
        safety_test = _test_safety_guidelines(knowledge_service)

        # 集成测试
        print_separator("集成测试")
        integration_test = _test_integration(knowledge_service)

        # 结果汇总
        print_separator("知识库服务测试完成")
        print(f"框架匹配: {successful_tests}/{total_tests} 通过")
        print(f"危机检测: {crisis_detected}/3 通过")
        print(f"安全指南: {'通过' if safety_test else '失败'}")
        print(f"集成测试: {'通过' if integration_test else '失败'}")

        return True

    except (ImportError, AttributeError) as exc:
        print(f"❗ 初始化失败: {str(exc)}")
        return False


def main():
    """主测试流程."""
    print(f"知识库服务测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if "KnowledgeService" not in globals():
        print("❌ 无法导入KnowledgeService，跳过测试")
        return 1

    success = test_knowledge_service()

    if success:
        print("🎉 知识库服务测试完成")
        return 0
    else:
        print("⚠️ 知识库服务测试失败")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
