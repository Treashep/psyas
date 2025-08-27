# -*- coding: utf-8 -*-
"""Guide Question models (引导问题模板)."""
from psyas.database import Column, PkModel, db


class GuideQuestion(PkModel):
    """引导问题模板（按场景分类）."""

    __tablename__ = "guide_questions"

    # 1. 问题分类（方便后续按场景匹配，比如“家庭关系”“情绪”“工作压力”）
    scene = Column(db.String(50), nullable=False)

    # 2. 问题模板（基础版用固定文本，后续可加变量替换，比如“你提到{issue}，能说说具体情况吗？”）
    question_text = Column(db.Text, nullable=False)

    # 3. 优先级（可选，基础版可暂不用，后续用于“优先推荐哪个问题”）
    priority = Column(db.Integer, default=1)

    def __repr__(self):
        """返回引导问题对象的字符串表示."""
        return f"<GuideQuestion(scene={self.scene}, question={self.question_text[:20]}...)>"
