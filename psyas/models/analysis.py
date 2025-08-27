# -*- coding: utf-8 -*-
"""Analysis models (用户分析结果)."""
import datetime as dt

from psyas.database import Column, PkModel, db, reference_col, relationship
from psyas.user.models import User
from psyas.models.conversation import Conversation

class Analysis(PkModel):
    """对用户的基础分析结果"""
    __tablename__ = "user_analysis"

    # 1. 关联用户（每个分析结果属于某个用户）
    user_id=reference_col("users",nullable=False)
    user=relationship(User, backref="analysis")

    # 2. 关联对话（标记该分析基于哪些对话，基础版先关联1条核心对话，后续可扩展为多对多）
    conversation_id=reference_col("conversations",nullable=False)
    conversation=relationship(Conversation, backref="related_analysis")

    # 3. 基础分析内容（简单维度，先跑通流程）
    core_issue=Column(db.String(200), nullable=False)
    emotion=Column(db.String(50), nullable=False)
    simple_conclusion=Column(db.Text, nullable=True)

    # 4. 元数据
    analyzed_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )

    def __repr__(self):
        return f"<UserAnalysis(user={self.user.username}, issue={self.core_issue})>"
