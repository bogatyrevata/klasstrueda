from flask_security import ConfirmRegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TelField, FileField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email


class EditProfileForm(FlaskForm):
    """Форма редактирования пользователя."""

    userphoto = FileField("Фотография", [FileAllowed(["jpg", "png"], "Только джпег или пнг!")])
    username = StringField("Логин")
    first_name = StringField("Имя")
    last_name = StringField("Фамилия")
    phone = TelField("Телефон")
    submit = SubmitField("Сохранить")


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
    """Расширенная форма регистрации."""

    first_name = StringField("Имя", [DataRequired()])
    last_name = StringField("Фамилия", [DataRequired()])

class FeedbackForm(FlaskForm):
    """Форма регистрации на курс и вопросов по курсу."""

    first_name = StringField("Ваше имя", [DataRequired()])
    email = EmailField("Ваш Email", [
        DataRequired("Email обязателен для заполнения"),
        Email("Неверный формат Email, адрес должен содержать символ @")
        ])
    course_title = StringField("Название курса")
    question = StringField("Ваш вопрос")
    message = TextAreaField("Сообщение", [DataRequired()])
