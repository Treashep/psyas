# -*- coding: utf-8 -*-
"""对话相关的API路由."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from psyas.services.conversation_service import ConversationService
from psyas.user.models import User

# 创建对话蓝图
conversation_bp = Blueprint("conversation", __name__, url_prefix="/api/conversation")

# 初始化对话服务
conversation_service = ConversationService()


@conversation_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    """
    用户对话接口 - 接收用户输入，返回助手回复.

    请求格式:
    {
        "message": "我最近感觉很焦虑"  // 不再需要user_id，从 JWT 获取
    }

    返回格式:
    {
        "code": 200,
        "message": "对话处理成功",
        "data": {
            "conversation_id": 1,
            "assistant_response": "我能感受到你的担心和不安。能告诉我更多关于这个情况的细节吗？",
            "user_input": "我最近感觉很焦虑",
            "created_at": "2025-08-28T16:37:00"
        }
    }
    """
    try:
        # 1. 从 JWT 获取用户ID
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"code": 401, "message": "用户不存在"}), 401

        # 2. 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "message": "请提供JSON数据"}), 400

        # 3. 验证必需字段
        message = data.get("message")
        if not message or not message.strip():
            return jsonify({"code": 400, "message": "消息内容不能为空"}), 400

        # 4. 调用对话服务处理
        result = conversation_service.process_user_input(
            user_id=current_user_id, user_input=message.strip()
        )

        # 4. 返回结果
        if "error" in result:
            return jsonify(result), result.get("code", 500)
        else:
            return jsonify(result), 200

    except (ValueError, TypeError) as exc:
        return jsonify({"code": 400, "message": f"参数格式错误: {str(exc)}"}), 400
    except ImportError as exc:
        return jsonify({"code": 500, "message": f"服务不可用: {str(exc)}"}), 500


@conversation_bp.route("/history", methods=["GET"])
@jwt_required()
def get_conversation_history():
    """
    获取用户对话历史接口.

    URL参数:
    - limit: 返回数量限制 (查询参数，默认10) // 不再需要user_id路径参数

    返回格式:
    {
        "code": 200,
        "message": "获取对话历史成功",
        "data": {
            "conversations": [
                {
                    "id": 1,
                    "user_input": "我最近感觉很焦虑",
                    "assistant_response": "我能感受到你的担心和不安...",
                    "created_at": "2025-08-28T16:37:00",
                    "is_analyzed": true
                }
            ],
            "total": 1
        }
    }
    """
    try:
        # 1. 从 JWT 获取用户ID
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"code": 401, "message": "用户不存在"}), 401

        # 2. 获取查询参数
        limit = request.args.get("limit", default=10, type=int)

        # 3. 验证参数
        if limit <= 0 or limit > 100:
            return jsonify({"code": 400, "message": "limit参数必须在1-100之间"}), 400

        # 4. 调用服务获取对话历史
        result = conversation_service.get_user_conversations(
            user_id=current_user_id, limit=limit
        )

        # 4. 返回结果
        if "error" in result:
            return jsonify(result), result.get("code", 500)
        else:
            return jsonify(result), 200

    except (ValueError, TypeError) as exc:
        return jsonify({"code": 400, "message": f"参数错误: {str(exc)}"}), 400


@conversation_bp.route("/status", methods=["GET"])
def conversation_status():
    """
    对话服务状态检查接口.

    返回格式:
    {
        "code": 200,
        "message": "对话服务运行正常",
        "data": {
            "service": "ConversationService",
            "status": "active",
            "timestamp": "2025-08-28T16:37:00"
        }
    }
    """
    from datetime import datetime

    try:
        return (
            jsonify(
                {
                    "code": 200,
                    "message": "对话服务运行正常",
                    "data": {
                        "service": "ConversationService",
                        "status": "active",
                        "timestamp": datetime.now().isoformat(),
                        "endpoints": [
                            "/api/conversation/chat",
                            "/api/conversation/history",  # 更新路径
                            "/api/conversation/status",
                        ],
                    },
                }
            ),
            200,
        )
    except ImportError as exc:
        return jsonify({"code": 500, "message": f"服务不可用: {str(exc)}"}), 500
