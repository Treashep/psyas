# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import current_user, login_user

from psyas.extensions import login_manager
from psyas.public.forms import LoginForm
from psyas.user.forms import RegisterForm
from psyas.user.models import User

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


# ============= 新增 API 路由（供 Vue 前端调用） =============
@blueprint.route("/api/login/", methods=["POST"])
def api_login():
    """新：登录 API（返回 JSON）."""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        return jsonify(
            {
                "status": "success",
                "message": "Logged in successfully",
                "user": {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                },
            }
        )
    else:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Validation failed",
                    "errors": form.errors,
                }
            ),
            400,
        )


@blueprint.route("/api/logout/", methods=["POST"])
@jwt_required()
def api_logout():
    """新：登出 API（返回 JSON）使用JWT认证."""
    # JWT logout通常只需要前端删除token，服务端不需要特别处理
    # 这里可以添加token黑名单功能如果需要的话
    return jsonify({"status": "success", "message": "Logged out successfully"})


@blueprint.route("/api/register/", methods=["POST"])
def api_register():
    """新：注册 API（返回 JSON）."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        return jsonify(
            {"status": "success", "message": "Registered successfully. Please log in."}
        )
    else:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Validation failed",
                    "errors": form.errors,
                }
            ),
            400,
        )


@blueprint.route("/api/user/", methods=["GET"])
@jwt_required()
def api_user_info():
    """新：获取当前用户信息使用JWT认证."""
    # 从JWT获取用户ID
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"status": "error", "message": "用户不存在"}), 401

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    )
