import werkzeug
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from app.ext.core.models import Photo, User
from app.ext.courses.forms import CategoryForm, CourseForm, ModuleForm, PromoForm, LessonForm, StudentWorkForm, ArtistWorkForm, ArtistForm, TariffForm
from app.ext.courses.models import Category, Course, Module, Lesson, StudentWork, Artist, ArtistWork, Tariff, Video, Promo, Payment
from app.extensions import db, photos, csrf, videos, files

from urllib.parse import urlparse, parse_qs

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
    return render_template(
        "courses/admin/index.j2",
        categories=categories_db,
        courses=courses_db,
        modules=modules_db,
        lessons=lessons_db)


@admin_courses.route("/add-category", methods=["GET", "POST"])
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category_db = Category(
            title=form.data["title"],
            alias=form.data["alias"],
            description=form.data["description"],
        )
        filename=""
        # Обработка загруженных файлов
        if "photo" in request.files and request.files["photo"]:
            for file in request.files.getlist("photo"):
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = photos.save(file)
                    new_photo = Photo(
                        filename=filename,
                        alt=f'Изображение для {form.data["title"]}',
                    )
                    category_db.photos.append(new_photo)

        category_db.save()
        flash("Категория успешно добавлена!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-category.j2", form=form)


@admin_courses.route("/edit-category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category_db = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category_db)

    if form.validate_on_submit():
        category_db.title = form.title.data
        category_db.alias = form.alias.data
        category_db.description = form.description.data

        # Обработка загруженных файлов
        if form.photo.data:
            for file in form.photo.data:
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = photos.save(file)
                    new_photo = Photo(
                        filename=filename,
                        alt=f'Изображение для {form.title.data}',
                    )
                    category_db.photos.append(new_photo)

        db.session.commit()
        flash("Категория успешно обновлена!", "success")
        return redirect(url_for(".edit_category", category_id=category_id))

    return render_template(
        "courses/admin/edit-category.j2",
        form=form,
        category=category_db,
        category_id=category_id)



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


@admin_courses.route("/add-course", methods=["GET", "POST"])
def add_course():
    form = CourseForm()
    form.category_id.choices = [(category.id, category.title) for category in Category.query.all()]
    form.modules.choices = [(module.id, module.title) for module in Module.query.all()]

    if form.validate_on_submit():
        file_fields = [
        "preview_photo", "homepage_photo", "about_photo",
        "registration_photo", "artist_photo", "artist_photo_preview"
        ]

        # Проверяем, что все обязательные файлы загружены (кроме artist_photo_preview)
        if any(field not in request.files or not request.files[field].filename for field in file_fields if field != "artist_photo_preview"):
            flash("Все фото для курса обязательны к загрузке, кроме фото работы мастера.", "danger")
            return render_template(
                "courses/admin/add-course.j2",
                form=form,
                courses=Course.query.all(),
        )

        course_db = Course(
            category_id=form.data["category_id"],
            title=form.data["title"],
            alias=form.data["alias"],
            preview_description=form.data["preview_description"],
            show_on_homepage=form.data["show_on_homepage"],
            popular=form.data["popular"],
            level=form.data["level"],
            duration=form.data["duration"],
            about=form.data["about"],
            learning_process_title = form.data["learning_process_title"],
            learning_process_description=form.data["learning_process_description"],
            features_title=form.data["features_title"],
            features_description=form.data["features_description"],
            skills_title=form.data["skills_title"],
            skills_description=form.data["skills_description"],
            registration_form=form.data["registration_form"],
            artist_title=form.data["artist_title"],
            artist_description=form.data["artist_description"],
            price=form.data["price"],
            start_date=form.data["start_date"],
            end_date=form.data["end_date"],
        )

       # Загружаем файлы
        for field in file_fields:
            file = request.files.get(field)
            if file and file.filename:
                try:
                    filename = photos.save(file)
                    setattr(course_db, field, filename)
                except Exception as e:
                    flash(f"Ошибка при сохранении {field}: {e}", "danger")
                    return render_template(
                        "courses/admin/add-course.j2",
                        form=form,
                        courses=Course.query.all(),
                    )

        # добавление модулей
        selected_modules = Module.query.filter(Module.id.in_(form.modules.data)).all()
        course_db.modules.extend(selected_modules)

        course_db.save()
        flash("Курс успешно добавлен!", "success")
        return redirect(url_for(".index"))

    return render_template("courses/admin/add-course.j2", form=form)


@admin_courses.route("/edit-course/<int:course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    course_db = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course_db)  # Передаем объект course_db в форму для предзаполнения полей
    artists = course_db.artists
    form.category_id.choices = [(category.id, category.title) for category in Category.query.all()]
    form.modules.choices = [(module.id, module.title) for module in Module.query.all()]

    # Предзаполняем выбранные модули
    if request.method == "GET":
        form.modules.data = [module.id for module in course_db.modules]


    if form.validate_on_submit():

        course_db.category_id = form.category_id.data
        course_db.title = form.title.data
        course_db.alias = form.alias.data
        course_db.preview_description = form.preview_description.data
        course_db.show_on_homepage = form.show_on_homepage.data
        course_db.popular = form.popular.data
        course_db.level = form.level.data
        course_db.duration = form.duration.data
        course_db.about = form.about.data
        course_db.learning_process_title  = form.learning_process_title.data
        course_db.learning_process_description = form.learning_process_description.data
        course_db.features_title = form.features_title.data
        course_db.features_description = form.features_description.data
        course_db.skills_title = form.skills_title.data
        course_db.skills_description = form.skills_description.data
        course_db.registration_form = form.registration_form.data
        course_db.price = form.price.data
        course_db.start_date = form.start_date.data
        course_db.end_date = form.end_date.data

        file_fields = [
            "preview_photo", "homepage_photo", "about_photo",
            "registration_photo", "artist_photo", "artist_photo_preview"
        ]

        for field in file_fields:
            file = request.files.get(field)
            if file:
                filename = photos.save(file)
                setattr(course_db, field, filename)

        # Обработка загруженных файлов модулей
        course_db.modules = [Module.query.get(module_id) for module_id in form.modules.data]

        db.session.commit()
        flash("Курс успешно обновлен!", "success")
        return redirect(url_for(".edit_course", course_id=course_id))

     # Предзаполняем поля формы и фото
    form.preview_photo.data = course_db.preview_photo
    form.homepage_photo.data = course_db.homepage_photo
    form.about_photo.data = course_db.about_photo
    form.registration_photo.data = course_db.registration_photo
    form.artist_photo.data = course_db.artist_photo
    form.artist_photo_preview.data = course_db.artist_photo_preview

    preview_photo = course_db.preview_photo
    homepage_photo = course_db.homepage_photo
    about_photo = course_db.about_photo
    registration_photo = course_db.registration_photo
    student_works = course_db.student_works
    artist_photo = course_db.artist_photo
    artist_photo_preview = course_db.artist_photo_preview
    return render_template(
        "courses/admin/edit-course.j2",
        form=form,
        course=course_db,
        course_id=course_id,
        preview_photo=preview_photo,
        homepage_photo=homepage_photo,
        about_photo=about_photo,
        registration_photo=registration_photo,
        student_works=student_works,
        artist_photo=artist_photo,
        artist_photo_preview=artist_photo_preview,
        artists=artists)


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


@admin_courses.route("/save-selected-courses", methods=["GET", "POST"])
def save_selected_courses():
    selected_courses = []

    # Получаем список всех курсов из базы данных
    courses = Course.query.all()

    if request.method == "POST":
        # Проходим по всем курсам и собираем выбранные для показа на главной странице
        for course in courses:
            checkbox_name = f"show_on_homepage_{course.id}"
            if checkbox_name in request.form:
                course.show_on_homepage = True
                selected_courses.append(course)
            else:
                course.show_on_homepage = False

        # Сохраняем изменения в базе данных
        db.session.commit()

        flash(f"Выбранные курсы обновлены: {', '.join(course.title for course in selected_courses)}", "success")
        return redirect(url_for('.index'))

    return render_template("courses/admin/save-selected-courses.j2", courses=courses)


@admin_courses.route("/save-selected-popular-courses", methods=["GET", "POST"])
def save_selected_popular_courses():
    # Получаем список всех курсов из базы данных
    courses = Course.query.all()

    if request.method == "POST":
        # Проходим по всем курсам и собираем выбранные как популярные
        for course in courses:
            checkbox_name = f"popular_{course.id}"
            if checkbox_name in request.form:
                course.popular = True
            else:
                course.popular = False

        # Сохраняем изменения в базе данных
        db.session.commit()

        flash("Выбранные популярные курсы обновлены", "success")
        return redirect(url_for('.index'))

    return render_template("courses/admin/save-selected-popular-courses.j2", courses=courses)



@admin_courses.route("/add-module", methods=["GET", "POST"])
def add_module():
    form = ModuleForm()
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]
    form.lessons.choices = [(lesson.id, lesson.title) for lesson in Lesson.query.all()]

    if form.validate_on_submit():
        module_db = Module(
            title=form.data["title"],
            alias=form.data["alias"],
            description=form.data["description"],
        )

        # Обработка загруженных файлов
        if form.photo.data:
            for file in form.photo.data:
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = photos.save(file)
                    new_photo = Photo(
                        filename=filename,
                        alt=f'Изображение для {form.title.data}',
                    )
                    module_db.photos.append(new_photo)
                    db.session.add(new_photo)  # Добавляем фото в сессию для сохранения

        db.session.add(module_db)
        db.session.commit()

        # Обновление связи courses вручную
        selected_courses = [Course.query.get(course_id) for course_id in form.course_id.data]
        for course in selected_courses:
            course.modules.append(module_db)

        # Обновление связи с lessons
        selected_lessons = [Lesson.query.get(lesson_id) for lesson_id in form.lessons.data]
        module_db.lessons = selected_lessons

        db.session.commit()  # Сохраняем изменения в базе данных
        flash("Модуль успешно добавлен!", "success")
        return redirect(url_for(".index"))

    modules_db = Module.query.all()  # Получаем все модули из базы данных

    return render_template(
        "courses/admin/add-module.j2",
        form=form,
        modules=modules_db)


@admin_courses.route("/edit-module/<int:module_id>", methods=["GET","POST"])
def edit_module(module_id):
    module_db = Module.query.get_or_404(module_id)
    form = ModuleForm(obj=module_db)
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]
    form.lessons.choices = [(lesson.id, lesson.title) for lesson in Lesson.query.all()]

    # Предзаполнение выбранных курсов
    form.course_id.data = [course.id for course in module_db.courses]

    # Предзаполнение выбранных уроков
    form.lessons.data = [lesson.id for lesson in module_db.lessons]

    if form.validate_on_submit():
        module_db.title = form.title.data
        module_db.alias = form.alias.data
        module_db.description = form.description.data

        if form.photo.data:
          for file in form.photo.data:
              if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                  filename = photos.save(file)
                  new_photo = Photo(
                      filename=filename,
                      alt=f'Изображение для {form.title.data}',
                  )
                  module_db.photos.append(new_photo)
                  db.session.add(new_photo)  # Добавляем фото в сессию для сохранения

        # Обновление связи courses вручную
        selected_courses = [Course.query.get(course_id) for course_id in form.course_id.data]
        module_db.courses = selected_courses

        # Обновление связи lessons вручную
        selected_lessons = [Lesson.query.get(lesson_id) for lesson_id in form.lessons.data]
        module_db.lessons = selected_lessons

        db.session.commit()
        flash("Модуль успешно обновлен!", "success")
        return redirect(url_for(".edit_module", module_id=module_id))

    modules_db = Module.query.all()  # Получаем все модули из базы данных

    return render_template(
        "courses/admin/edit-module.j2",
        form=form,
        module=module_db,
        module_id=module_id,
        modules=modules_db)


