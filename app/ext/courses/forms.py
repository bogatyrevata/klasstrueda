from flask_security import ConfirmRegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import DateField, StringField, SubmitField, TelField, FileField, EmailField, MultipleFileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Regexp, Email


class CategoryForm(FlaskForm):
    title = StringField("Название категории", validators=[DataRequired("Название обязательно для заполнения")])
    alias = StringField("Алиас категории", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    description = TextAreaField("Описание категории")
    photo = MultipleFileField("Фотографии к категории курса",  validators=[FileAllowed(["jpg", "png"], "Только jpg или png!")])
    submit = SubmitField("Добавить категорию")


class CourseForm(FlaskForm):
    title = StringField("Название курса", validators=[DataRequired("Название обязательно для заполнения")])
    alias = StringField("Алиас курса", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    category_id = SelectField("Название категории", coerce=int, validators=[DataRequired()])
    preview_description = TextAreaField("Краткое описание курса")
    preview_photo = MultipleFileField("Фотография к краткому описанию курса", [FileAllowed(["jpg", "png"], "Только jpg или png!")])
    level = TextAreaField("Уровень сложности курса")
    duration = TextAreaField("Продолжительность курса")
    about = TextAreaField("Описание курса")
    about_photo = MultipleFileField("Фотография к описанию курса", [FileAllowed(["jpg", "png"], "Только jpg или png!")])
    information = TextAreaField("Процесс обучени на курсе")
    features = TextAreaField("Преимущества")
    skills = TextAreaField("Чему вы научитесь")
    registration_form = TextAreaField("Форма регистрации")
    registration_photo = MultipleFileField("Фотография для формы регистрации", [FileAllowed(["jpg", "png"], "Только jpg или png!")])
    artist_description = TextAreaField("Информация о мастере")
    artist_photo = MultipleFileField("Фото мастера", [FileAllowed(["jpg","png"],"Только jpg и png!")])
    artist_work = MultipleFileField("Работы мастера", [FileAllowed(["jpg", "png"])])
    price = TextAreaField("Стоимость курса")
    final_registration_form = TextAreaField("Форма регистрации")
    start_date = DateField("Дата начала курса", validators=[DataRequired()])
    end_date = DateField("Дата окончания курса", validators=[DataRequired()])
    modules = SelectMultipleField("Модули", coerce=int)  # добавляем поле для выбора модулей
    submit = SubmitField("Добавить курс")


class ModuleForm(FlaskForm):
    course_id = SelectMultipleField("Название курса", coerce=int, validators=[DataRequired()])
    title = StringField("Название модуля", validators=[DataRequired()])
    alias = StringField("Алиас модуля", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    description = TextAreaField("Описание модуля")
    photo = MultipleFileField("Фотографии к модулю курса",  validators=[FileAllowed(["jpg", "png"], "Только jpg или png!")])
    lessons = SelectMultipleField("Уроки", coerce=int)
    submit = SubmitField("Добавить модуль")


class LessonForm(FlaskForm):
    module_id = SelectField("Название модуля", coerce=int, validators=[DataRequired()])
    title = StringField("Название урока", validators=[DataRequired()])
    alias = StringField("Алиас урока", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    description = TextAreaField("Описание урока")
    videos = FileField("Загрузить видео", validators=[
        FileAllowed(['mp4', 'avi', 'mov'], 'Только видео с расширениями: mp4, avi, mov!')
    ])
    fotos = FileField("Загрузить фото", validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Только фото с расширениями: jpg, jpeg, png!')
    ])
    file = FileField("Загрузить файл", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'], 'Только файлы с расширениями: jpg, jpeg, png, pdf, doc, docx!')
    ])
    submit = SubmitField("Добавить урок")

    # mp4, avi, mov


class HomeworkForm(FlaskForm):
    module_id = SelectField("Название модуля", coerce=int, validators=[DataRequired()])
    title = StringField("Название домашней работы", validators=[DataRequired()])
    description = TextAreaField("Описание урока")
    file = FileField("Загрузить файл", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'], 'Только файлы с расширениями: jpg, jpeg, png, pdf, doc, docx!')
    ])
    submit = SubmitField("Добавить домашнюю работу")


class StudentWorkForm(FlaskForm):
    course_id = SelectMultipleField("Название курса", coerce=int, validators=[DataRequired()])
    title = StringField("Имя студента", validators=[DataRequired()])
    description = TextAreaField("Описание работы")
    photo = MultipleFileField("Фотография работы студента", [FileAllowed(["jpg", "png"])])
    submit = SubmitField("Добавить работу студента")


class ArtistForm(FlaskForm):
    user_id = SelectField("Имя мастера", coerce=int, validators=[DataRequired()])
    avatar = MultipleFileField("Фотография мастера", [FileAllowed(["jpg", "png"])])
    bio = TextAreaField("Информация о мастере")
    contacts = TextAreaField("Контакты")
    submit = SubmitField("Добавить мастера")


class ArtistWorkForm(FlaskForm):
    title = StringField("Название работы", validators=[DataRequired()])
    description = TextAreaField("Описание работы")
    photo = MultipleFileField("Фотография работы мастера", [FileAllowed(["jpg", "png"])])
    artist_id = SelectField("Мастер", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Добавить работу мастера")


class CourseRegistrationForm(FlaskForm):
    name = StringField("Ваше имя", [DataRequired()])
    email = EmailField("Ваш Email",
    [
        DataRequired("Email обязателен для заполнения"),
        Email("Неверный формат Email, адрес должен содержать символ @")
    ])
    message = TextAreaField("Сообщение", [DataRequired()])
    submit = SubmitField("Отправить сообщение")
