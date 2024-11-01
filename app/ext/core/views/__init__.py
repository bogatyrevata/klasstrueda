from datetime import datetime, timedelta

from flask import Blueprint, abort, g, flash, redirect, render_template, request, url_for
from flask_security import hash_password, current_user
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.exc import OperationalError

from app.ext.core.models import user_datastore
from app.extensions import csrf, db
from config import TZ
from app.ext.core.forms import RegistrationForm

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
        "href": "courses",
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
            "title": "Курсы",
            "href": "courses",
          }, {
            "title": "Базовый ювелирный курс",
            "href": "basic-jewelry",
          }, {
            "title": "Мастер-класс: кольцо всмятку",
            "href": "jewelry-ring",
          }, {
            "title": "Ювелирный марафон: кольца",
            "href": "jewelry-marathon",
          }, {
              "title": "FAQ",
              "href": "faq",
          }, {
            "title": "Записаться",
            "href": "appointment",
          }, {
            "title": "Оплата",
            "href": "payment",
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
    form = RegistrationForm(meta={'csrf':False})
    return render_template("public/index.j2", form=form, hide_header=True, active_item="")


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
    form = RegistrationForm(meta={'csrf': False})
    return render_template("public/contacts.j2", form=form, active_item="contacts")


@core.get("/basic-jewelry")
def basic_jewelry():
    """Базовый ювелирный курс."""
    init_request()
    form = RegistrationForm(request.form, meta={'csrf': False})
    return render_template("public/basic-jewelry.j2", form=form, active_item="basic-jewelry")


@core.get("/appointment")
def appointment():
    """Регистрация на курс."""
    init_request()
    form = RegistrationForm(request.form, meta={'csrf':False})
    return render_template("public/appointment.j2", form=form, active_item="appointment")


@core.get("/jewelry-marathon")
def jewelry_marathon():
    """Регистрация на курс."""
    init_request()
    form = RegistrationForm(request.form, meta={'csrf':False})
    return render_template("public/jewelry-marathon.j2", form=form, active_item="jewelry-marathon")


@core.get("/jewelry-ring")
def jewelry_ring():
    """Регистрация на курс."""
    init_request()
    form = RegistrationForm(request.form, meta={'csrf': False})
    return render_template("public/jewelry-ring.j2", form=form, active_item="jewelry-ring")


@core.route("/form-processing", methods=["GET", "POST"])
def form_proc():
    if current_user.is_authenticated:
        form = RegistrationForm(
            first_name=current_user.first_name,
            email=current_user.email
        )
    else:
        form = RegistrationForm(request.form)

    if form.validate_on_submit():
        first_name = form.first_name.data
        email = form.email.data
        course_title = form.course_title.data
        message = form.message.data

        # Формируем сообщение для отправки уведомления
        send_message = (
            f"Новая заявка на курс:\n"
            f"Имя: {first_name}\n"
            f"Email: {email}\n"
            f"Курс: {course_title}\n"
            f"Сообщение: {message}"
        )

        # Отправляем сообщение в Телеграм
        send_to_telegram(send_message, send_to_admin=True)

        # Отправка сообщения на email
        email_subject = "Новая заявка на курс"
        send_to_email(
            subject=email_subject,
            body=send_message,
            recipients=['bogatyrevata@gmail.com'],
            sender='klasstruedaru@gmail.com',
            reply_to=['klasstruedaru@gmail.com']
        )

        flash("Заявка зарегистрирована, мы с вами свяжемся", "success")
        return redirect(url_for("core.contacts"))

    return render_template("public/contacts.j2", form=form, active_item="form-processing")
