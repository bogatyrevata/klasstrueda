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
    g.breadcrumbs = [{"title": "Личный кабинет"}]
    user_links = [
        {"controller": "user.edit", "title": "Изменить"},
        {"controller": "security.logout", "title": "Выйти"},
    ]
    user_links.extend(
        {"controller": "admin.index", "title": "Админка"} for role in current_user.roles if role.name == "admin"
    )
    return render_template("user/index.j2", user_links=user_links)


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
    return render_template("user/edit_profile.j2", form=edit_profile_form)
