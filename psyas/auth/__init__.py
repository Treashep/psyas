# -*- coding: utf-8 -*-
"""Authentication utilities.

提供JWT认证相关的装饰器和工具函数。
"""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from psyas.user.models import User


def jwt_required_custom(f):
    """自定义JWT认证装饰器."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({"error": "Invalid token"}), 401
            return f(current_user=current_user, *args, **kwargs)
        except (RuntimeError, AttributeError, ImportError):
            return jsonify({"error": "Token verification failed"}), 401

    return decorated_function
