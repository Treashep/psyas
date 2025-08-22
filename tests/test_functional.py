# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for

from psyas.user.models import User

from .factories import UserFactory


class TestLoggingIn:

    def test_can_log_in_returns_200(self, user, testapp):
        # 直接访问登录页，确保表单渲染
        res = testapp.get(url_for('public.login'))
        form = res.forms["loginForm"]  # 与模板表单 name 一致
        form["username"] = user.username
        form["password"] = "myprecious"
        res = form.submit().follow()
        assert res.status_code == 200

    # 其他登录测试用例类似，调整为直接访问登录页


class TestRegistering:
    def test_can_register(self, testapp):  # 移除 user 参数（避免干扰）
        old_count = len(User.query.all())
        # 直接访问注册页
        res = testapp.get(url_for('public.register'))
        form = res.forms["registerForm"]  # 与模板表单 name 一致
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "secret"
        form["confirm"] = "secret"
        res = form.submit().follow()
        assert res.status_code == 200
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, testapp):
        res = testapp.get(url_for('public.register'))
        form = res.forms["registerForm"]
        form["password"] = "secret"
        form["confirm"] = "secrets"
        res = form.submit()
        assert "Passwords must match" in res

    def test_sees_error_message_if_user_already_registered(self, testapp):
        # 用工厂创建用户，避免依赖外部逻辑
        UserFactory(username="existing_user", email="existing@example.com").save()
        res = testapp.get(url_for('public.register'))
        form = res.forms["registerForm"]
        form["username"] = "existing_user"
        form["email"] = "new@example.com"
        form["password"] = "secret"
        form["confirm"] = "secret"
        res = form.submit()
        assert "Username already registered" in res