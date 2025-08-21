# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"

# 关键修改：数据库连接地址（支持MySQL，兼容原有的环境变量方式）
# 1. 优先从环境变量 DATABASE_URL 读取（.env文件中配置）
# 2. 若未配置，默认使用MySQL连接（适配Docker环境）
SQLALCHEMY_DATABASE_URI = env.str(
    "DATABASE_URL",
    default="mysql+pymysql://root:123456@localhost:3306/psychology_agent",
)

SECRET_KEY = env.str("SECRET_KEY")
SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = (
    "flask_caching.backends.SimpleCache"  # Can be "MemcachedCache", "RedisCache", etc.
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
