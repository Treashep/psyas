# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest

# JWT 可选导入
try:
    from flask_jwt_extended import JWTManager

    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    JWTManager = None
bcrypt = Bcrypt()
cors = CORS()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()

# 条件创建JWT管理器
if JWT_AVAILABLE:
    jwt = JWTManager()
else:
    jwt = None
