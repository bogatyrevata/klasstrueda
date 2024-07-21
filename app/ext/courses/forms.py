from flask_security import ConfirmRegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import DateField, StringField, SubmitField, TelField, FileField, EmailField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Regexp, Email


class CategoryForm(FlaskForm):
    name = StringField("Название категории", validators=[DataRequired("Название обязательно для заполнения")])
    alias = StringField("Алиас категории", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    description = TextAreaField("Описание категории")
    submit = SubmitField("Добавить категорию")


class CourseForm(FlaskForm):
    name = StringField("Название курса", validators=[DataRequired("Название обязательно для заполнения")])
    alias = StringField("Алиас курса", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    category_id = SelectField("Название категории", coerce=int, validators=[DataRequired()])
    description = TextAreaField("Краткое описание курса")
    image = FileField("Фотография к краткому описанию курса", [FileAllowed(["jpg", "png"], "Только jpg или png!")])
    level = TextAreaField("Уровень сложности курса")
    duration = TextAreaField("Продолжительность курса")
    about = TextAreaField("Описание курса")
    about_photo = FileField("Фотография к описанию курса", [FileAllowed(["jpg", "png"], "Только jpg или png!")])
    information = TextAreaField("Процесс обучени на курсе")
    features = TextAreaField("Преимущества")
    skills = TextAreaField("Чему вы научитесь")
    students_work = FileField("Работы студентов", [FileAllowed(["jpg", "png"], "Только jpg или png!")])
    promo = TextAreaField("Акция")
    registration_form = TextAreaField("Форма регистрации")
    registration_photo = FileField("Фотография для формы регистрации", [FileAllowed(["jpg", "png"], "Только jpg или png!")])
    artist = TextAreaField("Информация о мастере")
    artist_photo = FileField("Фото мастера", [FileAllowed(["jpg","png"],"Только jpg и png!")])
    artist_work = FileField("Работы мастера", [FileAllowed(["jpg", "png"])])
    price = TextAreaField("Стоимость курса")
    final_registration_form = TextAreaField("Форма регистрации")
    start_date = DateField("Дата начала курса", validators=[DataRequired()])
    end_date = DateField("Дата окончания курса", validators=[DataRequired()])
    submit = SubmitField("Добавить курс")


class ModuleForm(FlaskForm):
    course_id = SelectMultipleField("Название курса", coerce=int, validators=[DataRequired()])
    name = StringField("Название модуля", validators=[DataRequired()])
    alias = StringField("Алиас модуля", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    description = TextAreaField("Описание модуля")
    submit = SubmitField("Добавить модуль")


class LessonForm(FlaskForm):
    module_id = SelectField("Название модуля", coerce=int, validators=[DataRequired()])
    name = StringField("Название урока", validators=[DataRequired()])
    alias = StringField("Алиас урока", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    description = TextAreaField("Описание урока")
    submit = SubmitField("Добавить урок")

class HomeworkForm(FlaskForm):
    module_id = SelectField("Название модуля", coerce=int, validators=[DataRequired()])
    name = StringField("Название домашней работы", validators=[DataRequired()])
    description = TextAreaField("Описание урока")
    file = FileField("Загрузить файл", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'], 'Только файлы с расширениями: jpg, jpeg, png, pdf, doc, docx!')
    ])
    submit = SubmitField("Добавить урок")


class CourseRegistrationForm(FlaskForm):
    name = StringField("Ваше имя", [DataRequired()])
    email = EmailField("Ваш Email",
    [
        DataRequired("Email обязателен для заполнения"),
        Email("Неверный формат Email, адрес должен содержать символ @")
    ])
    message = TextAreaField("Сообщение", [DataRequired()])
    submit = SubmitField("Отправить сообщение")
