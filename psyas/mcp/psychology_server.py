# -*- coding: utf-8 -*-
"""心理学MCP服务器 - 包装现有的KnowledgeService为MCP工具."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# 重用现有服务
try:
    from psyas.services.knowledge_service import KnowledgeService

    KNOWLEDGE_SERVICE_AVAILABLE = True
except ImportError:
    KNOWLEDGE_SERVICE_AVAILABLE = False
    print("警告：KnowledgeService不可用")


@dataclass
class MCPToolResult:
    """MCP工具调用结果."""

    success: bool
    data: Any
    error: Optional[str] = None


class PsychologyMCPServer:
    """
    心理学MCP服务器.

    将现有的KnowledgeService包装为标准的MCP工具，
    为Agent提供心理学分析、知识库查询等功能。
    """

    def __init__(self):
        """初始化心理学MCP服务器."""
        self.server_name = "psychology-tools"
        self.version = "1.0.0"

        # 初始化现有服务
        if KNOWLEDGE_SERVICE_AVAILABLE:
            try:
                self.knowledge_service = KnowledgeService()
                print("✅ 心理学MCP服务器已加载KnowledgeService")
            except (ImportError, AttributeError, RuntimeError) as e:
                self.knowledge_service = None
                print(f"⚠️ KnowledgeService初始化失败: {e}")
        else:
            self.knowledge_service = None

    async def emotion_analysis(
        self, text: str, context: Optional[Dict] = None
    ) -> MCPToolResult:
        """
        MCP工具：情绪分析.

        包装KnowledgeService.analyze_user_input方法

        Args:
            text: 用户输入文本
            context: 可选的上下文信息

        Returns:
            MCPToolResult: 情绪分析结果
        """
        try:
            if not self.knowledge_service:
                return MCPToolResult(
                    success=False, data=None, error="KnowledgeService不可用"
                )

            # 从上下文中提取情绪信息
            detected_emotion = context.get("emotion") if context else None

            # 调用现有服务
            knowledge_match = self.knowledge_service.analyze_user_input(
                text, detected_emotion
            )

            if knowledge_match:
                result_data = {
                    "emotion": knowledge_match.framework,
                    "confidence": knowledge_match.confidence,
                    "response_template": knowledge_match.response_template,
                    "follow_up_questions": knowledge_match.follow_up_questions,
                    "techniques": knowledge_match.techniques,
                    "immediate_response": knowledge_match.immediate_response,
                }

                return MCPToolResult(success=True, data=result_data)
            else:
                return MCPToolResult(
                    success=True,
                    data={
                        "emotion": None,
                        "confidence": 0.0,
                        "response_template": "我理解你想要分享的内容。",
                        "follow_up_questions": ["能告诉我更多吗？"],
                        "techniques": [],
                        "immediate_response": "我在这里倾听你。",
                    },
                )

        except (ImportError, AttributeError, RuntimeError) as e:
            return MCPToolResult(
                success=False, data=None, error=f"情绪分析失败: {str(e)}"
            )

    async def psychology_knowledge_search(
        self, emotion: str, keywords: List[str]
    ) -> MCPToolResult:
        """
        MCP工具：心理学知识搜索.

        基于情绪和关键词搜索相关的心理学知识

        Args:
            emotion: 检测到的情绪
            keywords: 关键词列表

        Returns:
            MCPToolResult: 知识搜索结果
        """
        try:
            if not self.knowledge_service:
                return MCPToolResult(
                    success=False, data=None, error="KnowledgeService不可用"
                )

            # 获取框架信息
            framework_info = (
                self.knowledge_service.get_framework_info(emotion) if emotion else None
            )

            # 获取相关技巧
            techniques = self.knowledge_service.suggest_techniques(
                emotion or "通用", emotion or ""
            )

            result_data = {
                "emotion": emotion,
                "frameworks": [emotion] if emotion else [],
                "techniques": techniques,
                "resources": [],
                "framework_info": framework_info,
            }

            return MCPToolResult(success=True, data=result_data)

        except (ImportError, AttributeError, RuntimeError) as e:
            return MCPToolResult(
                success=False, data=None, error=f"知识搜索失败: {str(e)}"
            )

    async def crisis_intervention(self, text: str, level: float) -> MCPToolResult:
        """
        MCP工具：危机干预.

        检测和处理心理危机情况

        Args:
            text: 用户输入文本
            level: 危机等级（0.0-1.0）

        Returns:
            MCPToolResult: 危机干预结果
        """
        try:
            if not self.knowledge_service:
                # 基础危机干预
                if level > 0.8:
                    return MCPToolResult(
                        success=True,
                        data={
                            "action": "immediate_intervention",
                            "hotline": "400-161-9995",
                            "message": "请立即联系专业帮助",
                            "level": "critical",
                        },
                    )
                elif level > 0.5:
                    return MCPToolResult(
                        success=True,
                        data={
                            "action": "monitoring",
                            "resources": ["self_help_guide", "coping_strategies"],
                            "message": "建议寻求专业支持",
                            "level": "moderate",
                        },
                    )
                else:
                    return MCPToolResult(
                        success=True,
                        data={
                            "action": "normal_support",
                            "message": "我在这里支持你",
                            "level": "low",
                        },
                    )

            # 使用KnowledgeService的危机检测
            crisis_response = self.knowledge_service._get_crisis_response()

            return MCPToolResult(
                success=True,
                data={
                    "action": "crisis_intervention",
                    "framework": crisis_response.framework,
                    "response": crisis_response.immediate_response,
                    "questions": crisis_response.follow_up_questions,
                    "techniques": crisis_response.techniques,
                    "confidence": crisis_response.confidence,
                },
            )

        except (ImportError, AttributeError, RuntimeError) as e:
            return MCPToolResult(
                success=False, data=None, error=f"危机干预失败: {str(e)}"
            )

    async def get_safety_guidelines(self) -> MCPToolResult:
        """
        MCP工具：获取安全使用指南.

        Returns:
            MCPToolResult: 安全指南信息
        """
        try:
            if self.knowledge_service:
                guidelines = self.knowledge_service.get_safety_guidelines()
            else:
                # 基础安全指南
                guidelines = {
                    "disclaimer": "本系统仅提供心理健康信息支持，不构成专业医疗建议",
                    "crisis_hotline": "心理危机干预热线：400-161-9995",
                    "refer_to_professional": [
                        "持续的抑郁或焦虑症状",
                        "自伤或自杀想法",
                        "严重的人际关系问题",
                        "创伤后应激反应",
                    ],
                    "boundaries": [
                        "不进行心理诊断",
                        "不提供药物建议",
                        "不处理急性危机情况",
                        "不替代专业治疗",
                    ],
                }

            return MCPToolResult(success=True, data=guidelines)

        except (ImportError, AttributeError, RuntimeError) as e:
            return MCPToolResult(
                success=False, data=None, error=f"获取安全指南失败: {str(e)}"
            )

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        获取可用的MCP工具列表.

        Returns:
            List[Dict]: 工具列表
        """
        return [
            {
                "name": "emotion_analysis",
                "description": "分析用户输入的情绪和心理状态",
                "parameters": {
                    "text": {"type": "string", "description": "用户输入文本"},
                    "context": {"type": "object", "description": "可选的上下文信息"},
                },
            },
            {
                "name": "psychology_knowledge_search",
                "description": "搜索相关的心理学知识和技巧",
                "parameters": {
                    "emotion": {"type": "string", "description": "情绪类型"},
                    "keywords": {"type": "array", "description": "关键词列表"},
                },
            },
            {
                "name": "crisis_intervention",
                "description": "危机检测和干预处理",
                "parameters": {
                    "text": {"type": "string", "description": "用户输入文本"},
                    "level": {"type": "number", "description": "危机等级0.0-1.0"},
                },
            },
            {
                "name": "get_safety_guidelines",
                "description": "获取安全使用指南",
                "parameters": {},
            },
        ]

    async def call_tool(
        self, tool_name: str, parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """
        统一的工具调用接口.

        Args:
            tool_name: 工具名称
            parameters: 工具参数

        Returns:
            MCPToolResult: 工具调用结果
        """
        try:
            if tool_name == "emotion_analysis":
                return await self.emotion_analysis(
                    parameters.get("text", ""), parameters.get("context")
                )
            elif tool_name == "psychology_knowledge_search":
                return await self.psychology_knowledge_search(
                    parameters.get("emotion", ""), parameters.get("keywords", [])
                )
            elif tool_name == "crisis_intervention":
                return await self.crisis_intervention(
                    parameters.get("text", ""), parameters.get("level", 0.0)
                )
            elif tool_name == "get_safety_guidelines":
                return await self.get_safety_guidelines()
            else:
                return MCPToolResult(
                    success=False, data=None, error=f"未知的工具: {tool_name}"
                )

        except (ImportError, AttributeError, RuntimeError) as e:
            return MCPToolResult(
                success=False, data=None, error=f"工具调用失败: {str(e)}"
            )
