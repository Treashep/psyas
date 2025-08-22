# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
)
from flask_login import login_required, login_user, logout_user, current_user

from psyas.extensions import login_manager
from psyas.public.forms import LoginForm
from psyas.user.forms import RegisterForm
from psyas.user.models import User
from psyas.utils import flash_errors

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


# ============= 旧路由（模板渲染，过渡阶段保留） =============
#@blueprint.route("/", methods=["GET", "POST"])
#def home():
 #   """旧：Home page（模板渲染）"""
  #  form = LoginForm(request.form)
  #  current_app.logger.info("Hello from the home page!")

    # 处理登录（旧逻辑）
#    if request.method == "POST":
#        if form.validate_on_submit():
#            login_user(form.user)
#            flash("You are logged in.", "success")
#            redirect_url = request.args.get("next") or url_for("user.members")
#           return redirect(redirect_url)
#        else:

#            flash_errors(form)

#    return render_template("public/home.html", form=form)
#
#
# @blueprint.route("/logout/")
# @login_required
# def logout():
#     """旧：Logout（模板渲染）"""
#     logout_user()
#     flash("You are logged out.", "info")
#     return redirect(url_for("public.home"))

#
# @blueprint.route("/register/", methods=["GET", "POST"])
# def register():
#     """旧：Register new user（模板渲染）"""
#     form = RegisterForm(request.form)
#     if form.validate_on_submit():
#         User.create(
#             username=form.username.data,
#             email=form.email.data,
#             password=form.password.data,
#             active=True,
#         )
#         flash("Thank you for registering. You can now log in.", "success")
#         return redirect(url_for("public.home"))
#     else:
#         flash_errors(form)
#
#     return render_template("public/register.html", form=form)
#
#
# @blueprint.route("/about/")
# def about():
#     """旧：About page（模板渲染）"""
#     form = LoginForm(request.form)
#     return render_template("public/about.html", form=form)


# ============= 新增 API 路由（供 Vue 前端调用） =============
@blueprint.route("/api/login/", methods=["POST"])
def api_login():
    """新：登录 API（返回 JSON）"""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user)
        return jsonify({
            "status": "success",
            "message": "Logged in successfully",
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email
            }
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "errors": form.errors
        }), 400


@blueprint.route("/api/logout/", methods=["POST"])
@login_required
def api_logout():
    """新：登出 API（返回 JSON）"""
    logout_user()
    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    })


@blueprint.route("/api/register/", methods=["POST"])
def api_register():
    """新：注册 API（返回 JSON）"""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        return jsonify({
            "status": "success",
            "message": "Registered successfully. Please log in."
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "errors": form.errors
        }), 400


@blueprint.route("/api/user/", methods=["GET"])
@login_required
def api_user_info():
    """新：获取当前用户信息（示例）"""
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    })