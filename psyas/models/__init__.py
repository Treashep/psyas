# -*- coding: utf-8 -*-
"""Models package."""

# 导入所有模型类，遵循模块初始化与导入规范
try:
    from .analysis import Analysis
except ImportError:
    Analysis = None

try:
    from .conversation import Conversation
except ImportError:
    Conversation = None

try:
    from .guide_question import GuideQuestion
except ImportError:
    GuideQuestion = None

# 只定义导出列表，避免未使用的导入
__all__ = ["Analysis", "Conversation", "GuideQuestion"]
