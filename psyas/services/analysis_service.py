# -*- coding: utf-8 -*-
"""分析服务 (AnalysisService) - 简单提取标签和结论."""
from collections import Counter
from typing import Dict, Optional

from sqlalchemy.exc import SQLAlchemyError

from psyas.database import db
from psyas.models.analysis import Analysis
from psyas.models.conversation import Conversation
from psyas.user.models import User


class AnalysisService:
    """分析服务类，负责分析用户对话并生成心理分析结果."""

    def __init__(self):
        """初始化分析服务."""
        # 情绪关键词词典
        self.emotion_keywords = {
            "焦虑": ["担心", "紧张", "害怕", "不安", "恐惧", "焦虑", "忧虑"],
            "抑郁": ["难过", "沮丧", "失落", "绝望", "无助", "悲伤", "低落"],
            "愤怒": ["生气", "愤怒", "恼火", "烦躁", "气愤", "恨", "愤恨"],
            "压力": ["压力", "负担", "疲惫", "累", "忙碌", "疲劳", "重担"],
            "快乐": ["开心", "高兴", "快乐", "兴奋", "满意", "幸福", "愉快"],
            "孤独": ["孤独", "独自", "没人", "孤单", "寂寞", "一个人"],
        }

        # 问题关键词词典
        self.issue_keywords = {
            "家庭关系": [
                "父母",
                "家人",
                "家庭",
                "爸爸",
                "妈妈",
                "兄弟",
                "姐妹",
                "家里",
            ],
            "工作压力": ["工作", "上班", "同事", "老板", "职场", "加班", "任务"],
            "学习问题": ["学习", "考试", "学校", "老师", "成绩", "作业", "学业"],
            "情感关系": ["恋人", "男朋友", "女朋友", "感情", "恋爱", "分手", "约会"],
            "人际关系": ["朋友", "社交", "人际", "交流", "沟通", "关系", "社会"],
            "自我认知": ["自己", "自我", "性格", "能力", "自信", "自尊", "价值"],
        }

    def analyze_user_conversations(
        self, user_id: int, conversation_id: Optional[int] = None
    ) -> Dict:
        """
        分析用户对话，生成心理分析结果.

        Args:
            user_id: 用户ID
            conversation_id: 特定对话ID（如果为None则分析最新对话）

        Returns:
            Dict: 分析结果
        """
        try:
            # 1. 验证用户存在
            user = User.query.get(user_id)
            if not user:
                return {"error": "用户不存在", "code": 404}

            # 2. 获取要分析的对话
            if conversation_id:
                conversation = Conversation.query.filter_by(
                    id=conversation_id, user_id=user_id
                ).first()
                if not conversation:
                    return {"error": "对话不存在", "code": 404}
            else:
                # 获取用户最新的未分析对话
                conversation = (
                    Conversation.query.filter_by(user_id=user_id, is_analyzed=False)
                    .order_by(Conversation.created_at.desc())
                    .first()
                )
                if not conversation:
                    return {"error": "没有需要分析的对话", "code": 404}

            # 3. 进行分析
            analysis_result = self._perform_analysis(conversation)

            # 4. 保存分析结果
            analysis = Analysis.create(
                user_id=user_id,
                conversation_id=conversation.id,
                core_issue=analysis_result["core_issue"],
                emotion=analysis_result["emotion"],
                simple_conclusion=analysis_result["conclusion"],
            )
            db.session.add(analysis)

            # 标记对话已分析
            conversation.is_analyzed = True

            db.session.commit()

            return {
                "code": 200,
                "message": "分析完成",
                "data": {
                    "analysis_id": analysis.id,
                    "core_issue": analysis.core_issue,
                    "emotion": analysis.emotion,
                    "conclusion": analysis.simple_conclusion,
                    "analyzed_at": analysis.analyzed_at.isoformat(),
                    "conversation_id": conversation.id,
                },
            }

        except SQLAlchemyError as exc:
            db.session.rollback()
            return {"error": f"数据库操作失败: {str(exc)}", "code": 500}
        except (ValueError, TypeError) as exc:
            return {"error": f"参数错误: {str(exc)}", "code": 400}

    def get_user_analysis_history(self, user_id: int, limit: int = 10) -> Dict:
        """
        获取用户的分析历史记录.

        Args:
            user_id: 用户ID
            limit: 返回的记录数量限制

        Returns:
            Dict: 分析历史数据
        """
        try:
            analyses = (
                Analysis.query.filter_by(user_id=user_id)
                .order_by(Analysis.analyzed_at.desc())
                .limit(limit)
                .all()
            )

            analysis_list = []
            for analysis in analyses:
                analysis_list.append(
                    {
                        "id": analysis.id,
                        "core_issue": analysis.core_issue,
                        "emotion": analysis.emotion,
                        "conclusion": analysis.simple_conclusion,
                        "analyzed_at": analysis.analyzed_at.isoformat(),
                        "conversation_id": analysis.conversation_id,
                    }
                )

            return {
                "code": 200,
                "message": "获取分析历史成功",
                "data": {"analyses": analysis_list, "total": len(analysis_list)},
            }

        except SQLAlchemyError as exc:
            return {"error": f"数据库查询失败: {str(exc)}", "code": 500}

    def get_analysis_by_id(self, user_id: int, analysis_id: int) -> Dict:
        """
        根据ID获取特定的分析结果.

        Args:
            user_id: 用户ID
            analysis_id: 分析结果ID

        Returns:
            Dict: 分析结果详情
        """
        try:
            analysis = Analysis.query.filter_by(id=analysis_id, user_id=user_id).first()

            if not analysis:
                return {"error": "分析结果不存在", "code": 404}

            return {
                "code": 200,
                "message": "获取分析结果成功",
                "data": {
                    "id": analysis.id,
                    "core_issue": analysis.core_issue,
                    "emotion": analysis.emotion,
                    "conclusion": analysis.simple_conclusion,
                    "analyzed_at": analysis.analyzed_at.isoformat(),
                    "conversation_id": analysis.conversation_id,
                    "user_input": analysis.conversation.user_input,
                    "assistant_response": analysis.conversation.assistant_response,
                },
            }

        except SQLAlchemyError as exc:
            return {"error": f"数据库查询失败: {str(exc)}", "code": 500}

    def _perform_analysis(self, conversation: Conversation) -> Dict:
        """
        对单个对话进行分析.

        Args:
            conversation: 对话对象

        Returns:
            Dict: 分析结果
        """
        user_input = conversation.user_input

        # 1. 情绪分析
        detected_emotion = self._analyze_emotion(user_input)

        # 2. 核心问题识别
        core_issue = self._identify_core_issue(user_input)

        # 3. 生成简单结论
        conclusion = self._generate_conclusion(detected_emotion, core_issue, user_input)

        return {
            "emotion": detected_emotion,
            "core_issue": core_issue,
            "conclusion": conclusion,
        }

    def _analyze_emotion(self, text: str) -> str:
        """
        分析文本中的主要情绪.

        Args:
            text: 输入文本

        Returns:
            str: 检测到的主要情绪
        """
        text_lower = text.lower()
        emotion_counts = Counter()

        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                emotion_counts[emotion] = count

        if emotion_counts:
            return emotion_counts.most_common(1)[0][0]
        else:
            return "中性"

    def _identify_core_issue(self, text: str) -> str:
        """
        识别文本中的核心问题领域.

        Args:
            text: 输入文本

        Returns:
            str: 识别到的核心问题
        """
        text_lower = text.lower()
        issue_counts = Counter()

        for issue, keywords in self.issue_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                issue_counts[issue] = count

        if issue_counts:
            return issue_counts.most_common(1)[0][0]
        else:
            # 基于文本长度和内容特征的简单推断
            if len(text) > 100:
                return "复杂情况"
            elif any(word in text_lower for word in ["怎么办", "不知道", "困惑"]):
                return "决策困难"
            else:
                return "日常分享"

    def _generate_conclusion(self, emotion: str, core_issue: str, text: str) -> str:
        """
        生成简单的分析结论.

        Args:
            emotion: 检测到的情绪
            core_issue: 核心问题
            text: 原始文本

        Returns:
            str: 分析结论
        """
        # 基础模板
        conclusion_parts = []

        # 情绪部分
        if emotion != "中性":
            emotion_templates = {
                "焦虑": "当前表现出一定程度的焦虑情绪",
                "抑郁": "情绪状态偏向低落，需要关注",
                "愤怒": "存在愤怒情绪，可能需要情绪管理",
                "压力": "面临一定的压力，建议适当调节",
                "快乐": "情绪状态良好，保持积极心态",
                "孤独": "可能感受到孤独，建议增加社交活动",
            }
            conclusion_parts.append(
                emotion_templates.get(emotion, f"主要情绪为{emotion}")
            )

        # 问题部分
        if core_issue != "日常分享":
            issue_templates = {
                "家庭关系": "在家庭关系方面需要更多沟通和理解",
                "工作压力": "工作方面的压力需要合理管理和调节",
                "学习问题": "学习相关的困扰需要找到合适的解决方法",
                "情感关系": "情感关系方面需要更多的理解和包容",
                "人际关系": "人际交往方面可以尝试更开放的态度",
                "自我认知": "对自我的认识和接纳是成长的重要部分",
            }
            conclusion_parts.append(
                issue_templates.get(core_issue, f"主要关注{core_issue}相关问题")
            )

        # 建议部分
        if len(text) > 50:
            conclusion_parts.append("建议继续深入探讨，寻找更好的应对方式")

        if not conclusion_parts:
            return "这是一次很好的自我表达，继续保持开放的沟通"

        return "，".join(conclusion_parts) + "。"