@admin_courses.route("/delete-module/<int:module_id>", methods=["GET"])
@admin_courses.route("/delete-module/<int:course_id>/<int:module_id>", methods=["GET"])
def delete_module(course_id=None, module_id=None):
    module_db = Module.query.get_or_404(module_id)
    if course_id:
        course_db = Course.query.get_or_404(course_id)

    # Удаляем модуль из указанного курса
    if course_id and module_db in course_db.modules:
        course_db.modules.remove(module_db)
        db.session.delete(module_db)  # Удаляем модуль из базы данных
        db.session.commit()
        flash("Модуль успешно удален из курса!", "success")
    else:
        db.session.delete(module_db)
        db.session.commit()
        flash("Модуль успешно удален без курса!", "warning")

    return redirect(url_for(".index"))


@admin_courses.route("/add-lesson", methods=["GET", "POST"])
def add_lesson():
    form = LessonForm(request.form)
    form.module_id.choices = [(module.id, module.title) for module in Module.query.all()]

    if form.validate_on_submit():
        lesson_db = Lesson(
            module_id=form.data["module_id"],
            title=form.data["title"],
            alias=form.data["alias"],
            description=form.data["description"],
            video_url=form.data["video_url"],
        )

        # Обработка загруженных фото
        if form.photo.data:
            for file in form.photo.data:
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = photos.save(file)
                    new_photo = Photo(
                        filename=filename,
                        alt=f'Изображение для {form.title.data}',
                    )
                    lesson_db.photos.append(new_photo)
                    db.session.add(new_photo)  # Добавляем фото в сессию для сохранения

         # Обработка видео
        if form.video.data:
            for file in form.video.data:
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = videos.save(file)
                    new_video = Video(
                        filename=filename,
                        alt=f'Видео для {form.title.data}',
                    )
                    lesson_db.videos.append(new_video)
                    db.session.add(new_video)

        # Обработка других файлов
        if form.file.data:
            file = form.file.data
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = files.save(file)
                lesson_db.file = filename  # Сохраняем путь к файлу


        db.session.add(lesson_db)
        db.session.commit()

        flash("Урок успешно сохранен!", "success")
        return redirect(url_for(".index"))

    lessons_db = Lesson.query.all()  # Получаем все уроки из базы данных

    return render_template(
        "courses/admin/add-lesson.j2",
        form=form,
        lessons=lessons_db)


