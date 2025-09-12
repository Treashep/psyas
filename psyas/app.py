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
    jwt,
    login_manager,
    migrate,
)

# 导入模型类用于shell context
# 新增：导入模型文件，确保Alembic能扫描到
from psyas.models import analysis  # noqa: F401
from psyas.models import conversation  # noqa: F401
from psyas.models import guide_question  # noqa: F401
from psyas.models import (
    Analysis,
    Conversation,
    GuideQuestion,
)


def create_app(config_object="psyas.settings"):
    """创建适用于前后端分离架构的应用工厂函数."""
    # 初始化 Flask 应用，指定静态文件目录
    app = Flask(
        __name__.split(".")[0],
        static_url_path="",
    )
    app.config.from_object(config_object)
    # 设置前端打包目录为 front/dist
    app.static_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "front", "dist")
    )

    # 先注册扩展，保证扩展初始化顺序正确
    register_extensions(app)

    # ---------- 重点：CORS 跨域配置 ----------
    # 开发环境直接放开跨域（方便调试），生产环境再严格限制
    if app.config.get("ENV") == "development":
        # 允许前端 http://localhost:8080 跨域访问所有路径（实际可根据需求缩小范围）
        CORS(
            app,
            origins="http://localhost:8080",  # 明确前端运行地址
            supports_credentials=True,  # 允许携带 cookie
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"],
        )
    # ---------- CORS 配置结束 ----------

    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    register_frontend_routes(app)

    # 注册业务接口蓝图
    from psyas.routes.analysis_routes import analysis_bp
    from psyas.routes.conversation_routes import conversation_bp
    from psyas.routes.test_routes import test_bp

    app.register_blueprint(test_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(conversation_bp)

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
    # 条件初始化JWT
    if jwt is not None:
        jwt.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints (API 蓝图)."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    from psyas.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)
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
        return {
            "db": db,
            "User": user.models.User,
            "Conversation": Conversation,  # 使用包级别导入
            "Analysis": Analysis,  # 使用包级别导入
            "GuideQuestion": GuideQuestion,  # 使用包级别导入
        }

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
    """新增：注册前端页面路由（生产环境）和测试 API."""
    # 设置前端打包目录为 front/dist
    static_dist = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "front", "dist")
    )

    # 测试 API 接口
    @app.route("/api/hello")
    def api_hello():
        return jsonify({"message": "Hello from Flask API!", "status": "success"})

    # 前端页面入口
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def frontend_index(path):
        # 关键：如果是 API 路径，不转发给前端（让后端正常处理）
        if not path.startswith("api/"):
            return send_from_directory(static_dist, "index.html")
        return jsonify({"error": "API 路径错误"}), 404


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
