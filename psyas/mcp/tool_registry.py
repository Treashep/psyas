# -*- coding: utf-8 -*-
"""MCP工具注册表 - 统一管理所有MCP工具."""
import asyncio
from typing import Any, Dict, List, Optional

from .database_server import DatabaseMCPServer
from .psychology_server import MCPToolResult, PsychologyMCPServer


class MCPToolRegistry:
    """
    MCP工具注册表.

    统一管理和调用所有MCP工具，为Agent提供一致的工具调用接口。
    """

    def __init__(self):
        """初始化MCP工具注册表."""
        # 初始化各个MCP服务器
        self.psychology_server = PsychologyMCPServer()
        self.database_server = DatabaseMCPServer()

        # 工具映射表
        self.tool_servers = {
            # 心理学工具
            "emotion_analysis": self.psychology_server,
            "psychology_knowledge_search": self.psychology_server,
            "crisis_intervention": self.psychology_server,
            "get_safety_guidelines": self.psychology_server,
            # 数据库工具
            "save_conversation": self.database_server,
            "get_user_conversations": self.database_server,
            "save_analysis": self.database_server,
            "get_user_info": self.database_server,
            "query_user_data": self.database_server,
        }

        print("✅ MCP工具注册表已初始化")

    async def call_tool(
        self, tool_name: str, parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """
        调用指定的MCP工具.

        Args:
            tool_name: 工具名称
            parameters: 工具参数

        Returns:
            MCPToolResult: 工具调用结果
        """
        try:
            if tool_name not in self.tool_servers:
                return MCPToolResult(
                    success=False, data=None, error=f"未找到工具: {tool_name}"
                )

            server = self.tool_servers[tool_name]
            result = await server.call_tool(tool_name, parameters)

            return result

        except (ImportError, AttributeError, RuntimeError) as e:
            return MCPToolResult(
                success=False, data=None, error=f"工具调用异常: {str(e)}"
            )

    async def call_multiple_tools(
        self, tool_calls: List[Dict[str, Any]]
    ) -> List[MCPToolResult]:
        """
        并行调用多个MCP工具.

        Args:
            tool_calls: 工具调用列表，每个元素包含tool_name和parameters

        Returns:
            List[MCPToolResult]: 工具调用结果列表
        """
        try:
            # 创建并发任务
            tasks = []
            for tool_call in tool_calls:
                tool_name = tool_call.get("tool_name", "")
                parameters = tool_call.get("parameters", {})
                task = self.call_tool(tool_name, parameters)
                tasks.append(task)

            # 并发执行
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # 处理异常结果
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(
                        MCPToolResult(
                            success=False,
                            data=None,
                            error=f"工具调用异常: {str(result)}",
                        )
                    )
                else:
                    processed_results.append(result)

            return processed_results

        except (ImportError, AttributeError, RuntimeError) as e:
            # 如果整个并发调用失败，返回错误结果
            error_result = MCPToolResult(
                success=False, data=None, error=f"并发工具调用失败: {str(e)}"
            )
            return [error_result] * len(tool_calls)

    def get_available_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        获取所有可用的MCP工具.

        Returns:
            Dict[str, List]: 按服务器分类的工具列表
        """
        return {
            "psychology": self.psychology_server.get_available_tools(),
            "database": self.database_server.get_available_tools(),
        }

    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        获取指定工具的信息.

        Args:
            tool_name: 工具名称

        Returns:
            Optional[Dict]: 工具信息，如果工具不存在则返回None
        """
        all_tools = self.get_available_tools()

        for server_name, tools in all_tools.items():
            for tool in tools:
                if tool["name"] == tool_name:
                    tool_info = tool.copy()
                    tool_info["server"] = server_name
                    return tool_info

        return None

    async def test_all_tools(self) -> Dict[str, MCPToolResult]:
        """
        测试所有MCP工具的可用性.

        Returns:
            Dict[str, MCPToolResult]: 工具测试结果
        """
        test_results = {}

        # 测试心理学工具
        psychology_tests = [
            ("emotion_analysis", {"text": "我很焦虑", "context": {}}),
            ("psychology_knowledge_search", {"emotion": "焦虑", "keywords": ["担心"]}),
            ("crisis_intervention", {"text": "我想死", "level": 0.8}),
            ("get_safety_guidelines", {}),
        ]

        for tool_name, params in psychology_tests:
            try:
                result = await self.call_tool(tool_name, params)
                test_results[tool_name] = result
            except (ImportError, AttributeError, RuntimeError) as e:
                test_results[tool_name] = MCPToolResult(
                    success=False, data=None, error=f"测试失败: {str(e)}"
                )

        # 注意：数据库工具测试需要真实的用户ID，这里不进行实际测试
        # 只检查工具是否可用
        database_tools = [
            "save_conversation",
            "get_user_conversations",
            "save_analysis",
            "get_user_info",
            "query_user_data",
        ]
        for tool_name in database_tools:
            if tool_name in self.tool_servers:
                test_results[tool_name] = MCPToolResult(
                    success=True,
                    data={"status": "available", "note": "需要实际参数进行完整测试"},
                    error=None,
                )
            else:
                test_results[tool_name] = MCPToolResult(
                    success=False, data=None, error="工具不可用"
                )

        return test_results