@admin_courses.route("/edit-lesson/<int:lesson_id>", methods=["GET","POST"])
def edit_lesson(lesson_id):
    lesson_db = Lesson.query.get_or_404(lesson_id)
    form = LessonForm(obj=lesson_db)
    form.module_id.choices = [(module.id, module.title) for module in Module.query.all()]

    if form.validate_on_submit():
        lesson_db.module_id = form.module_id.data
        lesson_db.title = form.title.data
        lesson_db.alias = form.alias.data
        lesson_db.description = form.description.data
        lesson_db.video_url = form.video_url.data.strip()  # сохраняем полную ссылку на видео

        if form.photo.data:
          for file in form.photo.data:
              if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                  filename = photos.save(file)
                  new_photo = Photo(
                      filename=filename,
                      alt=f'Изображение для {form.title.data}',
                  )
                  lesson_db.photos.append(new_photo)
                  db.session.add(new_photo)  # Добавляем фото в сессию для сохранения

         # Обработка видео
        if form.video.data:
            for file in form.video.data:
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = videos.save(file)
                    new_video = Video(
                        filename=filename,
                        alt=f'Видео для {form.title.data}',
                    )
                    lesson_db.videos.append(new_video)
                    db.session.add(new_video)

        # Обработка других файлов
        if form.file.data:
            file = form.file.data
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = files.save(file)
                lesson_db.file = filename  # Сохраняем путь к файлу

        db.session.commit()
        flash("Урок успешно обновлен!", "success")
        return redirect(url_for(".edit_lesson", lesson_id=lesson_id, lesson=lesson_db))

    lessons_db = Lesson.query.all()  # Получаем все уроки из базы данных

    return render_template(
        "courses/admin/edit-lesson.j2",
        form=form,
        lessons=lessons_db,
        lesson=lesson_db,
        lesson_id=lesson_id)


