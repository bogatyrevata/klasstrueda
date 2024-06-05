from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from app.ext.courses.forms import CategoryForm
from app.ext.courses.models import Category
from app.extensions import db, photos

admin_courses = Blueprint("admin_courses", __name__, template_folder="templates")


@admin_courses.get("")
def index():
    g.breadcrumbs = [
        {"controller": "admin.index", "title": "Админка"},
        {"title": "Курсы"},
    ]
    categories_db = Category.query.all()
    return render_template("courses/admin/index.j2", categories=categories_db)


@admin_courses.route("/add-category", methods=["GET", "POST"])
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category_db = Category(
            name=form.data["name"],
            alias=form.data["alias"],
            description=form.data["description"],
        )
        category_db.save()
        flash("Категория успешно добавлена!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-category.j2", form=form)


@admin_courses.route("/edit-category/>", methods=["GET", "POST"])
def edit_category(category_id):
    category_db = Category.query.get_or_404(category_id)
    form = CategoryForm(category_db)

    if form.validate_on_submit():
        form.name = form.name.data
        form.alias = form.alias.data
        form.description = form.description.data
        db.session.commit()
        flash("Категория успешно обновлена!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/edit-category.j2", form=form, category=category_db)


@admin_courses.route("/delete-category/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    category_db = Category.query.get_or_404(category_id)

    if category_db:
        db.session.delete(category_db)
        db.session.commit()
        flash("Категория успешно удалена!", "success")
    else:
        flash(f"Ошибка при удалении категории!", "danger")

    return redirect(url_for(".index"))
