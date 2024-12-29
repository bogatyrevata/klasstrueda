from flask import Blueprint, render_template
from flask_security import current_user

from app.ext.courses.models import Course, Payment
from app.extensions import csrf, db

user_courses = Blueprint("user_courses", __name__, template_folder="templates")


@user_courses.context_processor
def inject_user_menu():
    user_menu = [
        {"title": "Профиль", "href": "user.index"},
        {"title": "Курсы", "href": "user_courses.index"},
        {"title": "Баллы", "href": "user.points"},
        {"title": "Рассылка", "href": "user.mailing"},
        {"title": "Отзывы", "href": "user.feedback"},
    ]
    return {"user_menu": user_menu}


@user_courses.get("")
def index():
    payments_db = Payment.query.filter_by(user_id=current_user.id).all()
    return render_template("courses/user/user-courses.j2", payments=payments_db, active_item="user-courses")  # TODO: fix template name


@user_courses.get("/course/<int:course_id>")
def one(course_id):
    course_db = Course.query.get_or_404(course_id)
    # TODO: есть ли оплата для текущего пользователя
    return f"Курс и его подробности: {course_db.title}"
