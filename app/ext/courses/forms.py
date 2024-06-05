from flask_security import ConfirmRegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TelField, FileField, EmailField, TextAreaField, SelectField
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
