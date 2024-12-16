import time

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, url_for
from flask_security import current_user

from app.extensions import db
from app.ext.courses.models import Category, Course, Tariff, Payment
from app.ext.courses.forms import CourseRegistrationForm, CoursePaymentForm

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
        # Проверка Honeypot поля
        if form.hidden_field.data:
            current_app.logger.warning("Honeypot triggered! Possible bot detected.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
            return redirect(url_for("course.course_details"))

        # Проверка временной метки
        form_time = int(form.form_time.data)  # Получаем значение времени в миллисекундах
        current_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        time_difference = current_time - form_time

        if time_difference < 2000:  # Если разница меньше 2 секунд
            current_app.logger.warning("Форма отправлена слишком быстро! Возможный бот.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "error")
            return redirect(url_for("course.form_payment"))

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
        return redirect(url_for("course.course_details", course_id=course_id))

    return render_template("courses/public/course_details.j2", course=course, form=form)


@courses.route("/form-payment", methods=["GET", "POST"])
def form_payment():
     # Получаем все курсы и формируем их выбор
    courses = Course.query.all()
    course_choices = [(course.id, course.title) for course in courses]

    # Генерируем словарь тарифов для курсов
    # tariffs_by_course = {
    #     course.id: [(tariff.id, f"{tariff.title} – {tariff.price}") for tariff in course.tariffes] # tariffes — не опечатка???
    #     for course in courses
    # }
    tariffs_by_course = []
    for course in courses:
        for tariff in course.tariffes:
            tariffs_by_course.append((tariff.id, f"{tariff.title} – {tariff.price}"))
    current_app.logger.error(tariffs_by_course)

    # Создаём форму
    form = CoursePaymentForm()
    form.course_title.choices = course_choices  # Устанавливаем варианты выбора курсов
    form.price.choices = tariffs_by_course

    if current_user.is_authenticated:
        form.name.data = current_user.first_name
        form.email.data = current_user.email

    if form.validate_on_submit():
        # Проверка Honeypot поля
        if form.hidden_field.data:
            current_app.logger.warning("Honeypot triggered! Possible bot detected.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
            return redirect(url_for("course.form_payment"))

        # Проверка временной метки
        form_time = int(form.form_time.data)  # Получаем значение времени в миллисекундах
        current_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        time_difference = current_time - form_time

        if time_difference < 2000:  # Если разница меньше 2 секунд
            current_app.logger.warning("Форма отправлена слишком быстро! Возможный бот.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "error")
            return redirect(url_for("course.form_payment"))


        # Обработка отправки формы
        selected_course_id = form.course_title.data
        selected_price = form.price.data

        selected_course = Course.query.get_or_404(selected_course_id)
        selected_tariff = None
        if selected_course:
            selected_tariff = next((tariff for tariff in selected_course.tariffes if tariff.id == selected_price), None)

        if current_user.is_authenticated:
            payment_db = Payment(
                user_id=current_user.id,
                course_id=selected_course.id,
                tariff_id=selected_tariff.id,
                status_payment=0
            )
            db.session.add(payment_db)
            db.session.commit()
        else:
            flash("Для регистрации на курс — зайдите в личный кабинет.", "error")

        # Формируем сообщение для отправки
        send_message = (
            f"Новая заявка на курс:\n"
            f"Имя: {form.name.data}\n"
            f"Email: {form.email.data}\n"
            f"Курс: {selected_course.title if selected_course else 'Неизвестный курс'}\n"
            f"Тариф: {selected_tariff.title if selected_tariff else 'Неизвестный тариф'}\n"
            f"Цена: {selected_tariff.price if selected_tariff else 'Не указано'}\n"
            f"Способ оплаты: {form.payment_method.data}"
        )

        # Отправка сообщения (в Telegram и Email)
        send_to_telegram(send_message, send_to_admin=True)
        send_to_email(
            subject="Новая заявка на курс",
            body=send_message,
            recipients=['bogatyrevata@gmail.com'],
            sender='klasstruedaru@gmail.com',
            reply_to=['klasstruedaru@gmail.com']
        )

        flash("Заявка на оплату курса зарегистрирована", "success")
        return redirect(url_for("core.thank_you"))

    return render_template(
        "public/payment.j2",
        form=form,
        tariffs_by_course=tariffs_by_course,
    )
