from datetime import datetime, timedelta

from flask import Blueprint, abort, g, render_template
from flask_security import hash_password
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.exc import OperationalError

from app.ext.core.models import user_datastore
from app.extensions import csrf, db
from config import TZ


core = Blueprint("core", __name__, template_folder="templates")


def init_request():
    # try:
    #     db.create_all()
    #     user_datastore.find_or_create_role(
    #         name="admin",
    #         permissions={"admin-read", "admin-write", "user-read", "user-write"},
    #     )
    #     user_datastore.find_or_create_role(name="user", permissions={"user-read", "user-write"})
    #     if not user_datastore.find_user(email="admin@z-gu.ru"):
    #         user_datastore.create_user(
    #             username="admin",
    #             email="admin@z-gu.ru",
    #             password=hash_password("1234567"),
    #             roles=["admin"],
    #         )
    #     if not user_datastore.find_user(email="user@z-gu.ru"):
    #         user_datastore.create_user(
    #             username="user",
    #             email="user@z-gu.ru",
    #             password=hash_password("1234567"),
    #             roles=["user"],
    #         )
    # except OperationalError as msg:
    #     abort(500, msg)
    pass


@core.before_app_request
def before_app_request():
    g.current_year = datetime.now(tz=TZ).year
    g.menu = [
      {
        "title": "Home",
        "href": ""
      }, {
        "title": "About",
        "href": "about"
      }, {
        "title": "Courses",
        "href": "courses"
      }, {
        "title": "Pages",
        "href": "#",
        "submenu": [
          {
            "title": "Features",
            "href": "feature"
          }, {
            "title": "Appointment",
            "href": "appointment"
          }, {
            "title": "Our Team",
            "href": "team"
          }, {
            "title": "Testimonial",
            "href": "testimonial"
          }, {
            "title": "404 Page",
            "href": "404"
          }, {
            "title": "Страница курса",
            "href": "course-page"
          }, {
            "title": "Оплата",
            "href": "payment"
          }
        ]
      }, {
        "title": "Contact",
        "href": "contacts"
      }
    ]
    g.contacts = {
      "phone": "+012 345 6789",
      "address": "123 Street, New York, USA",
      "email": "info@example.com"
    }
    g.social_links = [{
      "title": "facebook-f",
      "href": "https://www.facebook.com/klasstrueda"
    }, {
      "title": "youtube",
      "href": "https://www.youtube.com/channel/UCXIbv2Y_Qvy3sxvluUDA6XQ"
    },{
      "title": "vk",
      "href": "https://vk.com/true_da"
    }, {
      "title": "instagram",
      "href": "https://www.instagram.com/klasstrueda/"
    }]


@core.get("")
def index():
    """Главная страница."""
    return render_template("public/index.j2")


@core.get("/<string:page_name>")
def page(page_name):
    """Для других статических страниц."""
    try:
        return render_template(f"public/{page_name}.j2")
    except TemplateNotFound:
        abort(404)
