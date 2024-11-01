import werkzeug
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from app.ext.core.models import Photo, User
from app.ext.courses.forms import CategoryForm, CourseForm, ModuleForm, LessonForm, StudentWorkForm, ArtistWorkForm, ArtistForm
from app.ext.courses.models import Category, Course, Module, Lesson, StudentWork, Artist, ArtistWork
from app.extensions import db, photos, csrf

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
        # Обработка загруженных файлов
        if "photo" in request.files and request.files["photo"]:
            for file in request.files.getlist("photo"):
                if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                    filename = photos.save(file)
                    new_photo = Photo(
                        filename=filename,
                        alt=f'Изображение для {form.data["name"]}',
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
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
    form.modules.choices = [(module.id, module.name) for module in Module.query.all()]

    if form.validate_on_submit():
        course_db = Course(
            category_id=form.data["category_id"],
            name=form.data["name"],
            alias=form.data["alias"],
            description=form.data["description"],
            level=form.data["level"],
            duration=form.data["duration"],
            about=form.data["about"],
            information=form.data["information"],
            features=form.data["features"],
            skills=form.data["skills"],
            registration_form=form.data["registration_form"],
            artist=form.data["artist"],
            price=form.data["price"],
            start_date=form.data["start_date"],
            end_date=form.data["end_date"],
            final_registration_form=form.data["final_registration_form"],
        )

        # Проверяем наличие и непустоту файла image
        if "image" in request.files and request.files["image"]:
            try:
                filename = photos.save(request.files["image"])
                course_db.image = filename
            except Exception as e:
                flash(f"Ошибка при сохранении изображения: {e}", "danger")
                return redirect(url_for(".add_course"))

        # Проверяем наличие и непустоту файла about_photo
        if "about_photo" in request.files and request.files["about_photo"]:
            try:
                filename = photos.save(request.files["about_photo"])
                course_db.about_photo = filename
            except Exception as e:
                flash(f"Ошибка при сохранении изображения: {e}", "danger")
                return redirect(url_for(".add_course"))

        # Проверяем наличие и непустоту файла students_work
        if "students_work" in request.files and request.files["students_work"]:
            try:
                filename = photos.save(request.files["students_work"])
                course_db.students_work = filename
            except Exception as e:
                flash(f"Ошибка при сохранении изображения: {e}", "danger")
                return redirect(url_for(".add_course"))

        # Проверяем наличие и непустоту файла registration_photo
        if "registration_photo" in request.files and request.files["registration_photo"]:
            try:
                filename = photos.save(request.files["registration_photo"])
                course_db.registration_photo = filename
            except Exception as e:
                flash(f"Ошибка при сохранении изображения: {e}", "danger")
                return redirect(url_for(".add_course"))

        # Проверяем наличие и непустоту файла artist_photo
        if "artist_photo" in request.files and request.files["artist_photo"]:
            try:
                filename = photos.save(request.files["artist_photo"])
                course_db.artist_photo = filename
            except Exception as e:
                flash(f"Ошибка при сохранении изображения: {e}", "danger")
                return redirect(url_for(".add_course"))

        # Проверяем наличие и непустоту файла artist_work
        if "artist_work" in request.files and request.files["artist_work"]:
            try:
                filename = photos.save(request.files["artist_work"])
                course_db.artist_work = filename
            except Exception as e:
                flash(f"Ошибка при сохранении изображения: {e}", "danger")
                return redirect(url_for(".add_course"))

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
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
    form.modules.choices = [(module.id, module.name) for module in Module.query.all()]

    # Предзаполняем выбранные модули
    if request.method == "GET":
        form.modules.data = [module.id for module in course_db.modules]

    if form.validate_on_submit():
        course_db.category_id = form.category_id.data
        course_db.name = form.name.data
        course_db.alias = form.alias.data
        course_db.description = form.description.data

        # Проверяем наличие и непустоту файла image
        if "image" in request.files and request.files["image"]:
            filename = photos.save(request.files["image"])
            course_db.image = filename

        course_db.level = form.level.data
        course_db.duration = form.duration.data
        course_db.about = form.about.data

        # Проверяем наличие и непустоту файла about_photo
        if "about_photo" in request.files and request.files["about_photo"]:
            filename = photos.save(request.files["about_photo"])
            course_db.about_photo = filename

        course_db.information = form.information.data
        course_db.features = form.features.data
        course_db.skills = form.skills.data

        # Проверяем наличие и непустоту файла students_work
        if "students_work" in request.files and request.files["students_work"]:
            filename = photos.save(request.files["students_work"])
            course_db.students_work = filename

        course_db.registration_form = form.registration_form.data

        # Проверяем наличие и непустоту файла registration_photo
        if "registration_photo" in request.files and request.files["registration_photo"]:
            filename = photos.save(request.files["registration_photo"])
            course_db.registration_photo = filename

        course_db.artist = form.artist.data

        # Проверяем наличие и непустоту файла artist_photo
        if "artist_photo" in request.files and request.files["artist_photo"]:
            filename = photos.save(request.files["artist_photo"])
            course_db.artist_photo = filename

        # Проверяем наличие и непустоту файла artist_work
        if "artist_work" in request.files and request.files["artist_work"]:
            filename = photos.save(request.files["artist_work"])
            course_db.artist_work = filename

        course_db.price = form.price.data
        course_db.final_registration_form = form.final_registration_form.data
        course_db.start_date = form.start_date.data
        course_db.end_date = form.end_date.data

        # Обработка загруженных файлов модулей

        course_db.modules = [Module.query.get(module_id) for module_id in form.modules.data]

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
    student_works = course_db.student_works
    artist_photo = course_db.artist_photo
    artist_work = course_db.artist_work
    return render_template(
        "courses/admin/edit-course.j2",
        form=form,
        course=course_id,
        course_id=course_id,
        image=image,
        about_photo=about_photo,
        registration_photo=registration_photo,
        student_works=student_works,
        artist_photo=artist_photo,
        artist_work=artist_work,
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


@admin_courses.route("/add-module", methods=["GET", "POST"])
def add_module():
    form = ModuleForm()
    form.course_id.choices = [(course.id, course.name) for course in Course.query.all()]
    form.lessons.choices = [(lesson.id, lesson.name) for lesson in Lesson.query.all()]

    if form.validate_on_submit():
        module_db = Module(
            name=form.data["name"],
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
                        alt=f'Изображение для {form.name.data}',
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

    modules = Module.query.all()  # Получаем все модули из базы данных

    return render_template("courses/admin/add-module.j2", form=form, modules=modules)


@admin_courses.route("/edit-module/<int:module_id>", methods=["GET","POST"])
def edit_module(module_id):
    module_db = Module.query.get_or_404(module_id)
    form = ModuleForm(obj=module_db)
    form.course_id.choices = [(course.id, course.name) for course in Course.query.all()]
    form.lessons.choices = [(lesson.id, lesson.name) for lesson in Lesson.query.all()]

    # Предзаполнение выбранных курсов
    form.course_id.data = [course.id for course in module_db.courses]

    # Предзаполнение выбранных уроков
    form.lessons.data = [lesson.id for lesson in module_db.lessons]

    if form.validate_on_submit():
        module_db.name = form.name.data
        module_db.alias = form.alias.data
        module_db.description = form.description.data

        if form.photo.data:
          for file in form.photo.data:
              if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                  filename = photos.save(file)
                  new_photo = Photo(
                      filename=filename,
                      alt=f'Изображение для {form.name.data}',
                  )
                  module_db.photos.append(new_photo)
                  db.session.add(new_photo)  # Добавляем фото в сессию для сохранения

        # Обновление связи courses вручную
        selected_courses = [Course.query.get(course_id) for course_id in form.course_id.data]
        module_db.courses = selected_courses

        # Обновление связи lessonsвручную
        selected_lessons = [Lesson.query.get(lesson_id) for lesson_id in form.lessons.data]
        module_db.lessons = selected_lessons

        db.session.commit()
        flash("Модуль успешно обновлен!", "success")
        return redirect(url_for(".edit_module", module_id=module_id))

    modules = Module.query.all()  # Получаем все модули из базы данных

    return render_template("courses/admin/edit-module.j2", form=form, module=module_db, module_id=module_id, modules=modules)


@admin_courses.route("/delete-module/<int:course_id>/<int:module_id>", methods=["GET"])
def delete_module(course_id, module_id):
    module_db = Module.query.get_or_404(module_id)
    course_db = Course.query.get_or_404(course_id)

    # Удаляем модуль из указанного курса
    if module_db in course_db.modules:
        course_db.modules.remove(module_db)
        db.session.commit()
        flash("Модуль успешно удален из курса!", "success")
    else:
        flash("Модуль не найден в указанном курсе!", "warning")

    return redirect(url_for(".index"))


@admin_courses.route("/add-lesson", methods=["GET","POST"])
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

    lessons = Lesson.query.all()  # Получаем все уроки из базы данных

    return render_template("courses/admin/add-lesson.j2", form=form, lessons=lessons)


@admin_courses.route("/edit-lesson/<int:lesson_id>", methods=["GET","POST"])
def edit_lesson(lesson_id):
    lesson_db = Lesson.query.get_or_404(lesson_id)
    form = LessonForm(obj=lesson_db)
    form.module_id.choices = [(module.id, module.name) for module in Module.query.all()]

    if form.validate_on_submit():
        lesson_db.module_id = form.module_id.data
        lesson_db.name = form.name.data
        lesson_db.alias = form.alias.data
        lesson_db.description = form.description.data
        db.session.commit()
        flash("Урок успешно обновлен!", "success")
        return redirect(url_for(".edit_lesson", lesson_id=lesson_id, lesson=lesson_db))

    lessons = Lesson.query.all()  # Получаем все уроки из базы данных

    return render_template("courses/admin/edit-lesson.j2", form=form, lessons=lessons, lesson=lesson_id, lesson_id=lesson_id)


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


@admin_courses.route("/add-studentwork", methods=["GET", "POST"])
def add_studentwork():
    form = StudentWorkForm()
    form.course_id.choices = [(course.id, course.name) for course in Course.query.all()]

    if form.validate_on_submit():
        studentwork_db = StudentWork(
            name=form.data["name"],
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

    studentworks = StudentWork.query.all()  # Получаем все работы из базы данных

    return render_template("courses/admin/add-studentwork.j2", form=form, studentworks=studentworks)



@admin_courses.route("/edit-studentwork/<int:studentwork_id>", methods=["GET", "POST"])
def edit_studentwork(studentwork_id):
    studentwork_db = StudentWork.query.get_or_404(studentwork_id)
    form = StudentWorkForm(obj=studentwork_db)
    form.course_id.choices = [(course.id, course.name) for course in Course.query.all()]

    # Предзаполнение выбранных курсов
    form.course_id.data = [course.id for course in studentwork_db.courses]

    if form.validate_on_submit():
        studentwork_db.name = form.name.data
        studentwork_db.description = form.description.data

        # Обработка загруженного файла (одно фото)
        if form.photo.data:
            file = form.photo.data[0]  # Берем только первое фото из списка
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                studentwork_db.photo = filename  # Сохраняем новое имя файла

        # Обновление связи courses вручную
        selected_courses = [Course.query.get(course_id) for course_id in form.course_id.data]
        studentwork_db.courses = selected_courses

        db.session.commit()
        flash("Работа студента успешно обновлена!", "success")
        return redirect(url_for(".edit_studentwork", studentwork_id=studentwork_id))

    studentworks = StudentWork.query.all()  # Получаем все работы студентов из базы данных

    return render_template(
        "courses/admin/edit-studentwork.j2",
        form=form,
        studentworks=studentworks,
        studentwork=studentwork_db,
        studentwork_id=studentwork_id,
    )


@admin_courses.route("/delete-studentwork/<int:studentwork_id>", methods=["GET"])
def delete_studentwork(studentwork_id):
    studentwork_db = StudentWork.query.get_or_404(studentwork_id)

    if studentwork_db:
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

    if form.validate_on_submit():
        artist_db = Artist(
            user_id=form.user_id.data,
            bio=form.bio.data,
            contacts=form.contacts.data,
        )

        # Обработка загруженного файла (одно фото)
        if form.avatar.data:
            # Загружается только одна фотография
            file = form.avatar.data[0]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                artist_db.avatar = filename  # Сохранение имени файла в поле avatar

        db.session.add(artist_db)
        db.session.commit()

        flash("Мастер успешно добавлен!", "success")
        return redirect(url_for(".index"))

    artists = Artist.query.all()  # Получаем всх мастеров из базы данных

    return render_template("courses/admin/add-artist.j2", form=form, artists=artists)


@admin_courses.route("/edit-artist/<int:artist_id>", methods=["GET", "POST"])
def edit_artist(artist_id):
    artist_db = Artist.query.get_or_404(artist_id)  # Получаем объект Artist или возвращаем 404
    form = ArtistForm(obj=artist_db)  # Создаем форму, используя объект Artist

    # Заполнение выбора для user_id с именами пользователей
    form.user_id.choices = [(user.id, f"{user.first_name} {user.last_name}") for user in User.query.all()]

    if form.validate_on_submit():
        artist_db.user_id = form.user_id.data
        artist_db.bio = form.bio.data
        artist_db.contacts = form.contacts.data

        # Обработка загруженного файла (одно фото)
        if form.avatar.data:
            file = form.avatar.data[0]
            if isinstance(file, werkzeug.datastructures.FileStorage) and file.filename:
                filename = photos.save(file)
                artist_db.avatar = filename  # Обновление имени файла в поле avatar

        db.session.commit()  # Сохранение изменений в базе данных
        flash("Информация о мастере успешно обновлена!", "success")
        return redirect(url_for(".index"))

    artists = Artist.query.all()  # Получаем всх мастеров из базы данных

    return render_template("courses/admin/edit-artist.j2", form=form, artists=artists, artist_id=artist_id, artist=artist_db,)


@admin_courses.route("/delete-artist/<int:artist_id>", methods=["GET"])
def delete_artist(artist_id):
     artist_db = Artist.query.get_or_404(artist_id)

     if artist_db:
        db.session.delete(artist_db)
        db.session.commit()
        flash("Работа мастера успешно удалена!", "success")
     else:
        flash("Ошибка при удалении работы мастера!", "danger")

     return redirect(url_for(".index"))


@admin_courses.route("/add-artistwork", methods=["GET", "POST"])
def add_artistwork():
    form = ArtistWorkForm()
    form.artist_id.choices = [(artist.id, artist.user.name) for artist in Artist.query.all()]

    if form.validate_on_submit():
        artistwork_db = ArtistWork(
            name=form.data["name"],
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

    artistworks = ArtistWork.query.all()  # Получаем все работы из базы данных

    return render_template("courses/admin/add-artistwork.j2", form=form, artistworks=artistworks)


@admin_courses.route("/edit-artistwork/<int:artistwork_id>", methods=["GET", "POST"])
def edit_artistwork(artistwork_id):
    artistwork_db = ArtistWork.query.get_or_404(artistwork_id)
    form = ArtistWorkForm(obj=artistwork_db)
    form.artist_id.choices = [(artist.id, artist.user.name) for artist in Artist.query.all()]

    # Предзаполнение выбранного мастера
    form.artist_id.data = artistwork_db.artist_id

    if form.validate_on_submit():
        artistwork_db.name = form.name.data
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
        return redirect(url_for(".edit_artistwork", artistwork_id=artistwork_id))

    artistworks = ArtistWork.query.all()  # Получаем все работы мастера из базы данных

    return render_template(
        "courses/admin/edit-artistwork.j2",
        form=form,
        artistworks=artistworks,
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

