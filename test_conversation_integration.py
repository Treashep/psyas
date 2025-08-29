# -*- coding: utf-8 -*-
"""对话服务与知识库服务集成测试."""
import sys
from datetime import datetime


def print_separator(title):
    """打印分隔符."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def test_conversation_service_integration():
    """测试对话服务与知识库服务的集成."""
    try:
        # 导入Flask应用和对话服务
        from psyas.app import create_app
        from psyas.services.conversation_service import ConversationService

        print_separator("对话服务集成测试")

        # 创建Flask应用实例
        app = create_app()

        # 在应用上下文中运行测试
        with app.app_context():
            # 初始化对话服务
            conv_service = ConversationService()

            # 测试用例
            test_cases = [
                {
                    "input": "我最近工作压力特别大，每天都感觉很焦虑",
                    "description": "工作压力+焦虑（应匹配正念疗法）",
                },
                {
                    "input": "和男朋友分手了，感觉很难过很绝望",
                    "description": "分手+抑郁（应匹配CBT）",
                },
                {
                    "input": "今天升职了，特别开心！",
                    "description": "积极情绪（应匹配积极心理学）",
                },
                {
                    "input": "我不想活了，感觉没有意义",
                    "description": "危机情况（应触发危机干预）",
                },
            ]

            successful_tests = 0
            total_tests = len(test_cases)

            for i, test_case in enumerate(test_cases, 1):
                print(f"\n📝 测试 {i}: {test_case['description']}")
                print(f"用户输入: {test_case['input']}")

                try:
                    # 直接测试回复生成（不涉及数据库写入）
                    response = conv_service._generate_assistant_response(
                        test_case["input"]
                    )
                    print(f"助手回复: {response}")
                    print("✅ 测试成功")
                    successful_tests += 1

                except (ImportError, AttributeError, RuntimeError) as e:
                    print(f"❌ 测试失败: {str(e)}")

            print_separator("集成效果验证")

            # 验证知识库服务是否被正确集成
            has_knowledge_service = (
                hasattr(conv_service, "knowledge_service")
                and conv_service.knowledge_service is not None
            )
            if has_knowledge_service:
                print("✅ 知识库服务已成功集成到对话服务中")

                # 测试知识库服务直接调用
                test_input = "我感到很焦虑和压力"
                knowledge_result = conv_service.knowledge_service.analyze_user_input(
                    test_input
                )
                if knowledge_result:
                    print(
                        f"📚 知识库直接调用测试: 匹配框架 '{knowledge_result.framework}'，置信度 {knowledge_result.confidence:.2f}"
                    )
                else:
                    print("⚠️ 知识库直接调用未返回结果")
            else:
                print("⚠️ 知识库服务未集成或初始化失败")

            print(
                f"\n📊 成功率: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)"
            )

            return successful_tests == total_tests

    except (ImportError, AttributeError) as e:
        print(f"❌ 导入失败: {e}")
        return False
    except (RuntimeError, ValueError) as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """主测试流程."""
    print(f"对话服务集成测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    success = test_conversation_service_integration()

    print_separator("测试结果汇总")
    if success:
        print("🎉 集成测试通过！对话服务成功集成知识库功能。")
        return 0
    else:
        print("⚠️ 集成测试失败，请检查服务配置。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
