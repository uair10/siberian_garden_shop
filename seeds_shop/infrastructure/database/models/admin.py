from flask_login import UserMixin
from sqlalchemy import Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from .base import TimedBaseModel


class AdminUser(UserMixin, TimedBaseModel):
    __tablename__ = "admin_user"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    can_create_admins: Mapped[bool] = mapped_column(server_default="0")
    can_export: Mapped[bool] = mapped_column(server_default="0")
    can_delete = Column(Boolean, server_default="0")
    can_edit = Column(Boolean, server_default="0")
    can_add = Column(Boolean, server_default="0")
    can_view_files = Column(Boolean, server_default="0")

    # TODO: Вынести это из модели
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def set_password(self, password: str):
        self.password = generate_password_hash(password, method="scrypt")  # type: ignore

    def check_password(self, password: str):
        return check_password_hash(self.password, password)
