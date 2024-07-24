from requests import post

from flask import current_app, url_for
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

