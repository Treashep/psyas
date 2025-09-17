# -*- coding: utf-8 -*-
"""认证路由模块.

提供JWT认证相关的API接口。
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from psyas.extensions import db  # noqa: F401
from psyas.user.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """用户注册接口."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    # 验证用户是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({"code": 400, "message": "用户名已存在"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"code": 400, "message": "邮箱已被注册"}), 400
    # 创建新用户
    user = User.create(username=username, password=password, email=email, active=True)
    return jsonify(
        {
            "code": 200,
            "message": "注册成功",
            "data": {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            },
        }
    )


@auth_bp.route("/login", methods=["POST"])
def jwt_login():
    """
    JWT登录接口.

    接收用户名和密码，验证后返回JWT token。
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        tokens = user.generate_tokens()
        return jsonify(
            {
                "code": 200,
                "message": "登录成功",
                "data": {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    **tokens,
                },
            }
        )
    else:
        return jsonify({"code": 401, "message": "用户名或密码错误"}), 401


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    刷新token.

    使用refresh token获取新的access token。
    """
    current_user_id = get_jwt_identity()
    # user = User.query.get(current_user_id)  # 暂时不需要user对象

    new_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_token, "expires_in": 3600})


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    获取当前用户信息.

    基于JWT token获取当前登录用户的详细信息。
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return jsonify(
        {
            "code": 200,
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
            },
        }
    )
