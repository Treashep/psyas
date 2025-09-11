# -*- coding: utf-8 -*-
"""聊天助手相关接口路由."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError

from psyas.models.analysis import Analysis
from psyas.services.analysis_service import AnalysisService
from psyas.services.conversation_service import ConversationService
from psyas.user.models import User

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


@chat_bp.route("/send-message", methods=["POST"])
@jwt_required()
def send_message():
    """
    用户发送消息接口（核心）.

    请求体：{ "user_input": "我最近和家里人相处不太好，很烦躁" }
    返回：{ "assistant_response": "能说说最近一次和家里人发生不愉快是因为什么事情吗？", "conversation_id": 123 }
    """
    # 1. 从 JWT 获取用户ID
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"code": 401, "msg": "用户不存在"}), 401

    # 2. 获取请求参数和校验
    data = request.get_json()
    user_input = data.get("user_input")
    if not user_input:
        return jsonify({"code": 400, "msg": "输入内容不能为空"}), 400

    # 3. 调用对话服务，生成回复并存储对话
    try:
        result = ConversationService.create_conversation(current_user_id, user_input)
        return jsonify({"code": 200, "msg": "对话成功", "data": result}), 200
    except SQLAlchemyError as exc:
        return jsonify({"code": 500, "msg": f"数据库操作失败: {str(exc)}"}), 500
    except (ValueError, TypeError) as exc:
        return jsonify({"code": 400, "msg": f"参数错误: {str(exc)}"}), 400


@chat_bp.route("/get-analysis", methods=["GET"])
@jwt_required()
def get_analysis():
    """
    获取用户的分析结果接口.

    返回：{ "analyses": [{"core_issue": "家庭关系困扰", "emotion": "烦躁", ...}] }
    """
    # 1. 从 JWT 获取用户ID
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"code": 401, "msg": "用户不存在"}), 401

    # 2. 查询该用户的所有分析结果（按时间倒序，最新的在前）
    analyses = (
        Analysis.query.filter_by(user_id=current_user_id)
        .order_by(Analysis.analyzed_at.desc())
        .all()
    )
    analyses_list = [
        {
            "analysis_id": analysis.id,
            "core_issue": analysis.core_issue,
            "emotion": analysis.emotion,
            "simple_conclusion": analysis.simple_conclusion,
            "analyzed_at": analysis.analyzed_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for analysis in analyses
    ]
    return jsonify({"code": 200, "msg": "获取分析成功", "data": analyses_list}), 200


@chat_bp.route("/create-analysis", methods=["POST"])
@jwt_required()
def create_analysis():
    """
    触发分析接口（基于某条对话生成分析结果）.

    请求体：{ "conversation_id": 123 }
    返回：{ "analysis": {"core_issue": "家庭关系困扰", ...} }
    """
    # 1. 从 JWT 获取用户ID
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"code": 401, "msg": "用户不存在"}), 401

    data = request.get_json()
    conversation_id = data.get("conversation_id")
    if not conversation_id:
        return jsonify({"code": 400, "msg": "对话 ID不能为空"}), 400

    try:
        analysis = AnalysisService.create_simple_analysis(
            current_user_id, conversation_id
        )
        return (
            jsonify(
                {
                    "code": 200,
                    "msg": "分析成功",
                    "data": {
                        "analysis_id": analysis.id,
                        "core_issue": analysis.core_issue,
                        "emotion": analysis.emotion,
                        "simple_conclusion": analysis.simple_conclusion,
                    },
                }
            ),
            200,
        )
    except SQLAlchemyError as exc:
        return jsonify({"code": 500, "msg": f"数据库操作失败: {str(exc)}"}), 500
    except (ValueError, TypeError) as exc:
        return jsonify({"code": 400, "msg": f"参数错误: {str(exc)}"}), 400
