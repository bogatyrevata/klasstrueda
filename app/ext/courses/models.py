from flask_security import SQLAlchemyUserDatastore
from flask_security.models.fsqla_v3 import FsModels, FsRoleMixin, FsUserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models import ModelMixin

FsModels.set_db_info(db)


class Category(db.Model, ModelMixin):
    """Модель для хранения категорий курсов."""

    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))

class Video(db.Model, ModelMixin):
    """Модель для хранения видео."""

    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    duration = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Course (db.Model, ModelMixin):
    """Модель для хранения курсов."""

    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    module = db.Column(db.Integer)
    artist = db.Column(db.String(255))
    tarif = db.Column(db.Integer)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'))


class Module (db.Model, ModelMixin):
    """Модель для хранения модулей курсов."""

    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))


class Lesson (db.Model, ModelMixin):
    """Модель для хранения уроков курсов."""

    __tablename__ = "lesson"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

class Homework (db.Model, ModelMixin):
    """Модель для хранения домашней работы для курсов."""

    __tablename__ = "homework"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    file = db.Column(db.String(255))

class Feedback (db.Model, ModelMixin):
    """Модель для хранения отзывов пользователей о курсах."""

    __tablename__ = "homework"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

class Artist (db.Model, ModelMixin):
    """Модель для хранения мастеров, ведущих курс."""

    __tablename__ = "artist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    category = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    social_link = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Payment (db.Model, ModelMixin):
    """Модель для хранения оплаты."""

    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime = db.Column(db.DateTime)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    tarif_id = db.Column(db.Integer, db.ForeignKey('tarif.id'))
    final_price = db.Column(db.Numeric(precision=10, scale=2))
    status_payment = db.Column(db.Integer)
    date_payment = db.Column(db.DateTime)

class Tarif (db.Model, ModelMixin):
    """Модель для хранения тарифов курсов."""

    __tablename__ = "tarif"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    price = db.Column(db.Numeric(precision=10, scale=2))
    discount = db.Column(db.Integer)

