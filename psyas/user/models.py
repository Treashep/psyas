# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from psyas.database import Column, PkModel, db, reference_col, relationship
from psyas.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Full username."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

    def generate_tokens(self):
        """生成JWT tokens."""
        access_token = create_access_token(
            identity=self.id,
            additional_claims={
                "username": self.username,
                "email": self.email,
                "is_admin": self.is_admin,
            },
        )
        refresh_token = create_refresh_token(identity=self.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600,  # 1小时
        }

    @staticmethod
    def verify_jwt_token(token):
        """验证JWT token并返回用户."""
        try:
            from flask_jwt_extended import decode_token

            decoded = decode_token(token)
            user_id = decoded["sub"]
            return User.query.get(user_id)
        except (ImportError, AttributeError, KeyError, RuntimeError):
            return None
