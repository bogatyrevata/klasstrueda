from datetime import datetime, timedelta

from flask import Blueprint, abort, g, redirect, render_template, request, url_for
from flask_security import hash_password
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.exc import OperationalError

from app.ext.courses.models import Category, Course

courses = Blueprint("course", __name__, template_folder="templates")

@courses.get("")
def index():
    categories_db = Category.query.all()
    courses_db = Course.query.all()
    return render_template("courses/public/index.j2", categories=categories_db, courses=courses_db)

@courses.route("/course/<int:course_id>")
def course_details(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404)  # Если курс не найден, возвращаем ошибку 404
    return render_template("courses/public/course_details.j2", course=course)
