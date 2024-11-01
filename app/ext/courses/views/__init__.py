from datetime import datetime, timedelta

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from flask_security import hash_password
from jinja2.exceptions import TemplateNotFound
from sqlalchemy.exc import OperationalError

from app.ext.courses.models import Category, Course
from app.ext.courses.forms import CourseRegistrationForm

from app.utils import send_to_telegram, send_to_email

courses = Blueprint("course", __name__, template_folder="templates")

@courses.get("")
def index():
    categories_db = Category.query.all()
    courses_db = Course.query.all()
    return render_template("courses/public/index.j2", categories=categories_db, courses=courses_db)

@courses.route("/course/<int:course_id>", methods=["GET", "POST"])
def course_details(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404)  # Если курс не найден, возвращаем ошибку 404

    form = CourseRegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        course_title = course.title  # Получаем название курса из объекта course
        message = form.message.data

        # Формируем сообщение для отправки
        send_message= (
            f"Новая заявка на курс:\n"
            f"Имя: {name}\n"
            f"Email: {email}\n"
            f"Курс: {course_title}\n"
            f"Сообщение: {message}"
        )

        # Отправляем сообщение в Telegram
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
        return redirect(url_for('course.course_details', course_id=course_id))

    return render_template("courses/public/course_details.j2", course=course, form=form)
