# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from datetime import timedelta

from environs import Env

env = Env()
env.read_env()  # 读取 .env 文件中的环境变量


# 1. 环境区分（开发/生产）
ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"  # 开发环境自动开启 DEBUG


# 2. 数据库配置（保持原有逻辑，增强可读性）
SQLALCHEMY_DATABASE_URI = env.str(
    "DATABASE_URL",
    default="mysql+pymysql://root:123456@localhost:3306/psychology_agent",
)
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭不必要的跟踪，提升性能


# 3. 安全配置
SECRET_KEY = env.str(
    "SECRET_KEY", default="dev-secret-key"
)  # 开发环境默认密钥（生产环境必须通过 .env 设置）
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)  # 密码加密强度

# JWT配置
JWT_SECRET_KEY = env.str(
    "JWT_SECRET_KEY", default=SECRET_KEY
)  # 默认为应用密钥，生产环境建议单独设置
JWT_ACCESS_TOKEN_EXPIRES = timedelta(
    hours=env.int("JWT_ACCESS_TOKEN_HOURS", default=1)
)  # 访问令牌过期时间，默认1小时
JWT_REFRESH_TOKEN_EXPIRES = timedelta(
    days=env.int("JWT_REFRESH_TOKEN_DAYS", default=30)
)  # 刷新令牌过期时间，默认30天
JWT_BLACKLIST_ENABLED = env.bool(
    "JWT_BLACKLIST_ENABLED", default=True
)  # 启用令牌黑名单
JWT_BLACKLIST_TOKEN_CHECKS = env.list(
    "JWT_BLACKLIST_TOKEN_CHECKS", default=["access", "refresh"]
)  # 黑名单检查的令牌类型
# 4. 静态文件配置
SEND_FILE_MAX_AGE_DEFAULT = env.int(
    "SEND_FILE_MAX_AGE_DEFAULT", default=300
)  # 静态文件缓存时间（秒）


# 5. 调试工具配置（仅开发环境生效）
DEBUG_TB_ENABLED = DEBUG  # 开发环境开启调试工具栏
DEBUG_TB_INTERCEPT_REDIRECTS = False  # 不拦截重定向


# 6. 缓存配置（可根据环境调整）
CACHE_TYPE = env.str(
    "CACHE_TYPE",
    default="flask_caching.backends.SimpleCache",  # 开发环境用简单缓存
    # 生产环境可改为："RedisCache"（需安装 redis 依赖）
)
CACHE_REDIS_URL = env.str(
    "CACHE_REDIS_URL", default=""
)  # 若用 Redis，通过环境变量配置地址


# 7. 跨域配置（前后端分离新增）
# 开发环境允许的前端域名（默认 Vue 开发服务器）
CORS_ORIGINS = env.list("CORS_ORIGINS", default=["http://localhost:5000"])
# 生产环境可通过 .env 文件设置为自己的前端域名，例如：
# CORS_ORIGINS=["https://your-frontend.com"]
