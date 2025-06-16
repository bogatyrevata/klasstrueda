import time
from datetime import datetime, timedelta

from flask import Blueprint, abort, current_app, g, flash, redirect, render_template, request, url_for
from flask_security import hash_password, current_user
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.exc import OperationalError

from app.ext.core.models import user_datastore
from app.extensions import csrf, db
from config import TZ
from app.ext.core.forms import FeedbackForm
from app.ext.courses.models import Course, Artist
from app.ext.courses.forms import CoursePaymentForm

from app.utils import send_to_telegram, send_to_email


core = Blueprint("core", __name__, template_folder="templates")


def init_request():
    """Создание базовых ролей и пользователей."""
    try:
        user_datastore.find_or_create_role(
            name="admin",
            permissions={"admin-read", "admin-write", "user-read", "user-write"},
        )
        user_datastore.find_or_create_role(name="user", permissions={"user-read", "user-write"})
        if not user_datastore.find_user(email="admin@z-gu.ru"):
            user_datastore.create_user(
                username="admin",
                email="admin@z-gu.ru",
                password=hash_password("1234567"),
                roles=["admin"],
            )
        if not user_datastore.find_user(email="user@z-gu.ru"):
            user_datastore.create_user(
                username="user",
                email="user@z-gu.ru",
                password=hash_password("1234567"),
                roles=["user"],
            )
        db.session.commit()
    except OperationalError as msg:
        abort(500, msg)


@core.before_app_request
def before_app_request():
    g.current_year = datetime.now(tz=TZ).year
    g.menu = [
      {
        "title": "Главная",
        "href": "",
      }, {
        "title": "О нас",
        "href": "about",
      }, {
        "title": "Курсы",
        "view_function": "course.index"
      }, {
        "title": "Разделы",
        "href": "#",
        "submenu": [
          {
            "title": "Наша команда",
            "href": "team",
          }, {
            "title": "Преимущества",
            "href": "feature",
          }, {
              "title": "FAQ",
              "href": "faq",
          }, {
            "title": "Оплата",
            "view_function": "course.payment"
          }, {
            "title": "Отзывы",
            "href": "testimonial",
          }, {
              "title": "Юридическая информация",
              "href": "legal-info",
          },{
              "title": "Политика конфиденциальности",
              "href": "privacy",
          },
        ],
      }, {
        "title": "Контакты",
        "href": "contacts",
      }
    ]
    g.contacts = {
      "phone": "+7(911)245-40-00",
      "tel": "+79112454000",
      "address": "Санкт-Петербург, Газовая 10",
      "email": "klasstrueda@gmail.com",
    }
    g.social_links = [{
      "title": "facebook-f",
      "href": "https://www.facebook.com/klasstrueda",
    }, {
      "title": "youtube",
      "href": "https://www.youtube.com/channel/UCXIbv2Y_Qvy3sxvluUDA6XQ",
    },{
      "title": "vk",
      "href": "https://vk.com/true_da",
    }, {
      "title": "instagram",
      "href": "https://www.instagram.com/klasstrueda/",
    }]


@core.get("")
def index():
    """Главная страница."""
    init_request()
    if current_user.is_authenticated:
        form = FeedbackForm(
            first_name=current_user.first_name,
            email=current_user.email,
            meta={"csrf": False})
    else:
        form = FeedbackForm(meta={"csrf": False})
    featured_artists = Artist.query.filter_by(show_on_homepage=True).all()
    featured_courses = Course.query.filter_by(show_on_homepage=True).all()
    return render_template(
        "public/index.j2",
        form=form,
        hide_header=True,
        featured_artists=featured_artists,
        featured_courses=featured_courses,
        active_item="")


@core.get("/<string:page_name>")
def page(page_name):
    """Для других статических страниц."""
    try:
        return render_template(f"public/{page_name}.j2", active_item=page_name)
    except TemplateNotFound:
        abort(404)


@core.get("/contacts")
def contacts():
    """Контакты."""
    init_request()
    if current_user.is_authenticated:
        form = FeedbackForm(
            first_name=current_user.first_name,
            email=current_user.email,
            meta={"csrf": False})
    else:
        form = FeedbackForm(meta={"csrf": False})
    return render_template("public/contacts.j2", form=form, active_item="contacts")