@admin_courses.route("/delete-lesson/<int:lesson_id>", methods=["GET"])
def delete_lesson(lesson_id):
    lesson_db = Lesson.query.get_or_404(lesson_id)

    if lesson_db:
        db.session.delete(lesson_db)
        db.session.commit()
        flash("Урок успешно удален!", "success")
    else:
        flash("Ошибка при удалении урока!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/delete-photo/<string:entity_type>/<int:entity_id>/<int:photo_id>", methods=["GET"])
def delete_photo(entity_type, entity_id, photo_id):
    photo_db = Photo.query.get_or_404(photo_id)

    # Удаление файла с сервера, если это необходимо
    db.session.delete(photo_db)
    db.session.commit()
    flash("Фотография успешно удалена!", "success")

    # Определение редиректа на основе типа сущности
    if entity_type == "category":
        return redirect(url_for(".edit_category", category_id=entity_id))
    elif entity_type == "course":
        return redirect(url_for(".edit_course", course_id=entity_id))
    elif entity_type == "module":
        return redirect(url_for(".edit_module", module_id=entity_id))
    elif entity_type == "lesson":
        return redirect(url_for(".edit_lesson", lesson_id=entity_id))
    else:
        flash("Неизвестный тип сущности!", "danger")
        return redirect(url_for(".index"))


@admin_courses.route("/delete-video/<string:entity_type>/<int:entity_id>/<int:video_id>", methods=["GET"])
def delete_video(entity_type, entity_id, video_id):
    video_db = Video.query.get_or_404(video_id)

    # Удаление из базы данных
    db.session.delete(video_db)
    db.session.commit()
    flash("Видео успешно удалено!", "success")

    if entity_type == "lesson":
        return redirect(url_for(".edit_lesson", lesson_id=entity_id))
    else:
        flash("Неизвестный тип сущности!", "danger")
        return redirect(url_for(".index"))


@admin_courses.route("/delete-file/<int:lesson_id>", methods=["GET"])
def delete_file(lesson_id):
    lesson_db = Lesson.query.get_or_404(lesson_id)

    # Обнуляем поле с файлом в базе данных
    lesson_db.file = None
    db.session.commit()

    flash("Запись о файле успешно удалена!", "success")

    return redirect(url_for(".edit_lesson", lesson_id=lesson_id))


