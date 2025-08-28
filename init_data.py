# -*- coding: utf-8 -*-
"""数据初始化脚本 - 添加基础引导问题和测试用户."""
from psyas.app import create_app
from psyas.database import db
from psyas.models.guide_question import GuideQuestion
from psyas.user.models import User


def init_guide_questions():
    """初始化引导问题数据."""
    guide_questions = [
        # 焦虑相关
        {
            "scene": "焦虑",
            "question_text": "能告诉我是什么具体的情况让你感到焦虑吗？",
            "priority": 1,
        },
        {
            "scene": "焦虑",
            "question_text": "这种焦虑的感觉从什么时候开始的？",
            "priority": 2,
        },
        {
            "scene": "焦虑",
            "question_text": "当你感到焦虑时，你的身体有什么反应？",
            "priority": 1,
        },
        # 抑郁相关
        {
            "scene": "抑郁",
            "question_text": "这种低落的情绪持续了多长时间？",
            "priority": 1,
        },
        {
            "scene": "抑郁",
            "question_text": "有什么事情能让你感觉好一些吗？",
            "priority": 2,
        },
        {
            "scene": "抑郁",
            "question_text": "你觉得这种感受对你的日常生活有什么影响？",
            "priority": 1,
        },
        # 愤怒相关
        {
            "scene": "愤怒",
            "question_text": "能说说让你感到愤怒的具体原因吗？",
            "priority": 1,
        },
        {
            "scene": "愤怒",
            "question_text": "当你愤怒的时候，你通常会做什么？",
            "priority": 2,
        },
        {"scene": "愤怒", "question_text": "你觉得这种愤怒是合理的吗？", "priority": 2},
        # 压力相关
        {"scene": "压力", "question_text": "这些压力主要来自哪些方面？", "priority": 1},
        {"scene": "压力", "question_text": "你平时是如何应对压力的？", "priority": 2},
        {
            "scene": "压力",
            "question_text": "有没有想过什么方法可以减轻这些压力？",
            "priority": 1,
        },
        # 快乐相关
        {
            "scene": "快乐",
            "question_text": "能分享一下是什么让你这么开心吗？",
            "priority": 1,
        },
        {
            "scene": "快乐",
            "question_text": "这种快乐的感觉对你来说意味着什么？",
            "priority": 2,
        },
        # 通用问题
        {
            "scene": "通用",
            "question_text": "能告诉我更多关于这个情况的细节吗？",
            "priority": 1,
        },
        {
            "scene": "通用",
            "question_text": "这种感受对你来说意味着什么？",
            "priority": 2,
        },
        {
            "scene": "通用",
            "question_text": "你觉得什么可能会帮助改善这种情况？",
            "priority": 2,
        },
        {
            "scene": "通用",
            "question_text": "在这种情况下，你通常会怎么做？",
            "priority": 3,
        },
        {
            "scene": "通用",
            "question_text": "有什么是你特别想要分享或探讨的吗？",
            "priority": 3,
        },
        # 工作压力相关
        {
            "scene": "工作压力",
            "question_text": "工作中哪些方面让你感到压力最大？",
            "priority": 1,
        },
        {
            "scene": "工作压力",
            "question_text": "你觉得这种工作压力是可以改变的吗？",
            "priority": 2,
        },
        # 家庭关系相关
        {
            "scene": "家庭关系",
            "question_text": "在家庭关系中，什么让你最困扰？",
            "priority": 1,
        },
        {
            "scene": "家庭关系",
            "question_text": "你希望家庭关系能有什么样的改变？",
            "priority": 2,
        },
        # 人际关系相关
        {
            "scene": "人际关系",
            "question_text": "在人际交往中，你遇到的主要困难是什么？",
            "priority": 1,
        },
        {
            "scene": "人际关系",
            "question_text": "你觉得什么样的人际关系对你来说是理想的？",
            "priority": 2,
        },
    ]

    print("正在添加引导问题...")
    added_count = 0

    for question_data in guide_questions:
        # 检查是否已存在相同的问题
        existing = GuideQuestion.query.filter_by(
            scene=question_data["scene"], question_text=question_data["question_text"]
        ).first()

        if not existing:
            question = GuideQuestion(**question_data)
            db.session.add(question)
            added_count += 1
            print(
                f"添加问题: [{question_data['scene']}] {question_data['question_text']}"
            )

    db.session.commit()
    print(f"成功添加 {added_count} 个引导问题")


def init_test_user():
    """初始化测试用户."""
    print("正在检查测试用户...")

    # 检查是否已存在测试用户
    existing_user = User.query.filter_by(username="testuser").first()
    if existing_user:
        print(f"测试用户已存在: ID={existing_user.id}, 用户名={existing_user.username}")
        return existing_user.id

    # 创建测试用户
    test_user = User(
        username="testuser",
        email="test@psyas.com",
        first_name="测试",
        last_name="用户",
        active=True,
        is_admin=False,
    )
    test_user.password = "testpassword"  # 会自动hash

    db.session.add(test_user)
    db.session.commit()

    print(f"成功创建测试用户: ID={test_user.id}, 用户名={test_user.username}")
    return test_user.id


def main():
    """主初始化函数."""
    print("=" * 60)
    print(" psyas 项目数据初始化")
    print("=" * 60)

    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 创建表（如果不存在）
        print("正在检查数据库表...")
        db.create_all()

        # 初始化引导问题
        init_guide_questions()

        # 初始化测试用户
        user_id = init_test_user()

        print("\n" + "=" * 60)
        print(" 初始化完成!")
        print("=" * 60)
        print(f"测试用户ID: {user_id}")
        print("引导问题数量:", GuideQuestion.query.count())
        print("\n可以开始测试业务接口了！")
        print("运行测试: python test_business_apis.py")


if __name__ == "__main__":
    main()
