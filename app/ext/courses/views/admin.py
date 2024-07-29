import werkzeug
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from app.ext.core.models import Photo
from app.ext.courses.forms import CategoryForm, CourseForm, ModuleForm, LessonForm
from app.ext.courses.models import Category, Course, Module, Lesson
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
    modules_db = Module.query.all()
    lessons_db = Lesson.query.all()
    return render_template("courses/admin/index.j2", categories=categories_db, courses=courses_db,
                           modules=modules_db, lessons=lessons_db)


@admin_courses.route("/add-category", methods=["GET", "POST"])
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category_db = Category(
            name=form.data["name"],
            alias=form.data["alias"],
            description=form.data["description"],
        )
        filename=""
        if "photo" in request.files and request.files["photo"]:
            filename = photos.save(request.files["photo"])
            photo_db = Photo(
                filename=filename,
                alt=f'Изображение для {form.data["name"]}',
            )
            category_db.photos.append(photo_db)

        category_db.save()
        flash("Категория успешно добавлена!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-category.j2", form=form)


@admin_courses.route("/edit-category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category_db = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category_db)

    if form.validate_on_submit():
        category_db.name = form.name.data
        category_db.alias = form.alias.data
        category_db.description = form.description.data

        # Обработка загруженных файлов
        if form.photo.data:
            for file in form.photo.data:
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = photos.save(file)
                    new_photo = Photo(
                        filename=filename,
                        alt=f'Изображение для {form.name.data}',
                    )
                    category_db.photos.append(new_photo)

        db.session.commit()
        flash("Категория успешно обновлена!", "success")
        return redirect(url_for(".edit_category", category_id=category_id))

    return render_template("courses/admin/edit-category.j2", form=form, category=category_db, category_id=category_id)


@admin_courses.route("/delete-photo/<int:photo_id>", methods=["POST"])
def delete_photo(photo_id):
    photo_db = Photo.query.get_or_404(photo_id)
    category_id = photo_db.category.id
    # Удаление файла с сервера, если это необходимо
    db.session.delete(photo_db)
    db.session.commit()
    flash("Фотография успешно удалена!", "success")
    return redirect(url_for(".edit_category", category_id=category_id))


@admin_courses.post("/delete-category/<int:category_id>")
def delete_category(category_id):
    category_db = Category.query.get_or_404(category_id)

    if category_db:
        db.session.delete(category_db)
        db.session.commit()
        flash("Категория успешно удалена!", "success")
    else:
        flash("Ошибка при удалении категории!", "danger")

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
            image=form.image["image"],
            level=form.level["level"],
            duration=form.duration["duration"],
            about=form.data["about"],
            about_photo=form.data["about_photo"],
            information=form.data["information"],
            features=form.data["features"],
            skills=form.data["skills"],
            students_work=form.data["students_work"],
            promo=form.data["promo"],
            registration_form=form.data["registration_form"],
            registration_photo=form.data["registration_photo"],
            artist=form.data["artist"],
            artist_photo=form.data["artist_photo"],
            artist_work=form.data["artist_work"],
            price=form.data["price"],
            start_date=form.start_date["start_date"],
            end_date=form.end_date["end_date"],
            final_registration_form=form.data["final_registration_form"],
        )
        course_db.save()
        flash("Курс успешно добавлен!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-course.j2", form=form)