@core.get("/basic-jewelry")
def basic_jewelry():
    """Базовый ювелирный курс."""
    init_request()
    if current_user.is_authenticated:
        form = FeedbackForm(
            first_name=current_user.first_name,
            email=current_user.email,
            meta={"csrf": False})
    else:
        form = FeedbackForm(meta={"csrf": False})
    return render_template("public/basic-jewelry.j2", form=form, active_item="basic-jewelry")


@core.get("/appointment")
def appointment():
    """Регистрация на курс."""
    init_request()
    if current_user.is_authenticated:
        form = FeedbackForm(
            first_name=current_user.first_name,
            email=current_user.email,
            meta={"csrf": False})
    else:
        form = FeedbackForm(meta={"csrf": False})
    return render_template("public/appointment.j2", form=form, active_item="appointment")


@core.get("/jewelry-marathon")
def jewelry_marathon():
    """Регистрация на курс."""
    init_request()
    if current_user.is_authenticated:
        form = FeedbackForm(
            first_name=current_user.first_name,
            email=current_user.email,
            meta={"csrf": False})
    else:
        form = FeedbackForm(meta={"csrf": False})
    return render_template("public/jewelry-marathon.j2", form=form, active_item="jewelry-marathon")


@core.get("/jewelry-ring")
def jewelry_ring():
    """Регистрация на курс."""
    init_request()
    form = FeedbackForm(request.form, meta={"csrf": False})
    return render_template("public/jewelry-ring.j2", form=form, active_item="jewelry-ring")


@core.get("/about")
def about():
    """О нас."""
    init_request()
    featured_artists = Artist.query.filter_by(show_on_homepage=True).all()
    return render_template("public/about.j2", featured_artists=featured_artists, active_item="about")


@core.route("/thank-you")
def thank_you():
    course_id = request.args.get("course_id")  # Извлекаем course_id из query параметров
    course = Course.query.get(course_id) if course_id else None
    return render_template("public/thank_you.j2", course=course)



@core.route("/form-processing", methods=["GET", "POST"])
def form_proc():
    if current_user.is_authenticated:
        form = FeedbackForm(
            first_name=current_user.first_name,
            email=current_user.email
        )
    else:
        form = FeedbackForm(request.form)

    if form.validate_on_submit():
        # Проверка Honeypot поля
        if form.hidden_field.data:
            current_app.logger.warning("Honeypot triggered! Possible bot detected.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
            return redirect(url_for("course.contacts"))

        # Проверка временной метки
        form_time = int(form.form_time.data)  # Получаем значение времени в миллисекундах
        current_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        time_difference = current_time - form_time

        if time_difference < 2000:  # Если разница меньше 2 секунд
            current_app.logger.warning("Форма отправлена слишком быстро! Возможный бот.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "error")
            return redirect(url_for("course.form_payment"))

        first_name = form.first_name.data
        email = form.email.data
        course_title = form.course_title.data
        message = form.message.data

        # Формируем сообщение для отправки уведомления
        send_message = (
            f"Новый вопрос с сайта:\n"
            f"Имя: {first_name}\n"
            f"Email: {email}\n"
            f"Сообщение: {message}"
        )

        # Отправляем сообщение админу в Телеграм
        send_to_telegram(send_message, send_to_admin=True)

         # Отправка уведомления админу по email
        email_subject = "Новый вопрос с сайта"
        send_to_email(
            subject=email_subject,
            body=send_message,
            recipients=['bogatyrevata@gmail.com'],
            sender='klasstruedaru@gmail.com',
            reply_to=['klasstruedaru@gmail.com']
        )

        # Отправка подтверждения пользователю
        user_subject = "Спасибо за ваш вопрос!"
        user_body = (
            f"Здравствуйте, {first_name}!\n\n"
            "Спасибо, что написали нам.\n"
            "Мы получили ваш вопрос и свяжемся с вами в ближайшее время.\n\n"
            "С уважением,\n"
            "Команда Klasstrueda"
        )
        send_to_email(
            subject=user_subject,
            body=user_body,
            recipients=[email],
            sender='klasstruedaru@gmail.com',
            reply_to=['klasstruedaru@gmail.com']
        )

        flash("Спасибо за ваш вопрос! Мы свяжемся с вами в ближайшее время. Ответ придёт на указанную вами почту.", "success")
        return redirect(url_for("core.thank_you"))

    return render_template("public/contacts.j2", form=form, active_item="form-processing")