@admin_courses.route("/add-studentwork", methods=["GET", "POST"])
def add_studentwork():
    form = StudentWorkForm()
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

    if form.validate_on_submit():
        studentwork_db = StudentWork(
            title=form.data["title"],
            description=form.data["description"],
        )
        filename = ""
        # Обработка загруженного файла (одно фото)
        if "photo" in request.files and request.files["photo"]:
            file = request.files["photo"]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                studentwork_db.photo = filename  # Сохранение имени файла в поле photo

        db.session.add(studentwork_db)
        db.session.commit()

        # Обновление связи courses вручную
        selected_courses = Course.query.filter(Course.id.in_(form.course_id.data)).all()
        for course in selected_courses:
            course.student_works.append(studentwork_db)  # Используем уже существующее отношение

        db.session.commit()

        flash("Работа студента успешно добавлена!", "success")
        return redirect(url_for(".index"))

    studentworks_db = StudentWork.query.all()  # Получаем все работы из базы данных

    return render_template(
        "courses/admin/add-studentwork.j2",
        form=form,
        studentworks=studentworks_db)



@admin_courses.route("/edit-studentwork/<int:studentwork_id>", methods=["GET", "POST"])
def edit_studentwork(studentwork_id):
    studentwork_db = StudentWork.query.get_or_404(studentwork_id)
    form = StudentWorkForm(obj=studentwork_db)

    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

    if request.method == "GET":
        # Предзаполнение выбранных курсов
        form.course_id.data = [course.id for course in studentwork_db.courses]

    if form.validate_on_submit():
        studentwork_db.title = form.title.data
        studentwork_db.description = form.description.data

        # Обработка загруженного файла (одно фото)
        if form.photo.data:
            file = form.photo.data[0]  # Берем только первое фото из списка
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                studentwork_db.photo = filename  # Сохраняем новое имя файла

        # Обновление связанных курсов
        selected_course_ids = form.course_id.data
        # Получение объектов курсов по выбранным ID
        selected_courses = Course.query.filter(Course.id.in_(selected_course_ids)).all()
        # Присвоение новых курсов (это автоматически обновит связи)
        studentwork_db.courses = selected_courses

        db.session.commit()
        flash("Работа студента успешно обновлена!", "success")
        return redirect(url_for(".edit_studentwork", studentwork_id=studentwork_id))

    studentworks_db = StudentWork.query.all()  # Получаем все работы студентов из базы данных

    return render_template(
        "courses/admin/edit-studentwork.j2",
        form=form,
        studentworks=studentworks_db,
        studentwork=studentwork_db,
        studentwork_id=studentwork_id)



@admin_courses.route("/delete-studentwork/<int:studentwork_id>", methods=["GET"])
def delete_studentwork(studentwork_id):
    studentwork_db = StudentWork.query.get_or_404(studentwork_id)

    if studentwork_db:
         # Удаление всех связей перед удалением `StudentWork`
        studentwork_db.courses = []
        db.session.commit()  # Обновление сессии, чтобы сохранить изменения в отношениях

        db.session.delete(studentwork_db)
        db.session.commit()
        flash("Работа студента успешно удалена!", "success")
    else:
        flash("Ошибка при удалении работы студента!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/add-artist", methods=["GET", "POST"])
def add_artist():
    form = ArtistForm()
    # Заполнение выбора для user_id с именами пользователей
    form.user_id.choices = [(user.id, f"{user.first_name} {user.last_name}") for user in User.query.all()]

    # Заполнение выбора для курсов
    form.courses.choices = [(course.id, course.title) for course in Course.query.all()]

    if form.validate_on_submit():
        artist_db = Artist(
            user_id=form.user_id.data,
            bio=form.bio.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            profession=form.profession.data,
            show_on_homepage=form.show_on_homepage.data,
            instagram=form.instagram.data,
            facebook=form.facebook.data,
            youtube=form.youtube.data,
            vkontakte=form.vkontakte.data,

        )

        # Обработка загруженного файла (одно фото)
        if form.avatar.data:
            # Загружается только одна фотография
            file = form.avatar.data[0]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                artist_db.avatar = filename  # Сохранение имени файла в поле avatar

        # Добавление курсов
        artist_db.courses.extend(Course.query.filter(Course.id.in_(form.courses.data)).all())

        db.session.add(artist_db)
        db.session.commit()

        flash("Мастер успешно добавлен!", "success")
        return redirect(url_for(".index"))

    artists_db = Artist.query.all()  # Получаем всх мастеров из базы данных

    return render_template(
        "courses/admin/add-artist.j2",
        form=form,
        artists=artists_db)


