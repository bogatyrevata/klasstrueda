from datetime import datetime, timedelta

from flask import Blueprint, abort, g, redirect, render_template, request, url_for
from flask_security import hash_password
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.exc import OperationalError

from app.ext.core.models import user_datastore
from app.extensions import csrf, db
from config import TZ

user_courses = Blueprint("user_courses", __name__, template_folder="templates")

@user_courses.get("")
def index():
    return "USER_COURSES template ..."
