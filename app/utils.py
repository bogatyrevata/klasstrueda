import time
from requests import post

from flask import current_app, url_for
from flask_mailman import EmailMessage
from flask_resize.exc import ImageNotFoundError

from app.extensions import resize


def url_for_icon(icon_name: str) -> str:
    """Формирование пути к иконке из спрайта."""
    filename = f"img/sprite.svg#{icon_name}"
    return url_for("static", filename=filename).replace("%23", "#")


def url_for_resize(
    filename: str,
    width: int = 200,
    height: int = 150,
    ext: str = "jpg",
    fill: bool = False,
):
    try:
        return resize(url_for("static", filename=filename), f"{width}x{height}", format=ext, fill=fill)
    except ImageNotFoundError as err:
        current_app.logger.error(f"Изображение '{filename}' не найдено {err}")
    return url_for("static", filename="images/no-image.jpg")

# функция отправки сообщения в телеграмм
def send_to_telegram(message, chat_id=None, send_to_admin=False):
    """Отправляет сообщение в указанный чат Telegram и админу, если send_to_admin указан.

    :param message: Текст сообщения
    :param chat_id: Идентификатор чата, куда будет отправлено сообщение
    :param send_to_admin: Флаг, указывающий на необходимость отправки сообщения админу
    """
    # Использование значения по умолчанию из конфигурации, если chat_id не передан
    if not chat_id:
        chat_id = current_app.config["TELEGRAM_CHAT_ID"]

    token = current_app.config["TELEGRAM_TOKEN"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Отправка сообщения в основной чат
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    response = post(url, data=data)
    if response.status_code == 200:
        current_app.logger.info("Сообщение успешно отправлено в чат %s", chat_id)
    else:
        current_app.logger.error("Ошибка при отправке сообщения в чат %s", chat_id)
        current_app.logger.debug(response.text)

    # Отправка сообщения админу, если send_to_admin установлен в True
    if send_to_admin:
        admin_id = current_app.config.get("TELEGRAM_ADMIN_ID")
        if admin_id:
            data["chat_id"] = admin_id
            response = post(url, data=data)
            if response.status_code == 200:
                current_app.logger.info("Сообщение успешно отправлено админу %s", admin_id)
            else:
                current_app.logger.error("Ошибка при отправке сообщения админу %s", admin_id)
                current_app.logger.debug(response.text)
        else:
            current_app.logger.error("Переменная окружения TELEGRAM_ADMIN_ID не установлена")

def send_to_email(subject, body, recipients, sender=None, reply_to=None):
    """
    Отправляет email с заданным содержимым.

    :param subject: Тема сообщения
    :param body: Тело сообщения
    :param recipients: Список получателей
    :param sender: Отправитель (если не указан, будет использован MAIL_DEFAULT_SENDER)
    :param reply_to: Адрес для ответа (опционально)
    """
    if not sender:
        sender = current_app.config['MAIL_DEFAULT_SENDER']

    msg = EmailMessage(
        subject,
        body,
        sender,
        recipients,
        reply_to=reply_to
    )
    msg.send()


def is_form_too_fast(form_time_field: str | int) -> bool:
    """Проверка: не слишком ли быстро отправлена форма (защита от ботов)"""
    try:
        form_time = int(form_time_field)
    except (ValueError, TypeError):
        return True
    current_time = int(time.time() * 1000)
    return current_time - form_time < 2000


def send_admin_notification(name, email, course_title=None, tariff_title=None, price=None, message=None, method=None):
    """Отправляет уведомление администратору о новой заявке"""
    if message:
        body = f"Новая заявка на курс:\nИмя: {name}\nEmail: {email}\nСообщение: {message}"
    else:
        body = (
            f"Новая заявка на курс:\n"
            f"Имя: {name}\nEmail: {email}\n"
            f"Курс: {course_title}\n"
            f"Тариф: {tariff_title}\n"
            f"Цена: {price}\n"
            f"Способ оплаты: {method}"
        )

    send_to_telegram(body, send_to_admin=True)
    send_to_email(
        subject="Новая заявка на курс",
        body=body,
        recipients=['bogatyrevata@gmail.com'],
        sender='klasstruedaru@gmail.com',
        reply_to=['klasstruedaru@gmail.com']
    )


def send_user_email(subject, body, recipient_email):
    """Отправляет письмо пользователю"""
    send_to_email(
        subject=subject,
        body=body,
        recipients=[recipient_email],
        sender='klasstruedaru@gmail.com',
        reply_to=['klasstruedaru@gmail.com']
    )

