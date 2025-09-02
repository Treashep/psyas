# -*- coding: utf-8 -*-
"""MCP (Model Context Protocol) 工具包装模块."""

# -*- coding: utf-8 -*-
"""
MCP (Model Context Protocol) 工具包装模块.

将现有的服务包装为MCP工具，为Agent提供统一的工具调用接口。
"""

try:
    from .database_server import DatabaseMCPServer  # noqa: F401
    from .psychology_server import PsychologyMCPServer  # noqa: F401
    from .tool_registry import MCPToolRegistry  # noqa: F401

    __all__ = ["PsychologyMCPServer", "DatabaseMCPServer", "MCPToolRegistry"]

except ImportError as e:
    print(f"警告：MCP模块导入失败: {e}")
    __all__ = []
