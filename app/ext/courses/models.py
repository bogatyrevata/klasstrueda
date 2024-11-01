from datetime import datetime

from app.extensions import db
from app.models import ModelMixin


user_payment_table = db.Table(
    "user_payment",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("payment_id", db.Integer, db.ForeignKey("payment.id")),
)


user_homework_table = db.Table(
    "user_homework",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("homework_id", db.Integer, db.ForeignKey("homework.id")),
)


video_category_table = db.Table(
    "video_category",
    db.Model.metadata,
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
    db.Column("video_id", db.Integer, db.ForeignKey("video.id")),
)


video_course_table = db.Table(
    "video_course",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("video_id", db.Integer, db.ForeignKey("video.id")),
)


video_module_table = db.Table(
    "video_module",
    db.Model.metadata,
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
    db.Column("video_id", db.Integer, db.ForeignKey("video.id")),
)


video_lesson_table = db.Table(
    "video_lesson",
    db.Model.metadata,
    db.Column("lesson_id", db.Integer, db.ForeignKey("lesson.id")),
    db.Column("video_id", db.Integer, db.ForeignKey("video.id")),
)


video_feedback_table = db.Table(
    "video_feedback",
    db.Model.metadata,
    db.Column("video_id", db.Integer, db.ForeignKey("video.id")),
    db.Column("feedback_id", db.Integer, db.ForeignKey("feedback.id")),
)


video_homework_table = db.Table(
    "video_homework",
    db.Model.metadata,
    db.Column("video_id", db.Integer, db.ForeignKey("video.id")),
    db.Column("homework_id", db.Integer, db.ForeignKey("homework.id")),
)


photo_category_table = db.Table(
    "photo_category",
    db.Model.metadata,
    db.Column("photo_id", db.Integer, db.ForeignKey("photos.id")),
    db.Column("category_id", db.Integer,db.ForeignKey("category.id")),
)


