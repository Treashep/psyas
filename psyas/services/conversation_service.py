# -*- coding: utf-8 -*-
"""对话服务 (ConversationService) - 处理用户输入、返回引导回复.

升级为Agent架构，但保持原有接口完全兼容。
"""
import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from sqlalchemy.exc import SQLAlchemyError

from psyas.database import db
from psyas.models.conversation import Conversation
from psyas.models.guide_question import GuideQuestion
from psyas.user.models import User

# 尝试导入知识库服务，如果导入失败则使用基础模式
try:
    from psyas.services.knowledge_service import KnowledgeService

    KNOWLEDGE_SERVICE_AVAILABLE = True
except ImportError:
    KNOWLEDGE_SERVICE_AVAILABLE = False
    print("警告：知识库服务不可用，将使用基础模式")

# 尝试导入MCP工具注册表
try:
    from psyas.mcp.tool_registry import MCPToolRegistry

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("警告：MCP工具不可用，将使用基础模式")


@dataclass
class AgentResult:
    """Agent处理结果."""

    response: str
    emotion: Optional[str] = None
    confidence: float = 0.0
    source: str = "basic"
    has_memory: bool = False


class ConversationService:
    """对话服务类，负责处理用户输入和生成引导回复.

    已升级为Agent架构，但保持原有接口完全兼容：
    - 感知模块：情绪检测 + 记忆增强
    - 推理模块：知识库分析 + 历史上下文
    - 行动模块：回复生成 + 个性化
    - 记忆模块：对话历史 + 连续性
    """

    def __init__(self):
        """初始化对话服务（Agent版本）."""
        self.emotion_keywords = {
            "焦虑": ["担心", "紧张", "害怕", "不安", "恐惧", "焦虑"],
            "抑郁": ["难过", "沮丧", "失落", "绝望", "无助", "悲伤"],
            "愤怒": ["生气", "愤怒", "恼火", "烦躁", "气愤", "愤怒"],
            "压力": ["压力", "负担", "疲惫", "累", "忙碌", "疲劳"],
            "快乐": ["开心", "高兴", "快乐", "兴奋", "满意", "幸福"],
        }

        # 初始化知识库服务（如果可用）
        if KNOWLEDGE_SERVICE_AVAILABLE:
            try:
                self.knowledge_service = KnowledgeService()
                print("✅ Agent已启用知识库服务")
            except (ImportError, AttributeError) as e:
                self.knowledge_service = None
                print(f"⚠️ 知识库服务初始化失败: {e}")
        else:
            self.knowledge_service = None

        # 初始化MCP工具注册表（如果可用）
        if MCP_AVAILABLE:
            try:
                self.mcp_registry = MCPToolRegistry()
                print("✅ Agent已启用MCP工具系统")
            except (ImportError, AttributeError, RuntimeError) as e:
                self.mcp_registry = None
                print(f"⚠️ MCP工具初始化失败: {e}")
        else:
            self.mcp_registry = None

        # Agent记忆缓存（简单版本）
        self._memory_cache = {}

    def process_user_input(self, user_id: int, user_input: str) -> Dict:
        """
        Agent主流程：处理用户输入，生成助手回复并保存对话记录.

        Agent化改造：
        1. 感知阶段：情绪检测 + 记忆增强
        2. 推理阶段：知识库分析 + 历史上下文
        3. 行动阶段：回复生成 + 个性化
        4. 记忆阶段：保存对话 + 更新记忆

        Args:
            user_id: 用户ID
            user_input: 用户输入的文本

        Returns:
            Dict: 包含助手回复和Agent信息的字典
        """
        try:
            # 1. 验证用户存在
            user = User.query.get(user_id)
            if not user:
                return {"error": "用户不存在", "code": 404}

            # === Agent四步流程 ===

            # 2. 感知阶段：理解用户输入（重用+增强现有逻辑）
            perception = self._agent_perceive(user_input)

            # 3. 记忆检索：获取用户历史上下文
            memory_context = self._agent_get_memory(user_id)

            # 4. 推理和行动：生成回复（重用+增强现有逻辑）
            agent_result = self._agent_reason_and_respond(
                user_input, perception, memory_context
            )

            # 5. 记忆更新：保存对话记录
            conversation = self._save_conversation(
                user_id, user_input, agent_result.response
            )

            # 6. 更新记忆缓存
            self._agent_update_memory(user_id, user_input, agent_result)

            return {
                "code": 200,
                "message": "Agent处理成功",
                "data": {
                    "conversation_id": conversation.id,
                    "assistant_response": agent_result.response,
                    "user_input": user_input,
                    "created_at": conversation.created_at.isoformat(),
                    # === Agent增强信息 ===
                    "agent_info": {
                        "detected_emotion": agent_result.emotion,
                        "confidence": agent_result.confidence,
                        "response_source": agent_result.source,
                        "has_memory": agent_result.has_memory,
                    },
                },
            }

        except SQLAlchemyError as exc:
            db.session.rollback()
            return {"error": f"数据库操作失败: {str(exc)}", "code": 500}
        except (ValueError, TypeError) as exc:
            return {"error": f"参数错误: {str(exc)}", "code": 400}

    # === 兼容性接口（保持原有API不变） ===

    @classmethod
    def create_conversation(cls, user_id: int, user_input: str) -> Dict:
        """
        创建对话（原有接口，完全兼容）.

        这个方法保持与原有ConversationService.create_conversation()完全兼容，
        但内部使用Agent处理。

        Args:
            user_id: 用户ID
            user_input: 用户输入

        Returns:
            Dict: 对话结果，包含Agent增强信息
        """
        service = cls()
        return service.process_user_input(user_id, user_input)

    def _agent_perceive(self, user_input: str) -> Dict:
        """
        Agent感知模块：理解用户输入.

        重用现有的_detect_emotion，但增加更多信息
        """
        emotion = self._detect_emotion(user_input)  # 重用现有方法

        # 简单的置信度计算
        confidence = 0.3  # 基础置信度
        if emotion:
            # 如果检测到情绪，增加置信度
            emotion_keywords = self.emotion_keywords.get(emotion, [])
            matched_keywords = sum(
                1 for keyword in emotion_keywords if keyword in user_input.lower()
            )
            confidence = min(0.5 + matched_keywords * 0.2, 1.0)

        return {
            "emotion": emotion,
            "confidence": confidence,
            "text_length": len(user_input),
            "keywords": self._extract_keywords(user_input),
        }

    def _agent_get_memory(self, user_id: int) -> List[Dict]:
        """
        Agent记忆模块：获取用户历史上下文.

        重用现有的get_user_conversations逻辑
        """
        # 检查缓存
        if user_id in self._memory_cache:
            return self._memory_cache[user_id]

        try:
            # 获取最近3条对话作为记忆上下文
            recent_conversations = (
                Conversation.query.filter_by(user_id=user_id)
                .order_by(Conversation.created_at.desc())
                .limit(3)
                .all()
            )

            memory_context = []
            for conv in recent_conversations:
                memory_context.append(
                    {
                        "user_input": conv.user_input,
                        "assistant_response": conv.assistant_response,
                        "created_at": conv.created_at.isoformat(),
                        "emotion": self._detect_emotion(
                            conv.user_input
                        ),  # 分析历史情绪
                    }
                )

            # 缓存记忆（简单版本）
            self._memory_cache[user_id] = memory_context
            return memory_context

        except SQLAlchemyError:
            return []  # 如果获取失败，返回空记忆

    def _agent_reason_and_respond(
        self, user_input: str, perception: Dict, memory_context: List[Dict]
    ) -> AgentResult:
        """
        Agent推理和行动模块：生成回复.

        重用现有的_generate_assistant_response逻辑，但增加记忆增强
        """
        detected_emotion = perception.get("emotion")
        confidence = perception.get("confidence", 0.0)

        # === 记忆增强：检查历史情绪模式 ===
        enhanced_emotion = self._enhance_emotion_with_memory(
            detected_emotion, memory_context
        )

        # 尝试使用MCP工具
        mcp_result = self._try_mcp_response(
            user_input, enhanced_emotion, detected_emotion, memory_context
        )
        if mcp_result:
            return mcp_result

        # 回退到知识库逻辑
        knowledge_result = self._try_knowledge_response(
            user_input, enhanced_emotion, detected_emotion, memory_context
        )
        if knowledge_result:
            return knowledge_result

        # 使用基础回复逻辑
        return self._generate_basic_response(
            enhanced_emotion, detected_emotion, confidence, memory_context
        )

    def _try_mcp_response(
        self,
        user_input: str,
        enhanced_emotion: Optional[str],
        detected_emotion: Optional[str],
        memory_context: List[Dict],
    ) -> Optional[AgentResult]:
        """尝试使用MCP工具生成回复."""
        if not self.mcp_registry:
            return None

        try:
            import asyncio

            loop = asyncio.get_event_loop()

            if loop.is_running():
                print("MCP工具可用，但当前在同步上下文中")
                return None

            mcp_result = loop.run_until_complete(
                self.mcp_registry.call_tool(
                    "emotion_analysis",
                    {
                        "text": user_input,
                        "context": {"emotion": enhanced_emotion or detected_emotion},
                    },
                )
            )

            if mcp_result.success and mcp_result.data.get("confidence", 0) > 0.3:
                return self._build_mcp_response(
                    mcp_result.data, enhanced_emotion, detected_emotion, memory_context
                )

        except (RuntimeError, AttributeError, ImportError) as e:
            print(f"MCP工具调用失败: {e}")

        return None

    def _try_knowledge_response(
        self,
        user_input: str,
        enhanced_emotion: Optional[str],
        detected_emotion: Optional[str],
        memory_context: List[Dict],
    ) -> Optional[AgentResult]:
        """尝试使用知识库生成回复."""
        if not self.knowledge_service:
            return None

        try:
            knowledge_match = self.knowledge_service.analyze_user_input(
                user_input, enhanced_emotion or detected_emotion
            )

            if knowledge_match and knowledge_match.confidence > 0.3:
                return self._build_knowledge_response(
                    knowledge_match, enhanced_emotion, detected_emotion, memory_context
                )

        except (ImportError, AttributeError, RuntimeError) as e:
            print(f"知识库服务调用失败: {e}")

        return None

    def _build_mcp_response(
        self,
        mcp_data: Dict,
        enhanced_emotion: Optional[str],
        detected_emotion: Optional[str],
        memory_context: List[Dict],
    ) -> AgentResult:
        """构建MCP增强回复."""
        enhanced_response = mcp_data.get("immediate_response", "")

        if memory_context:
            enhanced_response = self._add_memory_continuity(
                enhanced_response, memory_context
            )

        follow_up_questions = mcp_data.get("follow_up_questions", [])
        if follow_up_questions:
            enhanced_response += f" {follow_up_questions[0]}"

        return AgentResult(
            response=enhanced_response,
            emotion=enhanced_emotion or detected_emotion,
            confidence=mcp_data.get("confidence", 0.5),
            source="mcp_enhanced",
            has_memory=len(memory_context) > 0,
        )

    def _build_knowledge_response(
        self,
        knowledge_match,
        enhanced_emotion: Optional[str],
        detected_emotion: Optional[str],
        memory_context: List[Dict],
    ) -> AgentResult:
        """构建知识库增强回复."""
        enhanced_response = knowledge_match.immediate_response

        if memory_context:
            enhanced_response = self._add_memory_continuity(
                enhanced_response, memory_context
            )

        if knowledge_match.follow_up_questions:
            follow_up = knowledge_match.follow_up_questions[0]
            enhanced_response += f" {follow_up}"

        return AgentResult(
            response=enhanced_response,
            emotion=enhanced_emotion or detected_emotion,
            confidence=knowledge_match.confidence,
            source="knowledge_enhanced",
            has_memory=len(memory_context) > 0,
        )

    def _generate_basic_response(
        self,
        enhanced_emotion: Optional[str],
        detected_emotion: Optional[str],
        confidence: float,
        memory_context: List[Dict],
    ) -> AgentResult:
        """生成基础回复."""
        if enhanced_emotion or detected_emotion:
            base_response = self._get_emotion_response(
                enhanced_emotion or detected_emotion
            )
        else:
            base_response = "我理解你想要分享的内容。"

        guide_question = self._get_guide_question(
            (enhanced_emotion or detected_emotion) or "通用"
        )
        final_response = f"{base_response} {guide_question}"

        if memory_context:
            final_response = self._add_memory_continuity(final_response, memory_context)

        return AgentResult(
            response=final_response,
            emotion=enhanced_emotion or detected_emotion,
            confidence=confidence,
            source="basic_enhanced",
            has_memory=len(memory_context) > 0,
        )

    def _agent_update_memory(
        self, user_id: int, user_input: str, agent_result: AgentResult
    ):
        """Agent记忆更新：更新缓存记忆."""
        if user_id in self._memory_cache:
            # 更新记忆缓存
            memory = self._memory_cache[user_id]

            # 添加新的对话到记忆中
            new_memory = {
                "user_input": user_input,
                "assistant_response": agent_result.response,
                "created_at": "just_now",
                "emotion": agent_result.emotion,
            }
            memory.insert(0, new_memory)

            # 保持最近3条记录
            self._memory_cache[user_id] = memory[:3]

    def _enhance_emotion_with_memory(
        self, current_emotion: Optional[str], memory_context: List[Dict]
    ) -> Optional[str]:
        """
        记忆增强：根据历史对话优化情绪检测.

        新功能：如果当前没检测到情绪，但历史中有相关情绪，可以推断
        """
        if current_emotion or not memory_context:
            return current_emotion

        # 分析最近的情绪模式
        recent_emotions = []
        for conv in memory_context[:2]:  # 只看最近2条
            emotion = conv.get("emotion")
            if emotion:
                recent_emotions.append(emotion)

        # 如果最近的对话中有情绪模式，可能仍在持续
        if recent_emotions:
            most_recent_emotion = recent_emotions[0]  # 最新的情绪
            return most_recent_emotion

        return current_emotion

    def _add_memory_continuity(self, response: str, memory_context: List[Dict]) -> str:
        """
        增加记忆连续性：让回复体现对历史的记忆.

        新功能：让Agent显得"记得"用户之前说过的话
        """
        if not memory_context:
            return response

        # 简单的连续性短语
        continuity_phrases = [
            "结合我们之前聊过的，",
            "继续我们上次的话题，",
            "基于你之前提到的情况，",
            "考虑到你之前的分享，",
        ]

        # 30%概率添加连续性短语
        if random.random() < 0.3 and len(memory_context) > 0:
            phrase = random.choice(continuity_phrases)
            response = phrase + response.lower()

        return response

    def _extract_keywords(self, text: str) -> List[str]:
        """提取简单关键词（新功能）."""
        keywords = []
        text_lower = text.lower()

        # 提取情绪关键词
        for emotion, emotion_keywords in self.emotion_keywords.items():
            for keyword in emotion_keywords:
                if keyword in text_lower:
                    keywords.append(keyword)

        return keywords

    def _save_conversation(
        self, user_id: int, user_input: str, assistant_response: str
    ) -> Conversation:
        """保存对话记录（重用现有逻辑）."""
        conversation = Conversation.create(
            user_id=user_id,
            user_input=user_input.strip(),
            assistant_response=assistant_response,
            is_analyzed=False,
        )
        db.session.add(conversation)
        db.session.commit()
        return conversation

    # === 原有方法（保持不变，用于Agent内部调用） ===

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

        # 2. 尝试使用知识库服务增强回复
        if self.knowledge_service:
            try:
                knowledge_match = self.knowledge_service.analyze_user_input(
                    user_input, detected_emotion
                )

                if knowledge_match and knowledge_match.confidence > 0.3:
                    # 使用知识库增强的回复
                    enhanced_response = knowledge_match.immediate_response

                    # 添加后续引导问题
                    if knowledge_match.follow_up_questions:
                        follow_up = knowledge_match.follow_up_questions[0]
                        enhanced_response += f" {follow_up}"

                    return enhanced_response

            except (ImportError, AttributeError, RuntimeError) as e:
                print(f"知识库服务调用失败，使用基础模式: {e}")

        # 3. 基础模式：根据情绪生成基础回复
        if detected_emotion:
            base_response = self._get_emotion_response(detected_emotion)
        else:
            base_response = "我理解你想要分享的内容。"

        # 4. 添加引导问题
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