@admin_courses.route("/edit-artist/<int:artist_id>", methods=["GET", "POST"])
def edit_artist(artist_id):
    artist_db = Artist.query.get_or_404(artist_id)  # Получаем объект Artist или возвращаем 404
    form = ArtistForm(obj=artist_db)  # Создаем форму, используя объект Artist

    # Заполнение выбора для user_id с именами пользователей
    form.user_id.choices = [(user.id, f"{user.first_name} {user.last_name}") for user in User.query.all()]

    # Заполнение выбора для курсов
    form.courses.choices = [(course.id, course.title) for course in Course.query.all()]

    if request.method == "GET":
        # Предзаполнение выбранных курсов
        form.courses.data = [course.id for course in artist_db.courses]

    if form.validate_on_submit():
        artist_db.user_id = form.user_id.data
        artist_db.first_name = form.first_name.data
        artist_db.last_name = form.last_name.data
        artist_db.profession = form.profession.data
        artist_db.bio = form.bio.data
        artist_db.show_on_homepage = form.show_on_homepage.data
        artist_db.instagram = form.instagram.data
        artist_db.facebook = form.facebook.data
        artist_db.youtube = form.youtube.data
        artist_db.vkontakte = form.vkontakte.data


        # Обработка загруженного файла (одно фото)
        if form.avatar.data:
            file = form.avatar.data[0]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                artist_db.avatar = filename  # Обновление имени файла в поле avatar

        # Обновление связанных курсов
        selected_course_ids = form.courses.data
        selected_courses = Course.query.filter(Course.id.in_(selected_course_ids)).all()
        artist_db.courses = selected_courses

        db.session.commit()  # Сохранение изменений в базе данных
        flash("Информация о мастере успешно обновлена!", "success")
        return redirect(url_for(".index"))

    artists_db = Artist.query.all()  # Получаем всх мастеров из базы данных

    return render_template(
        "courses/admin/edit-artist.j2",
        form=form,
        artists=artists_db,
        artist_id=artist_id,
        artist=artist_db)

@admin_courses.route("/remove-artist-from-course/<int:course_id>/<int:artist_id>", methods=["GET"])
def remove_artist_from_course(course_id, artist_id):
    course_db = Course.query.get_or_404(course_id)
    artist_db = Artist.query.get_or_404(artist_id)

    if artist_db in course_db.artists:
        course_db.artists.remove(artist_db)
        db.session.commit()  # Просто удаляем связь
        flash("Мастер успешно удален из курса!", "success")
    else:
        flash("Мастер не найден в этом курсе!", "warning")

    return redirect(url_for(".edit_course", course_id=course_id))


@admin_courses.route("/delete-artist/<int:artist_id>", methods=["GET"])
def delete_artist(artist_id):
    artist_db = Artist.query.get_or_404(artist_id)

    if artist_db:
        # Удаление всех связанных ArtistWork перед удалением мастера
        artist_db.works.delete()

        db.session.delete(artist_db)
        db.session.commit()
        flash("Мастер и его работы успешно удалены!", "success")
    else:
        flash("Ошибка при удалении мастера!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/save-selected-artists", methods=["GET", "POST"])
def save_selected_artists():
    # Получаем список всех курсов из базы данных
    artists = Artist.query.all()

    if request.method == "POST":
        # Проходим по всем курсам и собираем выбранные для показа на главной странице
        for artist in artists:
            checkbox_name = f"show_on_homepage_{artist.id}"
            if checkbox_name in request.form:
                artist.show_on_homepage = True
            else:
                artist.show_on_homepage = False

        # Сохраняем изменения в базе данных
        db.session.commit()

        flash(f"Выбранные мастера обновлены", "success")
        return redirect(url_for('.index'))

    return render_template("courses/admin/save-selected-artists.j2", artists=artists)


@admin_courses.route("/add-artistwork", methods=["GET", "POST"])
def add_artistwork():
    form = ArtistWorkForm()
    form.artist_id.choices = [(artist.id, artist.user.name) for artist in Artist.query.all()]

    if form.validate_on_submit():
        artistwork_db = ArtistWork(
            title=form.data["title"],
            description=form.data["description"],
            artist_id=form.data["artist_id"],
        )
        filename = ""
        # Обработка загруженного файла (одно фото)
        if "photo" in request.files and request.files["photo"]:
            file = request.files["photo"]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                artistwork_db.photo = filename  # Сохранение имени файла в поле photo

        db.session.add(artistwork_db)
        db.session.commit()

        flash("Работа мастера успешно добавлена!", "success")
        return redirect(url_for(".index"))

    artistworks_db = ArtistWork.query.all()  # Получаем все работы из базы данных

    return render_template(
        "courses/admin/add-artistwork.j2",
        form=form,
        artistworks=artistworks_db)


