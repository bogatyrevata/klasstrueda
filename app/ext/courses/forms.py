from flask_security import ConfirmRegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TelField, FileField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email


class CategoryForm(FlaskForm):
    name = StringField("Название категории", validators=[DataRequired()])
    alias = StringField("Алиас категории", validators=[DataRequired()])  # TODO: добавить валидатор на латиницу
    description = TextAreaField("Описание категории")
    submit = SubmitField("Добавить категорию")
