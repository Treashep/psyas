# -*- coding: utf-8 -*-
"""对话服务：处理用户输入、匹配引导问题、存储对话."""
from sqlalchemy.exc import SQLAlchemyError

from psyas.database import db
from psyas.models.conversation import Conversation
from psyas.models.guide_question import GuideQuestion


class ConversationService:
    """对话服务类，处理用户对话和引导问题匹配."""

    @staticmethod
    def create_conversation(user_id, user_input):
        """创建对话记录并返回助手的引导回复."""
        # 1. 判断场景
        scene = ConversationService._judge_scene(user_input)

        # 2. 获取引导问题
        guide_question = (
            GuideQuestion.query.filter_by(scene=scene)
            .order_by(GuideQuestion.priority.desc())
            .first()
        )
        assistant_response = (
            guide_question.question_text
            if guide_question
            else "能和我多说说具体情况吗？"
        )

        # 3. 创建对话记录 - 确保参数与模型定义一致
        try:

            # 使用CRUDMixin的create方法创建对话记录
            new_conversation = Conversation.create(
                user_id=user_id,
                user_input=user_input,
                assistant_response=assistant_response,
            )

            return {
                "assistant_response": assistant_response,
                "conversation_id": new_conversation.id,
            }

        except SQLAlchemyError as exc:
            db.session.rollback()
            print(f"数据库操作失败: {exc}")
            # 返回一个默认响应，避免服务完全中断
            return {
                "assistant_response": assistant_response,
                "conversation_id": None,
            }

    @staticmethod
    def _judge_scene(user_input):
        """基础版：用关键词匹配场景（后续替换为NLP意图识别）.

        :param user_input: 用户输入文本
        :return: 场景标签（如"family_relation""emotion"）
        """
        user_input_lower = user_input.lower()
        # 关键词匹配场景
        if any(
            word in user_input_lower
            for word in ["家里人", "父母", "配偶", "孩子", "家庭"]
        ):
            return "家庭关系"
        elif any(
            word in user_input_lower
            for word in ["烦躁", "焦虑", "开心", "难过", "情绪"]
        ):
            return "情绪"
        elif any(word in user_input_lower for word in ["工作", "加班", "同事", "老板"]):
            return "工作压力"
        else:
            return "default"