@admin_courses.route("/edit-course/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    course_db = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course_db)  # Передаем объект course_db в форму для предзаполнения полей
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        course_db.category_id = form.category_id.data
        course_db.name = form.name.data
        course_db.alias = form.alias.data
        course_db.description = form.description.data

        # Проверяем наличие и непустоту файла image
        if 'image' in request.files and request.files['image']:
            filename = photos.save(request.files['image'])
            course_db.image = filename

        course_db.level = form.level.data
        course_db.duration = form.duration.data
        course_db.about = form.about.data

        # Проверяем наличие и непустоту файла about_photo
        if 'about_photo' in request.files and request.files['about_photo']:
            filename = photos.save(request.files['about_photo'])
            course_db.about_photo = filename

        course_db.information = form.information.data
        course_db.features = form.features.data
        course_db.skills = form.skills.data

        # Проверяем наличие и непустоту файла students_work
        if 'students_work' in request.files and request.files['students_work']:
            filename = photos.save(request.files['students_work'])
            course_db.students_work = filename

        course_db.promo = form.promo.data
        course_db.registration_form = form.registration_form.data

        # Проверяем наличие и непустоту файла registration_photo
        if 'registration_photo' in request.files and request.files['registration_photo']:
            filename = photos.save(request.files['registration_photo'])
            course_db.registration_photo = filename

        course_db.artist = form.artist.data

        # Проверяем наличие и непустоту файла artist_photo
        if 'artist_photo' in request.files and request.files['artist_photo']:
            filename = photos.save(request.files['artist_photo'])
            course_db.artist_photo = filename

        # Проверяем наличие и непустоту файла artist_work
        if 'artist_work' in request.files and request.files['artist_work']:
            filename = photos.save(request.files['artist_work'])
            course_db.artist_work = filename

        course_db.price = form.price.data
        course_db.final_registration_form = form.final_registration_form.data
        course_db.start_date = form.start_date.data
        course_db.end_date = form.end_date.data
        db.session.commit()
        flash("Курс успешно обновлен!", "success")
        return redirect(url_for(".edit_course", course_id=course_id))

     # Предзаполняем поля формы и фото
    form.image.data = course_db.image
    form.about_photo.data = course_db.about_photo
    form.registration_photo.data = course_db.registration_photo
    form.students_work.data = course_db.students_work
    form.artist_photo.data = course_db.artist_photo
    form.artist_work.data = course_db.artist_work

    image = course_db.image
    about_photo = course_db.about_photo
    registration_photo = course_db.registration_photo
    students_work = course_db.students_work
    artist_photo = course_db.artist_photo
    artist_work = course_db.artist_work
    print(about_photo)
    return render_template("courses/admin/edit-course.j2", form=form, course=course_id,
                           course_id=course_id, image=image, about_photo=about_photo, registration_photo=registration_photo,
                           students_work=students_work, artist_photo=artist_photo, artist_work=artist_work)


@admin_courses.post("/delete-course/<int:course_id>")
def delete_course(course_id):
    course_db = Course.query.get_or_404(course_id)

    if course_db:
        db.session.delete(course_db)
        db.session.commit()
        flash("Курс успешно удален!", "success")
    else:
        flash("Ошибка при удалении курса!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/add-module/", methods=["GET","POST"])
def add_module():
    form = ModuleForm()
    form.course_id.choices = [(course.id, course.name) for course in Course.query.all()]

    if form.validate_on_submit():
        module_db = Module(
            name=form.data["name"],
            alias=form.data["alias"],
            description=form.data["description"]
        )
        module_db.save()
        flash("Модуль успешно добавлен!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-module.j2", form=form)


@admin_courses.route("/edit-module/<int:module_id>", methods=["GET","POST"])
def edit_module(module_id):
    module_db = Module.query.get_or_404(module_id)
    form = ModuleForm(obj=module_db)

    if form.validate_on_submit():
        module_db.name = form.name.data
        module_db.alias = form.alias.data
        module_db.description = form.description.data
        db.session.commit()
        flash("Модуль успешно обновлен!", "success")
        return redirect(url_for(".edit_module", module_id=module_id))

    return render_template("courses/admin/edit-module.j2", form=form, module=module_id, module_id=module_id)


@admin_courses.post("/delete-module/<int:module_id>")
def delete_module(module_id):
    module_db = Module.query.get_or_404(module_id)

    if module_db:
        db.session.delete(module_db)
        db.session.commit()
        flash("Модуль успешно удален!", "success")
    else:
        flash("Ошибка при удалении модуля!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/add-lesson/", methods=["GET","POST"])
def add_lesson():
    form = LessonForm()
    form.module_id.choices = [(module.id, module.name) for module in Module.query.all()]

    if form.validate_on_submit():
        lesson_db = Lesson(
            module_id = form.data["module_id"],
            name=form.data["name"],
            alias=form.data["alias"],
            description=form.data["description"]
        )
        lesson_db.save()
        flash("Урок успешно сохранен!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-lesson.j2", form=form)


@admin_courses.route("/edit-lesson/<int:lesson_id>", methods=["GET","POST"])
def edit_lesson(lesson_id):
    lesson_db = Module.query.get_or_404(lesson_id)
    form = ModuleForm(obj=lesson_db)

    if form.validate_on_submit():
        lesson_db.name = form.name.data
        lesson_db.alias = form.alias.data
        lesson_db.description = form.description.data
        db.session.commit()
        flash("Урок успешно обновлен!", "success")
        return redirect(url_for(".edit_lesson", lesson_id=lesson_id))

    return render_template("courses/admin/edit-lesson.j2", form=form, lesson=lesson_id, lesson_id=lesson_id)


@admin_courses.post("/delete-lesson/<int:lesson_id>")
def delete_lesson(lesson_id):
    lesson_db = Module.query.get_or_404(lesson_id)

    if lesson_db:
        db.session.delete(lesson_db)
        db.session.commit()
        flash("Урок успешно удален!", "success")
    else:
        flash("Ошибка при удалении урока!", "danger")

    return redirect(url_for(".index"))
