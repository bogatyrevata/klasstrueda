"""Joker Core project."""

__author__ = "MakeHTML Team"


import logging
import os
import sys
from distutils.util import strtobool
from importlib import import_module

from click import unstyle
from flask import Flask
from flask_minify import minify
from flask_uploads import configure_uploads
from loguru import logger
from werkzeug.serving import WSGIRequestHandler, _ansi_style, _log, uri_to_iri

from app.exceptions import ExtNotValidError
from app.ext.core.forms import ExtendedConfirmRegisterForm
from app.ext.core.models import user_datastore
from app.extensions import csrf, db, executor, mail, migrate, photos, resize, security, session
from app.utils import url_for_icon, url_for_resize
from config import BASE_APP_NAME, EXT_DIR, LOGS_DIR, DevelopmentConfig, ProductionConfig

DEBUG = bool(strtobool(os.getenv("DEBUG", "False")))
LOG_FILENAME = BASE_APP_NAME.lower().replace(" ", "-")
LOG_BACKTRACE = True
DEFAULT_STDOUT_LOG_LEVEL = logging.DEBUG
HANDLERS = {
    "DEBUG": [
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{message}</level> [in {file.path}:{line}]",
            "level": DEFAULT_STDOUT_LOG_LEVEL,
            "backtrace": LOG_BACKTRACE,
        },
        {"sink": f"log/{LOG_FILENAME}-debug.log", "rotation": "10 MB", "level": "DEBUG"},
        {"sink": f"log/{LOG_FILENAME}.log", "rotation": "10 MB", "level": "ERROR"},
    ],
    "PRODUCTION": [{"sink": f"log/{LOG_FILENAME}.log", "rotation": "10 MB", "level": "ERROR"}],
}


class CoreRequestHandler(WSGIRequestHandler):
    # Just like WSGIRequestHandler, but another string
    def log(self, type, message, *args):
        _log(
            type,
            f"{message} - {self.address_string()}\n",
            *args,
        )

    # Just like WSGIRequestHandler, but another, TODO: refactor
    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        try:
            path = uri_to_iri(self.path)
            msg = f"{self.command} {path} {self.request_version}"
        except AttributeError:
            # path isn't set if the requestline was bad
            msg = self.requestline

        # Escape control characters that may be in the decoded path.
        msg = msg.translate(self._control_char_table)
        code = str(code)

        if code[0] == "1":  # 1xx - Informational
            msg = _ansi_style(msg, "bold")
        elif code == "200":  # 2xx - Success
            pass
        elif code == "304":  # 304 - Resource Not Modified
            msg = _ansi_style(msg, "cyan")
        elif code[0] == "3":  # 3xx - Redirection
            msg = _ansi_style(msg, "green")
        elif code == "404":  # 404 - Resource Not Found
            msg = _ansi_style(msg, "yellow")
        elif code[0] == "4":  # 4xx - Client Error
            msg = _ansi_style(msg, "bold", "red")
        else:  # 5xx, or any other response
            msg = _ansi_style(msg, "bold", "magenta")

        self.log("info", '"%s" %s %s', msg, code, size)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        msg = record.getMessage()
        logger.opt(depth=depth, exception=record.exc_info).log(level, unstyle(msg))


def register_extensions(app: Flask) -> None:
    """Вызов метода 'init_app' для регистрации расширений в Flask объект через параметр."""
    csrf.init_app(app)
    executor.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    resize.init_app(app)
    security.init_app(app, user_datastore, confirm_register_form=ExtendedConfirmRegisterForm)
    session.init_app(app)
    configure_uploads(app, photos)


def register_blueprints(app: Flask) -> None:
    """Регистрация всех расширений (Blueprints) для приложения из папки EXT_DIR."""
    ext_list = os.listdir(EXT_DIR)
    for extension in ext_list:
        if extension.startswith("."):
            continue
        try:
            imported_module = import_module(f"app.ext.{extension}")
            bps = imported_module.bps
            version = imported_module.__version__
        except AttributeError as exc:
            raise ExtNotValidError(f"В расширении {extension} нет информации по View") from exc
        app.extensions[f"core_{extension}"] = {"version": version}
        for blueprint in bps:
            app.register_blueprint(blueprint[0], url_prefix=blueprint[1])


def create_app(config_obj=None):
    app = Flask(__name__)

    # Logging configuration
    loguru_config = {"handlers": HANDLERS["DEBUG"]}
    logger.configure(**loguru_config)

    logging.basicConfig(handlers=[InterceptHandler()], level=DEFAULT_STDOUT_LOG_LEVEL, force=True)

    logging.getLogger("sqlalchemy").setLevel(logging.WARN)
    log_werkzeug = logging.getLogger("werkzeug")
    log_werkzeug.setLevel(logging.DEBUG)

    if config_obj is None:
        config_obj = DevelopmentConfig if DEBUG else ProductionConfig
        logger.debug(f"Загружен {config_obj.__name__}")
    app.config.from_object(config_obj)
    logger.info(f"Режим DEBUG: {app.debug}")

    if not app.debug:
        minify(app=app, html=True, js=False, cssless=False)

    os.makedirs(LOGS_DIR, exist_ok=True)

    register_extensions(app)
    register_blueprints(app)

    return app


try:
    """решение проблемы с модулем MySQLdb"""
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