photo_course_table = db.Table(
    "photo_course",
    db.Model.metadata,
    db.Column("photo_id", db.Integer, db.ForeignKey("photos.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
)


photo_module_table = db.Table(
    "photo_module",
    db.Model.metadata,
    db.Column("photo_id", db.Integer, db.ForeignKey("photos.id")),
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
)


photo_lesson_table = db.Table(
    "photo_lesson",
    db.Model.metadata,
    db.Column("photo_id", db.Integer, db.ForeignKey("photos.id")),
    db.Column("lesson_id", db.Integer, db.ForeignKey("lesson.id")),
)


photo_homework_table = db.Table(
    "photo_homework",
    db.Model.metadata,
    db.Column("photo_id", db.Integer, db.ForeignKey("photos.id")),
    db.Column("homework_id", db.Integer, db.ForeignKey("homework.id")),
)


photo_feedback_table = db.Table(
    "photo_feedback",
    db.Model.metadata,
    db.Column("photo_id", db.Integer, db.ForeignKey("photos.id")),
    db.Column("feedback_id", db.Integer, db.ForeignKey("feedback.id"))
)


homework_module_table = db.Table(
    "homework_module",
    db.Model.metadata,
    db.Column("homework_id", db.Integer, db.ForeignKey("homework.id")),
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
)


course_module_table = db.Table(
    "course_module",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
)


course_payment_table = db.Table(
    "course_payment",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("payment_id", db.Integer, db.ForeignKey("payment.id")),
)


course_promo_table = db.Table(
    "course_promo",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("promo_id", db.Integer, db.ForeignKey("promo.id")),
)

course_studentwork_table = db.Table(
    "course_studentwork",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("studentwork_id", db.Integer, db.ForeignKey("studentwork.id")),
)


course_tariff_table = db.Table(
    "course_tariff",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("tariff_id", db.Integer, db.ForeignKey("tariff.id")),
)


module_artist_table = db.Table(
    "module_artist",
    db.Model.metadata,
    db.Column("module_id", db.Integer, db.ForeignKey("module.id")),
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.id")),
)


artist_category_table = db.Table(
    "artist_category",
    db.Model.metadata,
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
)


artist_course_table = db.Table(
    "artist_course",
    db.Model.metadata,
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
)


tariff_payment_table = db.Table(
    "tariff_payment",
    db.Model.metadata,
    db.Column("tariff_id", db.Integer, db.ForeignKey("tariff.id")),
    db.Column("payment_id", db.Integer, db.ForeignKey("payment.id")),
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

    courses = db.relationship("Course", backref="category", lazy=True)
    photos = db.relationship("Photo", secondary="photo_category", backref=db.backref("category", lazy="dynamic"))



class Course(db.Model, ModelMixin):
    """Модель для хранения курсов."""

    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
    level = db.Column(db.String(255))
    duration = db.Column(db.String(255))
    about = db.Column(db.Text)
    about_photo = db.Column(db.String(255))
    information = db.Column(db.Text)
    features = db.Column(db.Text)
    skills = db.Column(db.Text)
    students_work = db.Column(db.Text)
    promo = db.Column(db.Text)
    registration_form = db.Column(db.String(255))
    registration_photo = db.Column(db.String(255))
    artist = db.Column(db.Text)
    promos = db.relationship("Promo", secondary="course_promo", backref="course")

    artist_photo = db.Column(db.String(255))
    artist_work = db.Column(db.Text)
    price = db.Column(db.Text)
    final_registration_form = db.Column(db.String(255))
    start_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    end_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    modules = db.relationship("Module", secondary="course_module", backref="course")
    student_works = db.relationship("StudentWork", secondary="course_studentwork", backref=db.backref("course", lazy="dynamic"))



class Module(db.Model, ModelMixin):
    """Модель для хранения модулей курсов."""

    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.Text)

    lessons = db.relationship("Lesson", cascade="all, delete-orphan", backref="module") # каскадное удаление
    courses = db.relationship("Course", secondary="course_module", backref="module")
    photos = db.relationship("Photo", secondary="photo_module", backref=db.backref("module", lazy="dynamic"))


class Lesson(db.Model, ModelMixin):
    """Модель для хранения уроков курсов."""

    __tablename__ = "lesson"
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)
    name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    description = db.Column(db.Text)
    file = db.Column(db.String(255))

    photos = db.relationship("Photo", secondary="photo_lesson", backref=db.backref("lesson", lazy="dynamic"))
    videos = db.relationship("Video", secondary="video_lesson", backref=db.backref("lesson", lazy="dynamic"))


class Homework(db.Model, ModelMixin):
    """Модель для хранения домашней работы для курсов."""

    __tablename__ = "homework"
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    file = db.Column(db.String(255))

    photos = db.relationship("Photo", secondary="photo_homework", backref=db.backref("homework", lazy="dynamic"))
    videos = db.relationship("Video", secondary="video_homework", backref=db.backref("homework", lazy="dynamic"))
    homeworks=db.relationship("Homework", secondary="homework_module", backref=db.backref("homework", lazy="dynamic"))


class Feedback(db.Model, ModelMixin):
    """Модель для хранения отзывов пользователей о курсах."""

    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subject = db.Column(db.String(255))
    message = db.Column(db.Text)

    photos = db.relationship("Photo", secondary="photo_feedback", backref=db.backref("feedback", lazy="dynamic"))
    videos = db.relationship("Video", secondary="video_feedback", backref=db.backref("feedback", lazy="dynamic"))



class Artist(db.Model, ModelMixin):
    """Модель для хранения мастеров, ведущих курс."""

    __tablename__ = "artist"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    avatar = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    contacts = db.Column(db.String(255))

    works = db.relationship("ArtistWork", back_populates="artist", lazy="dynamic") #определение отношения один ко многим
    courses = db.relationship("Course", secondary="artist_course",backref=db.backref("artists", lazy="dynamic"))
    modules=db.relationship("Module", secondary="module_artist", backref=db.backref("artists", lazy="dynamic"))
    # users = db.relationship("User", backref="artist") # one-to-many


class Payment(db.Model, ModelMixin):
    """Модель для хранения оплаты."""

    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    tariff_id = db.Column(db.Integer, db.ForeignKey("tariff.id"))
    datetime_create = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
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


class StudentWork(db.Model, ModelMixin):
    """Модель для хранения работ студентов."""

    __tablename__= "studentwork"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    photo = db.Column(db.String(255))

    courses = db.relationship("Course", secondary="course_studentwork", backref="studentworks")


class ArtistWork(db.Model, ModelMixin):
    """Модель для хранения работ мастера."""

    __tablename__= "artistwork"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    photo = db.Column(db.String(255))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)  # Внешний ключ на таблицу Artist

    # Определение отношения
    artist = db.relationship("Artist", back_populates="works")


class Promo(db.Model, ModelMixin):
    """Модель для хранения информации о акциях."""

    __tablename__ = "promo"
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(255))
    title = db.Column(db.String(255))
    description = db.Column(db.String(2048))
    photo = db.Column(db.String(255))
    price = db.Column(db.Numeric(precision=10, scale=2))
    discount = db.Column(db.Integer)
    start_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.UTC))
    end_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.UTC))

    courses = db.relationship("Course", secondary="course_promo", backref="promo")
