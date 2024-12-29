import os
from importlib import import_module

from alembic.migration import MigrationContext
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import login_required, roles_accepted
from sqlalchemy import create_engine

from app.exceptions import ExtNotValidError
from app.ext.core.models import Role, Setting, User, user_datastore
from app.extensions import db
from config import EXT_DIR
from version import __version__
from flask import g


admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("", methods=["GET", "POST"])
@login_required
@roles_accepted("admin")
def index():
    """Главная страница админки."""
    g.is_admin = True  # Добавление флага для админки
    g.breadcrumbs = [{"title": "Админка"}]
    admin_links = [
        {
            "controller": "admin.settings",
            "title": "Настройки",
            "icon": "settings",
        },
        {
            "controller": "admin.users",
            "title": "Пользователи",
            "icon": "users",
        },
        {
            "controller": "admin_courses.index",
            "title": "Курсы",
            "icon": "users",
        },
        {
            "controller": "admin_courses.payments",
            "title": "Оплаты",
            "icon": "users",
        },
    ]

    return render_template("admin/index.j2", admin_links=admin_links)


@admin.route("/settings", methods=["GET", "POST"])
@roles_accepted("admin")
def settings():
    """Настройки сайта и расширений."""
    g.breadcrumbs = [
        {"controller": ".index", "title": "Админка"},
        {"title": "Настройки"},
    ]

    engine = create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"])
    conn = engine.connect()

    context = MigrationContext.configure(conn)
    db_revision = context.get_current_revision()

    settings_db = Setting.query.all()
    if all(s.alias != "app_name" for s in settings_db):
        app_name = Setting(
            alias="app_name",
            title="Название сайта",
            setting=current_app.config.get("APP_NAME"),
        )
        db.session.add(app_name)
        db.session.commit()
    if all(s.alias != "app_description" for s in settings_db):
        app_name = Setting(
            alias="app_description",
            title="Описание сайта",
            setting=current_app.config.get("APP_DESCRIPTION"),
        )
        db.session.add(app_name)
        db.session.commit()

    ext_list = os.listdir(EXT_DIR)
    ext_list_vers = []
    for extension in ext_list:
        if extension.startswith("."):
            continue
        try:
            ext_version = import_module(f"app.ext.{extension}").__version__
        except AttributeError as exc:
            raise ExtNotValidError(f"В расширении {extension} нет информации по версии.") from exc
        ext_list_vers.append({"title": extension, "version": ext_version})

    return render_template(
        "admin/settings.j2",
        settings=settings_db,
        is_admin=True,
        version=__version__,
        db_revision=db_revision,
        extensions=ext_list_vers,
    )


@admin.get("/users")
@roles_accepted("admin")
def users():
    """Показ всех пользователей сайта."""
    g.breadcrumbs = [
        {"controller": ".index", "title": "Админка"},
        {"title": "Пользователи"},
    ]
    user_list_db = User.query.all()
    return render_template("admin/users.j2", users=user_list_db)


@admin.get("/user/<int:user_id>/roles")
@roles_accepted("admin")
def user_roles(user_id):
    """Показ ролей для конкретного пользователя."""
    g.breadcrumbs = [
        {"controller": ".index", "title": "Админка"},
        {"controller": ".users", "title": "Пользователи"},
        {"title": "Редактирование"},
    ]
    user_db = User.query.get_or_404(user_id)
    roles_db = Role.query.all()
    return render_template("admin/roles.j2", user=user_db, roles=roles_db)


@admin.get("/user/<int:user_id>/<int:role_id>/add")
@roles_accepted("admin")
def user_role_add(user_id, role_id):
    """Добавление роли пользователю."""
    user_db = User.query.get_or_404(user_id)
    role_db = Role.query.get_or_404(role_id)
    user_datastore.add_role_to_user(user_db, role_db)
    db.session.commit()
    flash(f"Группа {role_db.name} добавлена для пользователя {user_db.email}", "success")
    return redirect(url_for("admin.user_roles", user_id=user_id))


@admin.get("/user/<int:user_id>/<int:role_id>/delete")
@roles_accepted("admin")
def user_role_delete(user_id, role_id):
    """Удаление роли у пользователя."""
    user_db = User.query.get_or_404(user_id)
    role_db = Role.query.get_or_404(role_id)
    user_datastore.remove_role_from_user(user_db, role_db)
    db.session.commit()
    flash(f"Роль {role_db.name} удалена для {user_db.email}", "warning")
    return redirect(url_for("admin.user_roles", user_id=user_id))
