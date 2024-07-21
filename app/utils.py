
from flask import current_app, url_for
from flask_resize.exc import ImageNotFoundError

from app.extensions import resize
import requests


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
def send_to_telegram(token, chat_id, message):
    """
    Отправляет сообщение в указанный чат Telegram.

    :param token: Токен вашего Telegram-бота
    :param chat_id: Идентификатор чата, куда будет отправлено сообщение
    :param message: Текст сообщения
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Сообщение успешно отправлено")
    else:
        print("Ошибка при отправке сообщения")
        print(response.text)

# Пример использования
token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"
message = "Это тестовое сообщение из формы"

send_to_telegram(token, chat_id, message)
