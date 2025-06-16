from flask import Blueprint, render_template, flash, redirect, url_for
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
    payments_db = Payment.query.filter_by(user_id=current_user.id, status_payment=1).all() #получаем все оплаты пользователя со статусом 1
    return render_template("courses/user/user-courses.j2", payments=payments_db, active_item="user-courses")  # TODO: fix template name


@user_courses.get("/course/<int:course_id>")
def one(course_id):
    payment_db = Payment.query.filter_by(user_id=current_user.id, course_id=course_id).first_or_404()
    return render_template("courses/user/course-one.j2", payment=payment_db, active_item="course-one")


@user_courses.route("/proxy/<video_id>")
def proxy_video(video_id):
    # Перенаправляем на встраиваемый плеер YouTube
    return redirect(f'https://www.youtube.com/embed/{video_id}', code=302)
