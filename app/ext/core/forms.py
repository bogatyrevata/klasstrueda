from flask_security import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    """Форма редактирования пользователя."""

    username = StringField("Логин")
    firstname = StringField("Имя")
    lastname = StringField("Фамилия")
    phone = TelField("Телефон")
    submit = SubmitField("Сохранить")


class ExtendedRegisterForm(RegisterForm):
    """Расширенная форма регистрации."""

    first_name = StringField("Имя", [DataRequired()])
    last_name = StringField("Фамилия", [DataRequired()])
