# -*- coding: utf-8 -*-
"""数据库MCP服务器 - 包装现有的数据库操作为MCP工具."""
from typing import Any, Dict, List, Optional

from sqlalchemy.exc import SQLAlchemyError

# 重用现有模型和数据库
try:
    from psyas.database import db
    from psyas.models.analysis import Analysis
    from psyas.models.conversation import Conversation
    from psyas.user.models import User

    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("警告：数据库模型不可用")

from .psychology_server import MCPToolResult


class DatabaseMCPServer:
    """
    数据库MCP服务器.

    将现有的数据库操作包装为标准的MCP工具，
    为Agent提供数据存储、查询等功能。
    """

    def __init__(self):
        """初始化数据库MCP服务器."""
        self.server_name = "database-tools"
        self.version = "1.0.0"

    async def save_conversation(
        self,
        user_id: int,
        user_input: str,
        assistant_response: str,
        metadata: Optional[Dict] = None,
    ) -> MCPToolResult:
        """
        MCP工具：保存对话记录.

        Args:
            user_id: 用户ID
            user_input: 用户输入
            assistant_response: 助手回复
            metadata: 可选的元数据

        Returns:
            MCPToolResult: 保存结果
        """
        try:
            if not DATABASE_AVAILABLE:
                return MCPToolResult(success=False, data=None, error="数据库不可用")

            conversation = Conversation.create(
                user_id=user_id,
                user_input=user_input.strip(),
                assistant_response=assistant_response,
                is_analyzed=False,
            )

            db.session.add(conversation)
            db.session.commit()

            return MCPToolResult(
                success=True,
                data={
                    "conversation_id": conversation.id,
                    "created_at": conversation.created_at.isoformat(),
                    "user_id": user_id,
                },
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            return MCPToolResult(
                success=False, data=None, error=f"保存对话失败: {str(e)}"
            )

    async def get_user_conversations(
        self, user_id: int, limit: int = 10
    ) -> MCPToolResult:
        """
        MCP工具：获取用户对话历史.

        Args:
            user_id: 用户ID
            limit: 返回数量限制

        Returns:
            MCPToolResult: 对话历史
        """
        try:
            if not DATABASE_AVAILABLE:
                return MCPToolResult(success=False, data=None, error="数据库不可用")

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

            return MCPToolResult(
                success=True,
                data={
                    "conversations": conversation_list,
                    "total": len(conversation_list),
                    "user_id": user_id,
                },
            )

        except SQLAlchemyError as e:
            return MCPToolResult(
                success=False, data=None, error=f"获取对话历史失败: {str(e)}"
            )

    async def save_analysis(
        self, user_id: int, conversation_id: int, analysis_data: Dict
    ) -> MCPToolResult:
        """
        MCP工具：保存分析结果.

        Args:
            user_id: 用户ID
            conversation_id: 对话ID
            analysis_data: 分析数据

        Returns:
            MCPToolResult: 保存结果
        """
        try:
            if not DATABASE_AVAILABLE:
                return MCPToolResult(success=False, data=None, error="数据库不可用")

            analysis = Analysis.create(
                user_id=user_id,
                conversation_id=conversation_id,
                core_issue=analysis_data.get("core_issue", "未知"),
                emotion=analysis_data.get("emotion", "中性"),
                simple_conclusion=analysis_data.get("conclusion", ""),
            )

            db.session.add(analysis)
            db.session.commit()

            return MCPToolResult(
                success=True,
                data={
                    "analysis_id": analysis.id,
                    "analyzed_at": analysis.analyzed_at.isoformat(),
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                },
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            return MCPToolResult(
                success=False, data=None, error=f"保存分析失败: {str(e)}"
            )

    async def get_user_info(self, user_id: int) -> MCPToolResult:
        """
        MCP工具：获取用户信息.

        Args:
            user_id: 用户ID

        Returns:
            MCPToolResult: 用户信息
        """
        try:
            if not DATABASE_AVAILABLE:
                return MCPToolResult(success=False, data=None, error="数据库不可用")

            user = User.query.get(user_id)
            if not user:
                return MCPToolResult(success=False, data=None, error="用户不存在")

            return MCPToolResult(
                success=True,
                data={
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": (
                        user.created_at.isoformat()
                        if hasattr(user, "created_at")
                        else None
                    ),
                    "active": getattr(user, "active", True),
                },
            )

        except SQLAlchemyError as e:
            return MCPToolResult(
                success=False, data=None, error=f"获取用户信息失败: {str(e)}"
            )

    async def query_user_data(
        self, user_id: int, query_type: str, params: Optional[Dict] = None
    ) -> MCPToolResult:
        """
        MCP工具：通用用户数据查询.

        Args:
            user_id: 用户ID
            query_type: 查询类型 (conversations, analyses, profile)
            params: 查询参数

        Returns:
            MCPToolResult: 查询结果
        """
        try:
            if not DATABASE_AVAILABLE:
                return MCPToolResult(success=False, data=None, error="数据库不可用")

            params = params or {}

            if query_type == "conversations":
                return await self.get_user_conversations(
                    user_id, params.get("limit", 10)
                )
            elif query_type == "profile":
                return await self.get_user_info(user_id)
            elif query_type == "analyses":
                # 获取用户的分析历史
                analyses = (
                    Analysis.query.filter_by(user_id=user_id)
                    .order_by(Analysis.analyzed_at.desc())
                    .limit(params.get("limit", 10))
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

                return MCPToolResult(
                    success=True,
                    data={
                        "analyses": analysis_list,
                        "total": len(analysis_list),
                        "user_id": user_id,
                    },
                )
            else:
                return MCPToolResult(
                    success=False, data=None, error=f"未支持的查询类型: {query_type}"
                )

        except SQLAlchemyError as e:
            return MCPToolResult(
                success=False, data=None, error=f"查询用户数据失败: {str(e)}"
            )

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        获取可用的MCP工具列表.

        Returns:
            List[Dict]: 工具列表
        """
        return [
            {
                "name": "save_conversation",
                "description": "保存用户对话记录",
                "parameters": {
                    "user_id": {"type": "integer", "description": "用户ID"},
                    "user_input": {"type": "string", "description": "用户输入"},
                    "assistant_response": {"type": "string", "description": "助手回复"},
                    "metadata": {"type": "object", "description": "可选的元数据"},
                },
            },
            {
                "name": "get_user_conversations",
                "description": "获取用户对话历史",
                "parameters": {
                    "user_id": {"type": "integer", "description": "用户ID"},
                    "limit": {"type": "integer", "description": "返回数量限制"},
                },
            },
            {
                "name": "save_analysis",
                "description": "保存分析结果",
                "parameters": {
                    "user_id": {"type": "integer", "description": "用户ID"},
                    "conversation_id": {"type": "integer", "description": "对话ID"},
                    "analysis_data": {"type": "object", "description": "分析数据"},
                },
            },
            {
                "name": "get_user_info",
                "description": "获取用户信息",
                "parameters": {"user_id": {"type": "integer", "description": "用户ID"}},
            },
            {
                "name": "query_user_data",
                "description": "通用用户数据查询",
                "parameters": {
                    "user_id": {"type": "integer", "description": "用户ID"},
                    "query_type": {"type": "string", "description": "查询类型"},
                    "params": {"type": "object", "description": "查询参数"},
                },
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
            if tool_name == "save_conversation":
                return await self.save_conversation(
                    parameters.get("user_id"),
                    parameters.get("user_input", ""),
                    parameters.get("assistant_response", ""),
                    parameters.get("metadata"),
                )
            elif tool_name == "get_user_conversations":
                return await self.get_user_conversations(
                    parameters.get("user_id"), parameters.get("limit", 10)
                )
            elif tool_name == "save_analysis":
                return await self.save_analysis(
                    parameters.get("user_id"),
                    parameters.get("conversation_id"),
                    parameters.get("analysis_data", {}),
                )
            elif tool_name == "get_user_info":
                return await self.get_user_info(parameters.get("user_id"))
            elif tool_name == "query_user_data":
                return await self.query_user_data(
                    parameters.get("user_id"),
                    parameters.get("query_type", ""),
                    parameters.get("params"),
                )
            else:
                return MCPToolResult(
                    success=False, data=None, error=f"未知的工具: {tool_name}"
                )

        except (SQLAlchemyError, ImportError, AttributeError) as e:
            return MCPToolResult(
                success=False, data=None, error=f"工具调用失败: {str(e)}"
            )
