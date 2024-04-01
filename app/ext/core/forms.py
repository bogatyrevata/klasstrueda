from flask_security import ConfirmRegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    """Форма редактирования пользователя."""

    username = StringField("Логин")
    first_name = StringField("Имя")
    last_name = StringField("Фамилия")
    phone = TelField("Телефон")
    submit = SubmitField("Сохранить")


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    """Расширенная форма регистрации."""

    first_name = StringField("Имя", [DataRequired()])
    last_name = StringField("Фамилия", [DataRequired()])
