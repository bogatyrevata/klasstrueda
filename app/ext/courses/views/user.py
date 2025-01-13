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
    payments_db = Payment.query.filter_by(user_id=current_user.id).all() #получаем все оплаты пользователя
    course_db = Course.query.all()
    return render_template("courses/user/user-courses.j2", payments=payments_db, courses=course_db, active_item="user-courses")  # TODO: fix template name


@user_courses.get("/course/<int:course_id>")
def one(course_id):
    # Проверяем, существует ли указанный курс
    course_db = Course.query.get(course_id)
    if not course_db:
        flash("Такого курса не существует.", "danger")
        return redirect(url_for("user_courses.index"))

    # Проверяем, есть ли оплата за курс у текущего пользователя
    payment_exists = Payment.query.filter_by(user_id=current_user.id, course_id=course_id).first()

    if not payment_exists:
        # Если оплаты нет, возвращаем страницу ошибки или редирект
        flash("Вы не оплатили доступ к этому курсу.", "danger")
        return redirect(url_for("user_courses.index"))

    # Если оплата есть, загружаем курс
    course_db = Course.query.get_or_404(course_id)
    return render_template("courses/user/course-one.j2", course=course_db, active_item="course-one")