@admin_courses.route("/edit-artistwork/<int:artistwork_id>", methods=["GET", "POST"])
def edit_artistwork(artistwork_id):
    artistwork_db = ArtistWork.query.get_or_404(artistwork_id)
    form = ArtistWorkForm(obj=artistwork_db)
    form.artist_id.choices = [(artist.id, artist.user.name) for artist in Artist.query.all()]

    # Предзаполнение выбранного мастера
    form.artist_id.data = artistwork_db.artist_id

    if form.validate_on_submit():
        artistwork_db.title = form.title.data
        artistwork_db.description = form.description.data
        artistwork_db.artist_id = form.artist_id.data

        # Обработка загруженного файла (одно фото)
        if "photo" in request.files and request.files["photo"]:
            file = request.files["photo"]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                artistwork_db.photo = filename  # Обновление имени файла в поле photo

        db.session.commit()
        flash("Работа мастера успешно обновлена!", "success")
        return redirect(url_for(
            ".edit_artistwork",
            artistwork_id=artistwork_id))

    artistworks_db = ArtistWork.query.all()  # Получаем все работы мастера из базы данных

    return render_template(
        "courses/admin/edit-artistwork.j2",
        form=form,
        artistworks=artistworks_db,
        artistwork_id=artistwork_id,
        artistwork=artistwork_db,
        )


@admin_courses.route("/delete-artistwork/<int:artistwork_id>", methods=["GET"])
def delete_artistwork(artistwork_id):
    artistwork_db = ArtistWork.query.get_or_404(artistwork_id)

    if artistwork_db:
        db.session.delete(artistwork_db)
        db.session.commit()
        flash("Работа мастера успешно удалена!", "success")
    else:
        flash("Ошибка при удалении работы мастера!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/add-tariff", methods=["GET", "POST"])
def add_tariff():
    form = TariffForm()
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

    if form.validate_on_submit():
        if "photo" not in request.files or not request.files["photo"]:
            flash("Загрузка фотографии обязательна при создании тарифа.", "danger")
            return render_template(
                "courses/admin/add-tariff.j2",
                form=form,
                tariffs=Tariff.query.all(),
                courses=Course.query.all(),
            )

        tariff_db = Tariff(
          title=form.data["title"],
          description = form.data["description"],
          price = form.data["price"],
          discount = form.data["discount"] or 0.0, # подставляется 0.0 если поле пусто
        )

        file = request.files["photo"]
        if file and file.filename:
            filename = photos.save(file)
            tariff_db.photo = filename

        db.session.add(tariff_db)
        db.session.commit()

        # Обновление связи courses вручную
        selected_courses = Course.query.filter(Course.id.in_(form.course_id.data)).all()
        for course in selected_courses:
            course.tariffes.append(tariff_db)  # Используем уже существующее отношение

        db.session.commit()

        flash("Тариф успешно добавлен!", "success")
        return redirect(url_for(".index"))

    tariffs_db = Tariff.query.all()  # Получаем все тарифы из базы данных
    courses_db = Course.query.all()  # Загружаем курсы для передачи в шаблон

    return render_template(
        "courses/admin/add-tariff.j2",
        form=form,
        tariffs=tariffs_db,
        courses=courses_db)


@admin_courses.route("/edit-tariff/<int:tariff_id>", methods=["GET", "POST"])
def edit_tariff(tariff_id):
    tariff_db = Tariff.query.get_or_404(tariff_id)
    form = TariffForm(obj=tariff_db)

     # Заполнение выборок для курсов
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

    if request.method == "GET":
        # Предзаполнение выбранных курсов
        form.course_id.data = [course.id for course in tariff_db.courses]

    if form.validate_on_submit():
        tariff_db.title = form.title.data
        tariff_db.description = form.description.data
        tariff_db.price = form.price.data
        tariff_db.discount = form.discount.data or 0.0 # подставляется 0.0 если поле пусто

        # Обработка загруженного файла (одно фото)
        file = request.files["photo"]
        if file and file.filename:
            filename = photos.save(file)
            tariff_db.photo = filename  # Обновляем только если загружен новый файл

        # Обновление связанных курсов
        selected_course_ids = form.course_id.data
        # Получение объектов курсов по выбранным ID
        selected_courses = Course.query.filter(Course.id.in_(selected_course_ids)).all()
        # Присвоение новых курсов (это автоматически обновит связи)
        tariff_db.courses = selected_courses

        db.session.commit()
        flash("Тариф успешно обновлен!", "success")
        return redirect(url_for(".edit_tariff", tariff_id=tariff_id))

    tariffs_db = Tariff.query.all()  # Получаем все тарифы из базы данных
    courses_db = Course.query.all()  # Загружаем курсы для передачи в шаблон

    return render_template(
        "courses/admin/edit-tariff.j2",
        form=form,
        tariffs=tariffs_db,
        tariff_id=tariff_id,
        tariff=tariff_db,
        courses=courses_db,
        )


