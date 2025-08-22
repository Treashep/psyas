# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import os
import sys

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS  # 新增：导入 CORS 处理跨域

from psyas import commands, public, user
from psyas.extensions import (  # 移除了未使用的csrf_protect
    bcrypt,
    cache,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)


def create_app(config_object="psyas.settings"):
    """创建适用于前后端分离架构的应用工厂函数."""
    # 初始化 Flask 应用，指定静态文件目录
    app = Flask(
        __name__.split(".")[0],
        static_url_path="",  # 先设置 URL 前缀，后续再设置目录
    )
    app.config.from_object(config_object)

    # 延迟设置 static_folder（此时 app.root_path 已被 Flask 正确识别）
    app.static_folder = os.path.join(app.root_path, "static", "dist")

    # 验证关键配置是否加载
    if "CORS_ORIGINS" not in app.config:
        raise ValueError(f"配置文件 {config_object} 中未找到 CORS_ORIGINS，请检查 settings.py")

    register_extensions(app)  # 先注册扩展，保持一致性

    # 仅在开发环境启用 CORS
    if app.config["ENV"] == "development":
        CORS(
            app,
            resources={
                r"/api/*": {
                    "origins": app.config["CORS_ORIGINS"],
                    "supports_credentials": True,
                }
            },
        )

    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    register_frontend_routes(app)  # 注册前端路由

    return app

# 以下函数保持不变，无需修改
def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    # csrf_protect.init_app(app)  # 前后端分离场景暂不启用 CSRF
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints (API 蓝图)."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers (返回 JSON 而非 HTML)."""

    def render_error(error):
        error_code = getattr(error, "code", 500)
        return (
            jsonify({"error": True, "message": str(error), "code": error_code}),
            error_code,
        )

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_frontend_routes(app):
    """新增：注册前端页面路由（生产环境）和测试 API."""  # 修复：末尾添加句号
    static_dist = os.path.join(app.root_path, "static", "dist")

    # 测试 API 接口
    @app.route("/api/hello")
    def api_hello():
        return jsonify({"message": "Hello from Flask API!", "status": "success"})

    # 前端页面入口
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def frontend_index(path):
        return send_from_directory(static_dist, "index.html")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
