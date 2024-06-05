from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from app.ext.courses.forms import CategoryForm, CourseForm
from app.ext.courses.models import Category, Course
from app.extensions import db, photos

admin_courses = Blueprint("admin_courses", __name__, template_folder="templates")


@admin_courses.get("")
def index():
    g.breadcrumbs = [
        {"controller": "admin.index", "title": "Админка"},
        {"title": "Курсы"},
    ]
    categories_db = Category.query.all()
    courses_db = Course.query.all()
    return render_template("courses/admin/index.j2", categories=categories_db, courses=courses_db)


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


@admin_courses.route("/edit-category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category_db = Category.query.get_or_404(category_id)
    print(category_db.__dict__)
    if request.method == "GET":
        form = CategoryForm(data=category_db.__dict__)
    else:
        form = CategoryForm()
    print(form.data)

    if form.validate_on_submit():
        category_db.name = form.name.data
        category_db.alias = form.alias.data
        category_db.description = form.description.data
        db.session.commit()
        flash("Категория успешно обновлена!", "success")
        return redirect(url_for(".edit_category", category_id=category_id))

    return render_template("courses/admin/edit-category.j2", form=form, category=category_db, category_id=category_id)


@admin_courses.post("/delete-category/<int:category_id>")
def delete_category(category_id):
    category_db = Category.query.get_or_404(category_id)

    if category_db:
        db.session.delete(category_db)
        db.session.commit()
        flash("Категория успешно удалена!", "success")
    else:
        flash(f"Ошибка при удалении категории!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/add-course/", methods=["GET", "POST"])
def add_course():
    form = CourseForm()
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        course_db = Course(
            category_id=form.data["category_id"],
            name=form.data["name"],
            alias=form.data["alias"],
            description=form.data["description"],
        )
        db.session.add(course_db)
        db.session.commit()
        flash("Курс успешно добавлен!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-course.j2", form=form)