@admin_courses.route("/delete-tariff/<int:course_id>/<int:tariff_id>", methods=["GET"])
def delete_tariff(course_id, tariff_id):
    tariff_db = Tariff.query.get_or_404(tariff_id)
    course_db = Course.query.get_or_404(course_id)

    if tariff_db and course_db:
        # Удаление связи между курсом и тарифом
        if tariff_db in course_db.tariffes:
            course_db.tariffes.remove(tariff_db)

        db.session.commit()  # Сохраняем изменения

        flash("Связь тарифа с курсом успешно удалена!", "success")
    else:
        flash("Ошибка при удалении связи тарифа!", "danger")

    return redirect(url_for(".index"))


@admin_courses.route("/add-promo/", methods=["GET", "POST"])
def add_promo():
    form = PromoForm()
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

    if form.validate_on_submit():
        promo_db = Promo(
            title=form.data["title"],
            alias= form.data["alias"],
            description=form.data["description"],
            price=form.data["price"],
            discount=form.data["discount"],
            start_time=form.data["start_time"],
            end_time=form.data["end_time"],
        )

        filename = ""
        # Обработка загруженного файла (одно фото)
        if "photo" in request.files and request.files["photo"]:
            file = request.files["photo"]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                promo_db.photo = filename  # Сохранение имени файла в поле photo

        db.session.add(promo_db)
        db.session.commit()

        # Обновление связи courses вручную
        selected_courses = Course.query.filter(Course.id.in_(form.course_id.data)).all()
        for course in selected_courses:
            course.promos.append(promo_db)  # Используем уже существующее отношение

        db.session.commit()
        flash("Акция успешно добавленa!", "success")
        return redirect(url_for(".index"))

    promos_db = Promo.query.all()  # Получаем все промо-коды из базы данных

    return render_template(
        "courses/admin/add-promo.j2",
        form=form,
        promos=promos_db,
    )


@admin_courses.route("/add-promo/<int:promo_id>", methods=["GET", "POST"])
def edit_promo(promo_id):
    promo_db = Promo.query.get_or_404(promo_id)
    form = PromoForm(obj=promo_db)

    # Заполнение выборок для курсов
    form.course_id.choices = [(course.id, course.title) for course in Course.query.all()]

    if request.method == "GET":
        # Предзаполнение выбранных курсов
        form.course_id.data = [course.id for course in promo_db.courses]

    if form.validate_on_submit():
        promo_db.title = form.title.data
        promo_db.alias = form.alias.data
        promo_db.description = form.description.data
        promo_db.price = form.price.data
        promo_db.discount = form.discount.data
        promo_db.start_time = form.start_time.data
        promo_db.end_time = form.end_time.data

        # Обработка загруженного файла (одно фото)
        if "photo" in request.files and request.files["photo"]:
            file = request.files["photo"]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                promo_db.photo = filename  # Обновление имени файла в поле photo

        # Обновление связанных курсов
        selected_course_ids = form.course_id.data
        # Получение объектов курсов по выбранным ID
        selected_courses = Course.query.filter(Course.id.in_(selected_course_ids)).all()
        # Присвоение новых курсов (это автоматически обновит связи)
        promo_db.courses = selected_courses

        db.session.commit()
        flash("Акция успешно изменена!", "success")
        return redirect(url_for(".index", promo_id=promo_id))

    promos_db = Promo.query.all()  # Получаем все промо-коды из базы данных

    return render_template(
        "courses/admin/edit-promo.j2",
        form=form,
        promos=promos_db,
        promo_id=promo_id,
        promo=promo_db,
    )


@admin_courses.route("/delete-promo/<int:promo_id>", methods=["GET"])
def delete_promo(promo_id):
    promo_db = Promo.query.get_or_404(promo_id)

    if promo_db:
        # Удаление всех связей c курсами перед удалением `Promo`
        promo_db.courses = []
        db.session.commit()  # Обновление сессии, чтобы сохранить изменения в отношениях

        db.session.delete(promo_db)
        db.session.commit()
        flash("Акция успешно удалена!", "success")
    else:
        flash("Ошибка при удалении акции!", "danger")

    return redirect(url_for(".index"))


@admin_courses.get("/payments")
def payments():
    """Вывод всех платежей в админке."""
    payments_db = Payment.query.all()
    courses_db = Course.query.all()
    return render_template("courses/admin/payments.j2", payments=payments_db, courses=courses_db)


@admin_courses.get("/payments/change-status/<int:payment_id>")
def change_payment_status(payment_id):
    """Изменение статуса оплаты по клику на кнопку в админке."""
    payment_db = Payment.query.get_or_404(payment_id)
    payment_db.status_payment = 1
    db.session.commit()
    return {"status": "success"}
