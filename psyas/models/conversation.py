# -*- coding: utf-8 -*-
"""Conversation models (用户与助手的对话记录)."""
import datetime as dt
from psyas.database import Column, PkModel, db, relationship, reference_col

class Conversation(PkModel):
    """用户与助手的单轮对话记录"""
    __tablename__ = "conversations"
    # 1. 关联用户（关键：每一条对话都属于某个用户）
    user_id=reference_col("users",nullable=False)
    user=relationship("User", backref="conversations")

    # 2. 对话内容（基础版只存核心文本）
    user_input=Column(db.Text, nullable=False)
    assistant_response=Column(db.Text, nullable=False)

    # 3. 基础元数据
    created_at=Column(db.DateTime,nullable=False,default=lambda: dt.datetime.now(dt.timezone.utc))
    is_analyzed=Column(db.Boolean,default=False)

    def __repr__(self):
        return f"<Conversation(user={self.user.username},time={self.created_at})>"