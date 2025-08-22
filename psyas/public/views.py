# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask_login import current_user, login_required, login_user, logout_user

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
    """新：登录 API（返回 JSON）。"""
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
@login_required
def api_logout():
    """新：登出 API（返回 JSON）。"""
    logout_user()
    return jsonify({"status": "success", "message": "Logged out successfully"})


@blueprint.route("/api/register/", methods=["POST"])
def api_register():
    """新：注册 API（返回 JSON）。"""
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
@login_required
def api_user_info():
    """新：获取当前用户信息（示例）。"""
    return jsonify(
        {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }
    )
