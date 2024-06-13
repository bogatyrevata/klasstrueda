from datetime import datetime, timedelta

from flask import Blueprint, abort, g, redirect, render_template, request, url_for
from flask_security import hash_password
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.exc import OperationalError

from app.ext.courses.models import Category

courses = Blueprint("course", __name__, template_folder="templates")

@courses.get("")
def index():
    categories_db = Category.query.all()
    return render_template("courses/public/index.j2", categories=categories_db)
