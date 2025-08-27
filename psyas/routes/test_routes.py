# -*- coding: utf-8 -*-
"""测试路由相关的单元测试模块."""
from flask import Blueprint, jsonify, request  # 核心工具

test_bp = Blueprint("test", __name__, url_prefix="/test")


# 测试接口 1：基础连接测试
@test_bp.route("/hello", methods=["GET"])
def hello():
    """
    基础连接测试接口.

    用于验证前后端是否能够正常通信
    返回固定的成功响应

    Returns:
        json: 包含状态码、消息和空数据的JSON响应
    """

    return jsonify({"code": 200, "message": "前后端连接成功！", "data": None})


@test_bp.route("/users", methods=["POST"])
def create_user():
    """
    用户数据处理接口.

    接收包含name和age的JSON数据，对age进行加1处理后返回
    若数据格式错误或缺少必要字段，返回相应的错误信息

    Returns:
        json: 包含处理结果的JSON响应
        int: HTTP状态码（200成功，400错误）
    """

    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请传输JSON数据"}), 400
    if "name" not in data or "age" not in data:
        return jsonify({"code": 400, "message": "请缺少name或age"}), 400
    process_age = int(data["age"]) + 1
    return jsonify(
        {
            "code": 200,
            "message": "数据处理成功",
            "data": {"原始数据": data, "age": process_age},
        }
    )


@test_bp.route("/greet", methods=["GET"])
def greet():
    """
    问候语生成接口.

    接收URL参数中的name（默认值为"访客"），生成个性化问候语并返回
    用于测试GET请求参数的接收与处理

    Returns:
        json: 包含问候信息和接收参数的JSON响应
    """

    username = request.args.get("name", default="访客", type=str)
    greeting = f"你好{username}！后端已收到你传递的参数"
    return jsonify(
        {
            "code": 200,
            "message": "参数接收成功",
            "data": {"greeting": greeting, "received_username": username},
        }
    )
