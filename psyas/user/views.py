# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

from psyas.user.models import User

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@jwt_required()
def members():
    """List members using JWT authentication."""
    # 从JWT获取用户ID并验证用户存在
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        # 这里可以返回错误页面或重定向到登录页
        return "用户不存在", 401

    return render_template("users/members.html")
