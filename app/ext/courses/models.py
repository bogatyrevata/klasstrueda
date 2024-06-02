from datetime import datetime, UTC

from app.extensions import db
from app.models import ModelMixin


video_category_table = db.Table(
    "video_category",
    db.Model.metadata,
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
    db.Column("video_id", db.Integer, db.ForeignKey("video.id")),
)


class Video(db.Model, ModelMixin):
    """Модель для хранения видео."""

    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    duration_seconds = db.Column(db.Integer)


class Category(db.Model, ModelMixin):
    """Модель для хранения категорий курсов."""

    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))


class Course(db.Model, ModelMixin):
    """Модель для хранения курсов."""

    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))


class Module(db.Model, ModelMixin):
    """Модель для хранения модулей курсов."""

    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))


class Lesson(db.Model, ModelMixin):
    """Модель для хранения уроков курсов."""

    __tablename__ = "lesson"
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(2048))


class Homework(db.Model, ModelMixin):
    """Модель для хранения домашней работы для курсов."""

    __tablename__ = "homework"
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    name = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    file = db.Column(db.String(255))


class Feedback(db.Model, ModelMixin):
    """Модель для хранения отзывов пользователей о курсах."""

    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subject = db.Column(db.String(255))
    message = db.Column(db.Text)


class Artist(db.Model, ModelMixin):
    """Модель для хранения мастеров, ведущих курс."""

    __tablename__ = "artist"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    avatar = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    contacts = db.Column(db.String(255))


class Payment(db.Model, ModelMixin):
    """Модель для хранения оплаты."""

    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"))
    datetime_create = db.Column(db.DateTime, default=datetime.now(tz=UTC))
    datetime_payment = db.Column(db.DateTime)
    final_price = db.Column(db.Numeric(precision=10, scale=2))
    status_payment = db.Column(db.Integer)


class Tariff(db.Model, ModelMixin):
    """Модель для хранения тарифов курсов."""

    __tablename__ = "tariff"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    price = db.Column(db.Numeric(precision=10, scale=2))
    discount = db.Column(db.Integer)
