from datetime import datetime, timedelta

from flask import Blueprint, abort, current_app, flash, g, jsonify, redirect, render_template, request, url_for
from flask_security import hash_password
from requests import get
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
    g.menu = [{
        "title": "Главная",
        "url": "index",
    }, {
        "title": "Сделать прогноз",
        "url": "predictions",
    }, {
        "title": "Контакты",
        "url": "contacts",
    }, {
        "title": "Предложения по улучшению сайта",
        "url": "suggestions_improvement",
    }, {
        "title": "Таблица РПЛ",
        "url": "show_table",
    }]


@core.get("")
def index():
    """Главная страница."""
    menu = [
      {
        "title": "Главная",
        "href": "index"
      }, {
        "title": "Стайлгайд",
        "href": "styleguide"
      }, {
        "title": "Контакты",
        "href": "contacts"
      }
    ]
    contacts = {
      "phone": "+012 345 6789",
      "address": "123 Street, New York, USA"
    }
    links = [{
      "title": "facebook-f",
      "href": "#twitter-ur2l"
    }, {
      "title": "youtube",
      "href": "#twitter-url3"
    },{
      "title": "vk",
      "href": "#twitter-url4"
    }, {
      "title": "instagram",
      "href": "#twitter-url4"
    }]
    return render_template("public/index.j2", menu=menu, contacts=contacts, links=links)

