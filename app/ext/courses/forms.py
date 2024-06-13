from flask_security import ConfirmRegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TelField, FileField, EmailField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Regexp


class CategoryForm(FlaskForm):
    name = StringField("Название категории", validators=[DataRequired()])
    alias = StringField("Алиас категории", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    description = TextAreaField("Описание категории")
    submit = SubmitField("Добавить категорию")

class CourseForm(FlaskForm):
    name = StringField("Название курса", validators=[DataRequired()])
    alias = StringField("Алиас курса", validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9_-]+$', message="Алиас должен содержать только латинские буквы, цифры, дефисы и подчеркивания.")
    ])
    category_id = SelectField("Название категории", coerce=int, validators=[DataRequired()])
    description = TextAreaField("Описание курса")
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
