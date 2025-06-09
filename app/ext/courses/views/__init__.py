import time

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, url_for, jsonify
from flask_security import current_user

from app.extensions import db
from app.ext.courses.models import Category, Course, Tariff, Payment
from app.ext.courses.forms import CourseRegistrationForm, CoursePaymentForm

from app.utils import send_to_telegram, send_to_email

courses = Blueprint("course", __name__, template_folder="templates")

@courses.before_app_request
def before_request():
    g.popular_courses = Course.query.filter(Course.popular == True).all()

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

    # Получаем все курсы из базы данных
    courses = Course.query.all()

    # Генерируем список выбора курсов
    course_choices = [(course.id, course.title) for course in courses]

    # Генерируем список тарифов для всех курсов
    tariffs_by_course = [
        (tariff.id, f"{tariff.title} – {tariff.price}")
        for course in courses for tariff in course.tariffes
    ]

    # Инициализируем обе формы
    registration_form = CourseRegistrationForm()
    payment_form = CoursePaymentForm()

    payment_form.course_title.choices = course_choices  # Устанавливаем варианты выбора курсов
    payment_form.price.choices = tariffs_by_course

    # Заполняем формы данными текущего пользователя, если он авторизован
    if current_user.is_authenticated:
        registration_form.name.data = current_user.first_name
        registration_form.email.data = current_user.email

        payment_form.name.data = current_user.first_name
        payment_form.email.data = current_user.email

    # Обработка данных формы
    if registration_form.validate_on_submit() and registration_form.form_name.data == 'registration':
        # Логика обработки формы регистрации
        if registration_form.hidden_field.data:
            current_app.logger.warning("Honeypot triggered! Possible bot detected.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
            return redirect(url_for("course.course_details", course_id=course_id))

        # Проверка временной метки
        form_time = int(registration_form.form_time.data)  # Получаем значение времени в миллисекундах
        current_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        time_difference = current_time - form_time

        if time_difference < 2000:  # Если разница меньше 2 секунд
            current_app.logger.warning("Форма отправлена слишком быстро! Возможный бот.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "error")
            return redirect(url_for("course.course_details"))

        name = registration_form.name.data
        email = registration_form.email.data
        course_title = course.title  # Получаем название курса из объекта course
        message = registration_form.message.data

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

    elif payment_form.validate_on_submit() and payment_form.form_name.data == 'payment':
        # Логика обработки формы оплаты
        if payment_form.hidden_field.data:
            current_app.logger.warning("Honeypot triggered! Possible bot detected.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
            return redirect(url_for("course.course_details", course_id=course_id))

         # Проверка временной метки
        form_time_str = payment_form.form_time.data  # Получаем значение времени как строку
        if not form_time_str:  # Если поле пустое
            flash("Ошибка при отправке формы. Время отправки формы отсутствует.", "error")
            return redirect(url_for("course.course_details", course_id=course_id))

        form_time = int(form_time_str)  # Преобразуем в целое число
        current_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        time_difference = current_time - form_time

        if time_difference < 2000:  # Если разница меньше 2 секунд
            # Выводим предупреждение
            current_app.logger.warning(f"{current_time}, {form_time}")
            current_app.logger.warning("Форма отправлена слишком быстро! Возможный бот.")
            flash("Ошибка при отправке формы. Попробуйте снова.", "error")
            return redirect(url_for("course.course_details"))

        # Проверка существования выбранного курса и тарифа
        selected_course = Course.query.get(payment_form.course_title.data)
        if not selected_course:
            flash("Выбранный курс не найден. Пожалуйста, выберите корректный курс.", "danger")
            return redirect(url_for("course.course_details"))

        selected_tariff = next(
            (tariff for tariff in selected_course.tariffes if tariff.id == payment_form.price.data),
            None # Если тариф не найден, возвращаем None
        )
        if not selected_tariff:
            flash("Выбранный тариф не относится к выбранному курсу. Пожалуйста, выберите корректный тариф.", "danger")
            return redirect(url_for("course.course_details"))

        # Сохранение заявки на оплату в базу
        if current_user.is_authenticated:
            payment_db = Payment(
                user_id=current_user.id,
                course_id=selected_course.id,
                tariff_id=selected_tariff.id,
                payment_method=payment_form.payment_method.data,
                status_payment=0, # 0 - не оплачено
            )
            db.session.add(payment_db)
            db.session.commit()
        else:
            flash("Для регистрации на курс — зайдите в личный кабинет.", "danger")
            return redirect(url_for("course.course_details"))

        # Формирование сообщения
        send_message = (
            f"Новая заявка на курс:\n"
            f"Имя: {payment_form.name.data}\n"
            f"Email: {payment_form.email.data}\n"
            f"Курс: {selected_course.title}\n"
            f"Тариф: {selected_tariff.title}\n"
            f"Цена: {selected_tariff.price}\n"
            f"Способ оплаты: {payment_form.payment_method.data}"
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
        return redirect(url_for("course.course_details", course_id=course_id))



    return render_template(
        "courses/public/course_details.j2",
        course=course,
        registration_form=registration_form,
        payment_form=payment_form,
        )


@courses.route("/form-payment", methods=["GET", "POST"])
def form_payment():
    # Получаем все курсы и формируем их выбор
    courses = Course.query.all()
    course_choices = [(course.id, course.title) for course in courses]

    # Генерируем список тарифов для всех курсов
    tariffs_by_course = [
        (tariff.id, f"{tariff.title} – {tariff.price}")
        for course in courses for tariff in course.tariffes
    ]

    current_app.logger.debug(tariffs_by_course)

    # Создаём форму
    form = CoursePaymentForm()
    form.course_title.choices = course_choices  # Устанавливаем варианты выбора курсов
    form.price.choices = tariffs_by_course

    if current_user.is_authenticated:
        form.name.data = current_user.first_name
        form.email.data = current_user.email

    if not form.validate_on_submit():
        return render_template("public/payment.j2", form=form, tariffs_by_course=tariffs_by_course)

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

    # Проверка существования выбранного курса и тарифа
    selected_course = Course.query.get(form.course_title.data)
    if not selected_course:
        flash("Выбранный курс не найден. Пожалуйста, выберите корректный курс.", "danger")
        return redirect(url_for("course.form_payment"))

    selected_tariff = next(
        (tariff for tariff in selected_course.tariffes if tariff.id == form.price.data),
        None # Если тариф не найден, возвращаем None
    )
    if not selected_tariff:
        flash("Выбранный тариф не относится к выбранному курсу. Пожалуйста, выберите корректный тариф.", "danger")
        return redirect(url_for("course.form_payment"))

    # Сохранение заявки на оплату в базу
    if current_user.is_authenticated:
        payment_db = Payment(
            user_id=current_user.id,
            course_id=selected_course.id,
            tariff_id=selected_tariff.id,
            payment_method=form.payment_method.data,
            status_payment=0, # 0 - не оплачено
        )
        db.session.add(payment_db)
        db.session.commit()
    else:
        flash("Для регистрации на курс — зайдите в личный кабинет.", "danger")
        return redirect(url_for("course.form_payment"))

    # Формирование сообщения
    send_message = (
        f"Новая заявка на курс:\n"
        f"Имя: {form.name.data}\n"
        f"Email: {form.email.data}\n"
        f"Курс: {selected_course.title}\n"
        f"Тариф: {selected_tariff.title}\n"
        f"Цена: {selected_tariff.price}\n"
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


@courses.route("/get-tariffs/<int:course_id>")
def get_tariffs(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Курс не найден"}), 404  # Ошибка 404

    tariffs = [{"tariff": t.title, "price": t.price, "id": t.id} for t in course.tariffes]

    if not tariffs:
        return jsonify([{"price": "0", "tariff": "Для этого курса пока нет тарифов"}])  # Сообщение, если тарифов нет

    return jsonify(tariffs)
