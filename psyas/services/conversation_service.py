# -*- coding: utf-8 -*-
"""对话服务 (ConversationService) - 处理用户输入、返回引导回复."""
import random
from typing import Dict, Optional

from sqlalchemy.exc import SQLAlchemyError

from psyas.database import db
from psyas.models.conversation import Conversation
from psyas.models.guide_question import GuideQuestion
from psyas.user.models import User


class ConversationService:
    """对话服务类，负责处理用户输入和生成引导回复."""

    def __init__(self):
        """初始化对话服务."""
        self.emotion_keywords = {
            "焦虑": ["担心", "紧张", "害怕", "不安", "恐惧", "焦虑"],
            "抑郁": ["难过", "沮丧", "失落", "绝望", "无助", "悲伤"],
            "愤怒": ["生气", "愤怒", "恼火", "烦躁", "气愤", "愤怒"],
            "压力": ["压力", "负担", "疲惫", "累", "忙碌", "疲劳"],
            "快乐": ["开心", "高兴", "快乐", "兴奋", "满意", "幸福"],
        }

    def process_user_input(self, user_id: int, user_input: str) -> Dict:
        """
        处理用户输入，生成助手回复并保存对话记录.

        Args:
            user_id: 用户ID
            user_input: 用户输入的文本

        Returns:
            Dict: 包含助手回复和对话ID的字典
        """
        try:
            # 1. 验证用户存在
            user = User.query.get(user_id)
            if not user:
                return {"error": "用户不存在", "code": 404}

            # 2. 分析用户输入，生成引导回复
            assistant_response = self._generate_assistant_response(user_input)

            # 3. 保存对话记录
            conversation = Conversation.create(
                user_id=user_id,
                user_input=user_input.strip(),
                assistant_response=assistant_response,
                is_analyzed=False,
            )
            db.session.add(conversation)
            db.session.commit()

            return {
                "code": 200,
                "message": "对话处理成功",
                "data": {
                    "conversation_id": conversation.id,
                    "assistant_response": assistant_response,
                    "user_input": user_input,
                    "created_at": conversation.created_at.isoformat(),
                },
            }

        except SQLAlchemyError as exc:
            db.session.rollback()
            return {"error": f"数据库操作失败: {str(exc)}", "code": 500}
        except (ValueError, TypeError) as exc:
            return {"error": f"参数错误: {str(exc)}", "code": 400}

    def _generate_assistant_response(self, user_input: str) -> str:
        """
        根据用户输入生成引导回复.

        Args:
            user_input: 用户输入的文本

        Returns:
            str: 生成的助手回复
        """
        # 1. 检测情绪关键词
        detected_emotion = self._detect_emotion(user_input)

        # 2. 根据情绪生成基础回复
        if detected_emotion:
            base_response = self._get_emotion_response(detected_emotion)
        else:
            base_response = "我理解你想要分享的内容。"

        # 3. 添加引导问题
        guide_question = self._get_guide_question(detected_emotion or "通用")

        return f"{base_response} {guide_question}"

    def _detect_emotion(self, text: str) -> Optional[str]:
        """
        检测文本中的情绪关键词.

        Args:
            text: 输入文本

        Returns:
            Optional[str]: 检测到的情绪类型，如果没有检测到则返回None
        """
        text_lower = text.lower()
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return emotion
        return None

    def _get_emotion_response(self, emotion: str) -> str:
        """
        根据情绪类型生成对应的回复.

        Args:
            emotion: 情绪类型

        Returns:
            str: 情绪回复
        """
        emotion_responses = {
            "焦虑": "我能感受到你的担心和不安。",
            "抑郁": "我听到了你内心的难过，这些感受很真实。",
            "愤怒": "你的愤怒情绪我能理解，这种感觉一定很难受。",
            "压力": "听起来你承受了很多压力，这确实不容易。",
            "快乐": "很高兴听到你有开心的事情！",
        }
        return emotion_responses.get(emotion, "我理解你的感受。")

    def _get_guide_question(self, scene: str) -> str:
        """
        获取引导问题.

        Args:
            scene: 场景分类

        Returns:
            str: 引导问题
        """
        # 从数据库获取引导问题
        guide_questions = GuideQuestion.query.filter_by(scene=scene).all()

        if guide_questions:
            # 随机选择一个引导问题
            selected_question = random.choice(guide_questions)
            return selected_question.question_text
        else:
            # 默认引导问题
            default_questions = [
                "能告诉我更多关于这个情况的细节吗？",
                "这种感受对你来说意味着什么？",
                "你觉得什么可能会帮助改善这种情况？",
                "在这种情况下，你通常会怎么做？",
            ]
            return random.choice(default_questions)

    def get_user_conversations(self, user_id: int, limit: int = 10) -> Dict:
        """
        获取用户的对话历史.

        Args:
            user_id: 用户ID
            limit: 返回的对话数量限制

        Returns:
            Dict: 对话历史数据
        """
        try:
            conversations = (
                Conversation.query.filter_by(user_id=user_id)
                .order_by(Conversation.created_at.desc())
                .limit(limit)
                .all()
            )

            conversation_list = []
            for conv in conversations:
                conversation_list.append(
                    {
                        "id": conv.id,
                        "user_input": conv.user_input,
                        "assistant_response": conv.assistant_response,
                        "created_at": conv.created_at.isoformat(),
                        "is_analyzed": conv.is_analyzed,
                    }
                )

            return {
                "code": 200,
                "message": "获取对话历史成功",
                "data": {
                    "conversations": conversation_list,
                    "total": len(conversation_list),
                },
            }

        except SQLAlchemyError as exc:
            return {"error": f"数据库查询失败: {str(exc)}", "code": 500}
