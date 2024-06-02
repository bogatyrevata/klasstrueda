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
