from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from app.ext.core.forms import EditProfileForm
from app.ext.core.models import User
from app.extensions import db, photos

user = Blueprint("user", __name__, template_folder="templates")


@user.get("")
@login_required
def index():
    """Главная страница личного кабинета."""
    user_links = [
        {"controller": "user.edit", "title": "Изменить"},
        {"controller": "security.logout", "title": "Выйти"},
    ]
    # user_links.extend(
    #     {"controller": "admin.index", "title": "Админка"} for role in current_user.roles if role.name == "admin"
    # )
    if any(role.name == "admin" for role in current_user.roles):
        user_links.append({"controller": "admin.index", "title": "Админка"})

    return render_template("user/index.j2", user_links=user_links)


@user.context_processor
def inject_user_menu():
    user_menu = [
        {"title": "Профиль", "href": "user.index"},
        {"title": "Курсы", "href": "user_courses.index"},
        {"title": "Баллы", "href": "user.points"},
        {"title": "Рассылка", "href": "user.mailing"},
        {"title": "Отзывы", "href": "user.feedback"},
    ]
    return {"user_menu": user_menu}


@user.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Редактирование данных пользователя."""
    g.breadcrumbs = [{"controller": ".index", "title": "Личный Кабинет"}, {"title": "Изменить"}]
    current_user_db = User.query.get(current_user.id)
    edit_profile_form = EditProfileForm()
    if edit_profile_form.validate_on_submit():
        current_user_db.username = edit_profile_form.username.data
        current_user_db.first_name = edit_profile_form.first_name.data
        current_user_db.last_name = edit_profile_form.last_name.data
        if edit_profile_form.phone.data:
            current_user_db.us_phone_number = edit_profile_form.phone.data

        # Проверяем наличие и непустоту файла userphoto
        if 'userphoto' in request.files and request.files['userphoto']:
            filename = photos.save(request.files['userphoto'])
            current_user_db.userphoto = filename
            db.session.commit()  # Сохраняем изменения в базе данных после сохранения файла

        db.session.commit()  # Сохраняем изменения в базе данных
        flash("Сохранено", "success")
        return redirect(url_for("user.edit"))
    edit_profile_form.userphoto.data = current_user_db.userphoto
    edit_profile_form.username.data = current_user_db.username
    edit_profile_form.first_name.data = current_user_db.first_name
    edit_profile_form.last_name.data = current_user_db.last_name
    edit_profile_form.phone.data = current_user_db.us_phone_number
    userphoto = current_user_db.userphoto
    return render_template("user/edit_profile.j2", form=edit_profile_form, userphoto=userphoto)


@user.get("/points")
def points():
    """Баллы пользователя."""
    return render_template("user/points.j2", active_item="points")


@user.get("/mailing")
def mailing():
    """Подписка пользователя."""
    return render_template("user/mailing.j2", active_item="mailing")


@user.get("/feedback")
def feedback():
    """Обратная связь пользователя."""
    return render_template("user/feedback.j2", active_item="feedback")

