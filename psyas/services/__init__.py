# -*- coding: utf-8 -*-
"""Services package (业务逻辑服务层)."""

# 导入ConversationService（已升级为Agent架构）
try:
    from .conversation_service import ConversationService
except ImportError:
    ConversationService = None

# 导入其他服务
try:
    from .analysis_service import AnalysisService
except ImportError:
    AnalysisService = None

try:
    from .knowledge_service import KnowledgeService
except ImportError:
    KnowledgeService = None

# 只定义导出列表，避免未使用的导入
__all__ = ["ConversationService", "AnalysisService", "KnowledgeService"]
