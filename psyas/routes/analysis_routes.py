# -*- coding: utf-8 -*-
"""分析结果相关的API路由."""
from flask import Blueprint, jsonify, request

from psyas.services.analysis_service import AnalysisService

# 创建分析蓝图
analysis_bp = Blueprint("analysis", __name__, url_prefix="/api/analysis")

# 初始化分析服务
analysis_service = AnalysisService()


@analysis_bp.route("/analyze", methods=["POST"])
def analyze_conversation():
    """
    分析对话接口 - 对用户对话进行心理分析.

    请求格式:
    {
        "user_id": 1,
        "conversation_id": 1  // 可选，如果不提供则分析最新未分析的对话
    }

    返回格式:
    {
        "code": 200,
        "message": "分析完成",
        "data": {
            "analysis_id": 1,
            "core_issue": "工作压力",
            "emotion": "焦虑",
            "conclusion": "当前表现出一定程度的焦虑情绪，工作方面的压力需要合理管理和调节，建议继续深入探讨，寻找更好的应对方式。",
            "analyzed_at": "2025-08-28T16:37:00",
            "conversation_id": 1
        }
    }
    """
    try:
        # 1. 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({"code": 400, "message": "请提供JSON数据"}), 400

        # 2. 验证必需字段
        user_id = data.get("user_id")
        conversation_id = data.get("conversation_id")  # 可选

        if not user_id:
            return jsonify({"code": 400, "message": "缺少user_id字段"}), 400

        # 3. 调用分析服务
        result = analysis_service.analyze_user_conversations(
            user_id=int(user_id),
            conversation_id=int(conversation_id) if conversation_id else None,
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


@analysis_bp.route("/results/<int:user_id>", methods=["GET"])
def get_analysis_results(user_id):
    """
    获取用户分析结果列表接口.

    URL参数:
    - user_id: 用户ID (路径参数)
    - limit: 返回数量限制 (查询参数，默认10)

    返回格式:
    {
        "code": 200,
        "message": "获取分析历史成功",
        "data": {
            "analyses": [
                {
                    "id": 1,
                    "core_issue": "工作压力",
                    "emotion": "焦虑",
                    "conclusion": "当前表现出一定程度的焦虑情绪...",
                    "analyzed_at": "2025-08-28T16:37:00",
                    "conversation_id": 1
                }
            ],
            "total": 1
        }
    }
    """
    try:
        # 1. 获取查询参数
        limit = request.args.get("limit", default=10, type=int)

        # 2. 验证参数
        if limit <= 0 or limit > 100:
            return jsonify({"code": 400, "message": "limit参数必须在1-100之间"}), 400

        # 3. 调用服务获取分析历史
        result = analysis_service.get_user_analysis_history(
            user_id=user_id, limit=limit
        )

        # 4. 返回结果
        if "error" in result:
            return jsonify(result), result.get("code", 500)
        else:
            return jsonify(result), 200

    except (ValueError, TypeError) as exc:
        return jsonify({"code": 400, "message": f"参数错误: {str(exc)}"}), 400


@analysis_bp.route("/detail/<int:user_id>/<int:analysis_id>", methods=["GET"])
def get_analysis_detail(user_id, analysis_id):
    """
    获取分析结果详情接口.

    URL参数:
    - user_id: 用户ID (路径参数)
    - analysis_id: 分析结果ID (路径参数)

    返回格式:
    {
        "code": 200,
        "message": "获取分析结果成功",
        "data": {
            "id": 1,
            "core_issue": "工作压力",
            "emotion": "焦虑",
            "conclusion": "当前表现出一定程度的焦虑情绪...",
            "analyzed_at": "2025-08-28T16:37:00",
            "conversation_id": 1,
            "user_input": "我最近工作压力很大",
            "assistant_response": "听起来你承受了很多压力，这确实不容易..."
        }
    }
    """
    try:
        # 1. 调用服务获取分析详情
        result = analysis_service.get_analysis_by_id(
            user_id=user_id, analysis_id=analysis_id
        )

        # 2. 返回结果
        if "error" in result:
            return jsonify(result), result.get("code", 500)
        else:
            return jsonify(result), 200

    except (ValueError, TypeError) as exc:
        return jsonify({"code": 400, "message": f"参数错误: {str(exc)}"}), 400


@analysis_bp.route("/summary/<int:user_id>", methods=["GET"])
def get_analysis_summary(user_id):
    """
    获取用户分析摘要接口 - 统计用户的整体心理状态趋势.

    URL参数:
    - user_id: 用户ID (路径参数)

    返回格式:
    {
        "code": 200,
        "message": "获取分析摘要成功",
        "data": {
            "total_analyses": 5,
            "emotion_distribution": {
                "焦虑": 2,
                "压力": 1,
                "快乐": 1,
                "中性": 1
            },
            "issue_distribution": {
                "工作压力": 2,
                "人际关系": 1,
                "日常分享": 2
            },
            "recent_trend": "焦虑",
            "last_analysis_date": "2025-08-28T16:37:00"
        }
    }
    """
    try:
        # 1. 获取用户所有分析结果进行统计
        result = analysis_service.get_user_analysis_history(user_id=user_id, limit=100)

        if "error" in result:
            return jsonify(result), result.get("code", 500)

        analyses = result["data"]["analyses"]

        if not analyses:
            return (
                jsonify(
                    {
                        "code": 200,
                        "message": "暂无分析数据",
                        "data": {
                            "total_analyses": 0,
                            "emotion_distribution": {},
                            "issue_distribution": {},
                            "recent_trend": None,
                            "last_analysis_date": None,
                        },
                    }
                ),
                200,
            )

        # 2. 统计情绪分布
        emotion_distribution = {}
        issue_distribution = {}

        for analysis in analyses:
            emotion = analysis["emotion"]
            issue = analysis["core_issue"]

            emotion_distribution[emotion] = emotion_distribution.get(emotion, 0) + 1
            issue_distribution[issue] = issue_distribution.get(issue, 0) + 1

        # 3. 计算最近趋势（最近3次分析的主要情绪）
        recent_emotions = [analysis["emotion"] for analysis in analyses[:3]]
        recent_trend = (
            max(set(recent_emotions), key=recent_emotions.count)
            if recent_emotions
            else None
        )

        # 4. 返回摘要结果
        return (
            jsonify(
                {
                    "code": 200,
                    "message": "获取分析摘要成功",
                    "data": {
                        "total_analyses": len(analyses),
                        "emotion_distribution": emotion_distribution,
                        "issue_distribution": issue_distribution,
                        "recent_trend": recent_trend,
                        "last_analysis_date": (
                            analyses[0]["analyzed_at"] if analyses else None
                        ),
                    },
                }
            ),
            200,
        )

    except (ValueError, TypeError) as exc:
        return jsonify({"code": 400, "message": f"参数错误: {str(exc)}"}), 400


@analysis_bp.route("/status", methods=["GET"])
def analysis_status():
    """
    分析服务状态检查接口.

    返回格式:
    {
        "code": 200,
        "message": "分析服务运行正常",
        "data": {
            "service": "AnalysisService",
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
                    "message": "分析服务运行正常",
                    "data": {
                        "service": "AnalysisService",
                        "status": "active",
                        "timestamp": datetime.now().isoformat(),
                        "endpoints": [
                            "/api/analysis/analyze",
                            "/api/analysis/results/<user_id>",
                            "/api/analysis/detail/<user_id>/<analysis_id>",
                            "/api/analysis/summary/<user_id>",
                            "/api/analysis/status",
                        ],
                    },
                }
            ),
            200,
        )
    except ImportError as exc:
        return jsonify({"code": 500, "message": f"服务不可用: {str(exc)}"}), 500
