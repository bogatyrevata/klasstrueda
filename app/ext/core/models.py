from flask_security import SQLAlchemyUserDatastore
from flask_security.models.fsqla_v3 import FsModels, FsRoleMixin, FsUserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models import ModelMixin

FsModels.set_db_info(db)


class Role(db.Model, FsRoleMixin):
    pass


class User(db.Model, FsUserMixin):
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))


class Photo(db.Model, ModelMixin):
    """Модель для хранения изображений сайта."""

    __tablename__ = "photos"
    id: Mapped[int] = mapped_column(init=True, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    alt: Mapped[str] = mapped_column(String(255))


class Setting(db.Model):
    """Настройки сайта."""

    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(init=True, primary_key=True)
    alias = db.Column(db.String(64), unique=True, nullable=False)
    setting = db.Column(db.String(1024))
    title = db.Column(db.String(256))
    description = db.Column(db.String(2048))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
