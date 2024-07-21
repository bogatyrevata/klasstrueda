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
def send_to_telegram(message, chat_id=None):
    """Отправляет сообщение в указанный чат Telegram.

    :param message: Текст сообщения
    :param chat_id: Идентификатор чата, куда будет отправлено сообщение
    """
    if not chat_id:
        chat_id = current_app.config["TELEGRAM_CHAT_ID"]
    token = current_app.config["TELEGRAM_TOKEN"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }

    response = post(url, data=data)

    if response.status_code == 200:
        current_app.logger.info("Сообщение успешно отправлено")
    else:
        current_app.logger.error("Ошибка при отправке сообщения")
        current_app.logger.debug(response.text)
