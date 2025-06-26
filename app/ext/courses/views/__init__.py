import time

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, url_for, jsonify
from flask_security import current_user

from app.extensions import db
from app.ext.courses.models import Category, Course, Tariff, Payment
from app.ext.courses.forms import CourseRegistrationForm, CoursePaymentForm

from app.utils import send_to_telegram, send_to_email, send_user_email, send_admin_notification, is_form_too_fast


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
        abort(404)

    courses = Course.query.all()
    course_choices = [(course.id, course.title) for course in courses]
    tariffs_by_course = [
        (tariff.id, f"{tariff.title} – {tariff.price}")
        for course in courses for tariff in course.tariffes
    ]

    registration_form = CourseRegistrationForm()
    payment_form = CoursePaymentForm()
    payment_form.course_title.choices = course_choices
    payment_form.price.choices = tariffs_by_course

    if current_user.is_authenticated:
        registration_form.name.data = current_user.first_name
        registration_form.email.data = current_user.email
        payment_form.name.data = current_user.first_name
        payment_form.email.data = current_user.email

    # Обработка формы "Задать вопрос"
    if registration_form.validate_on_submit() and registration_form.form_name.data == 'registration':
        if registration_form.hidden_field.data or is_form_too_fast(registration_form.form_time.data):
            flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
            return redirect(url_for("course.course_details", course_id=course_id))

        name = registration_form.name.data
        email = registration_form.email.data
        message = registration_form.message.data

        send_admin_notification(name, email, message=message)
        send_user_email(
            subject="Спасибо за ваш вопрос!",
            body=(
                f"Здравствуйте, {name}!\n\n"
                "Спасибо, что написали нам.\n"
                "Мы получили ваш вопрос и свяжемся с вами в ближайшее время.\n\n"
                "С уважением,\nКоманда Klasstrueda"
            ),
            recipient_email=email
        )
        flash("Спасибо за ваш вопрос! Мы свяжемся с вами в ближайшее время. Ответ придёт на указанную вами почту.", "success")
        return redirect(url_for("course.course_details", course_id=course_id))

    # Обработка формы оплаты
    elif payment_form.validate_on_submit() and payment_form.form_name.data == 'payment':
        if payment_form.hidden_field.data or is_form_too_fast(payment_form.form_time.data):
            flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
            return redirect(url_for("course.course_details", course_id=course_id))

        selected_course = Course.query.get(payment_form.course_title.data)
        if not selected_course:
            flash("Выбранный курс не найден.", "danger")
            return redirect(url_for("course.course_details", course_id=course_id))

        selected_tariff = next(
            (tariff for tariff in selected_course.tariffes if tariff.id == payment_form.price.data),
            None
        )
        if not selected_tariff:
            flash("Выбранный тариф не относится к выбранному курсу.", "danger")
            return redirect(url_for("course.course_details", course_id=course_id))

        if not current_user.is_authenticated:
            flash("Для регистрации на курс — зайдите в личный кабинет.", "danger")
            return redirect(url_for("course.course_details", course_id=course_id))

        payment_db = Payment(
            user_id=current_user.id,
            course_id=selected_course.id,
            tariff_id=selected_tariff.id,
            payment_method=payment_form.payment_method.data,
            status_payment=0 if selected_tariff.price > 0 else 1,
        )
        db.session.add(payment_db)
        db.session.commit()

        send_admin_notification(
            name=payment_form.name.data,
            email=payment_form.email.data,
            course_title=selected_course.title,
            tariff_title=selected_tariff.title,
            price=selected_tariff.price,
            method=payment_form.payment_method.data
        )

        # === Бесплатный курс ===
        if selected_tariff.price == 0:
            flash("Бесплатный курс добавлен в ваш личный кабинет. Вы можете начать обучение прямо сейчас!", "success")
            send_user_email(
                subject="Доступ к бесплатному курсу предоставлен",
                body=(
                    f"Здравствуйте, {current_user.first_name}!\n\n"
                    f"Вы зарегистрировались на бесплатный курс \"{selected_course.title}\".\n"
                    "Курс уже добавлен в ваш личный кабинет, и вы можете приступить к обучению прямо сейчас.\n\n"
                    "С уважением,\nКоманда Klasstrueda"
                ),
                recipient_email=payment_form.email.data
            )
            return redirect(url_for("course.course_details", course_id=course_id))

        # === Платный курс ===
        flash("Заявка на курс зарегистрирована. Мы свяжемся с вами по email с подробностями.", "success")
        send_user_email(
            subject="Спасибо за регистрацию на курс!",
            body=(
                f"Здравствуйте, {current_user.first_name}!\n\n"
                f"Вы успешно зарегистрировались на курс \"{selected_course.title}\".\n"
                f"Выбранный тариф: {selected_tariff.title} ({selected_tariff.price})\n"
                f"Способ оплаты: {payment_form.payment_method.data.upper()}\n\n"
                "Мы свяжемся с вами в ближайшее время.\n\n"
                "С уважением,\nКоманда Klasstrueda"
            ),
            recipient_email=payment_form.email.data
        )
        return redirect(url_for("course.course_details", course_id=course_id))

    return render_template(
        "courses/public/course_details.j2",
        course=course,
        registration_form=registration_form,
        payment_form=payment_form,
    )


