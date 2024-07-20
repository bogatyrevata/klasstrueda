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