@courses.route("/payment", methods=["GET", "POST"])
def payment():
    courses = Course.query.all()
    course_choices = [(course.id, course.title) for course in courses]
    tariffs_by_course = [
        (tariff.id, f"{tariff.title} – {tariff.price}")
        for course in courses for tariff in course.tariffes
    ]

    form = CoursePaymentForm()
    form.course_title.choices = course_choices
    form.price.choices = tariffs_by_course

    if current_user.is_authenticated:
        form.name.data = current_user.first_name
        form.email.data = current_user.email

    if not form.validate_on_submit():
        return render_template("courses/public/payment.j2", form=form)

    # Проверки на бота
    if form.hidden_field.data or is_form_too_fast(form.form_time.data):
        flash("Ошибка при отправке формы. Попробуйте снова.", "danger")
        return redirect(url_for("course.payment"))

    # Проверка курса
    selected_course = Course.query.get(form.course_title.data)
    if not selected_course:
        flash("Выбранный курс не найден. Пожалуйста, выберите корректный курс.", "danger")
        return redirect(url_for("course.payment"))

    # Проверка тарифа
    selected_tariff = next(
        (tariff for tariff in selected_course.tariffes if tariff.id == form.price.data),
        None
    )
    if not selected_tariff:
        flash("Выбранный тариф не относится к выбранному курсу.", "danger")
        return redirect(url_for("course.payment"))

    # Проверка авторизации
    if not current_user.is_authenticated:
        flash("Для регистрации на курс — зайдите в личный кабинет.", "danger")
        return redirect(url_for("course.payment"))

    # Сохранение заявки
    payment_db = Payment(
        user_id=current_user.id,
        course_id=selected_course.id,
        tariff_id=selected_tariff.id,
        payment_method=form.payment_method.data,
        status_payment=0 if selected_tariff.price > 0 else 1,
    )
    db.session.add(payment_db)
    db.session.commit()

    # Уведомление администратору
    send_admin_notification(
        name=form.name.data,
        email=form.email.data,
        course_title=selected_course.title,
        tariff_title=selected_tariff.title,
        price=selected_tariff.price,
        method=form.payment_method.data
    )

    # === Бесплатный курс ===
    if selected_tariff.price == 0:
        flash("Бесплатный курс добавлен в ваш личный кабинет. Вы можете начать обучение прямо сейчас!", "success")
        send_user_email(
            subject="Доступ к бесплатному курсу предоставлен",
            body=(
                f"Здравствуйте, {form.name.data}!\n\n"
                f"Вы зарегистрировались на бесплатный курс \"{selected_course.title}\".\n"
                "Курс уже добавлен в ваш личный кабинет, и вы можете приступить к обучению прямо сейчас.\n\n"
                "С уважением,\n"
                "Команда Klasstrueda"
            ),
            recipient_email=form.email.data
        )
        return redirect(url_for("core.thank_you"))

    # === Платный курс ===
    flash("Заявка на курс зарегистрирована. Мы свяжемся с вами по email с подробностями.", "success")
    send_user_email(
        subject="Спасибо за регистрацию на курс!",
        body=(
            f"Здравствуйте, {form.name.data}!\n\n"
            f"Вы успешно зарегистрировались на курс \"{selected_course.title}\".\n"
            f"Выбранный тариф: {selected_tariff.title} ({selected_tariff.price})\n"
            f"Способ оплаты: {form.payment_method.data.upper()}\n\n"
            "Мы свяжемся с вами в ближайшее время.\n\n"
            "С уважением,\n"
            "Команда Klasstrueda"
        ),
        recipient_email=form.email.data
    )

    return redirect(url_for("core.thank_you"))


@courses.route("/get-tariffs/<int:course_id>")
def get_tariffs(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Курс не найден"}), 404  # Ошибка 404

    tariffs = [{"tariff": t.title, "price": round(t.price), "id": t.id} for t in course.tariffes]

    if not tariffs:
        return jsonify([{"price": "0", "tariff": "Для этого курса пока нет тарифов"}])  # Сообщение, если тарифов нет

    return jsonify(tariffs)
