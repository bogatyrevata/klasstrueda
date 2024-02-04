import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from flask_security import uia_email_mapper, uia_phone_mapper, uia_username_mapper

load_dotenv()

BASE_APP_NAME = os.getenv("APP_NAME", "KlassTrueda")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EXT_DIR = os.path.join(BASE_DIR, "app/ext")
LOGS_DIR = os.path.join(BASE_DIR, "log")
TZ = ZoneInfo("Europe/Moscow")


class BaseConfig:
    """Базовый конфиг."""

    APP_NAME = BASE_APP_NAME
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION")

    MAIL_ADMINS = ["admin@gu.ru"]
    MAIL_BACKEND = os.getenv("MAIL_BACKEND", "console")
    MAIL_DEFAULT_SENDER = (BASE_APP_NAME, "team@jokerinteractive.ru")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "465"))
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", None)
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", None)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    RESIZE_DOMAIN = os.getenv("RESIZE_DOMAIN", "127.0.0.1:5000")
    RESIZE_ROOT = os.path.join(BASE_DIR, "app")
    RESIZE_URL = os.getenv("RESIZE_URL", "http://127.0.0.1:5000/")
    RESIZE_TARGET_DIRECTORY = "static/images/cache"
    RESIZE_CACHE_STORE = os.getenv("RESIZE_CACHE_STORE", "noop")
    RESIZE_REDIS_KEY = os.getenv("RESIZE_REDIS_KEY", "joker-core")
    # RESIZE_REDIS_PASSWORD = os.getenv("RESIZE_REDIS_PASSWORD")

    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_USERNAME_ENABLE = True

    # SECURITY_PHONE_REGION_DEFAULT = "RU"
    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {"email": {"mapper": uia_email_mapper, "case_insensitive": True}},
        {"username": {"mapper": uia_username_mapper}},
    ]

    # SECURITY_TWO_FACTOR_ENABLED_METHODS = ["email", "authenticator", "sms"]
    # SECURITY_US_ENABLED_METHODS = ["password", "email", "sms"]
    # SECURITY_TOTP_SECRETS = {"1": "ZjQ9Qa31VOrfEzuPy4VHQWPCTmRzCnFzMKLxXYiZu8A"}

    SECURITY_PASSWORD_LENGTH_MIN = 5
    SECURITY_POST_LOGIN_VIEW = "/lk"
    SECURITY_EMAIL_SENDER = (BASE_APP_NAME, "team@jokerinteractive.ru")

    SECURITY_LOGIN_USER_TEMPLATE = "security/login.j2"
    SECURITY_US_SIGNIN_TEMPLATE = "security/us_signin.j2"
    SECURITY_REGISTER_USER_TEMPLATE = "security/register.j2"
    SECURITY_RESET_PASSWORD_TEMPLATE = "security/reset.j2"
    SECURITY_FORGOT_PASSWORD_TEMPLATE = "security/forgot.j2"
    SECURITY_CHANGE_PASSWORD_TEMPLATE = "security/change.j2"
    SECURITY_SEND_CONFIRMATION_TEMPLATE = "security/confirm.j2"

    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "Super-Secret-Salt!1@#$%^&*")

    SESSION_COOKIE_SECURE = False
    SESSION_FILE_DIR = os.path.join(BASE_DIR, "sessions")
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 60 * 60

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DB_DRIVER = "sqlite"
    SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}:///:memory:"

    UPLOADED_PHOTOS_DEST = "static/upload"

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "xcvsdrfgohlkjn,sdasdfIWE!@#$%^&*"
    WTF_CSRF_SSL_STRICT = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """Конфиг для разработки."""

    ENV = "development"
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "liualdsknbkjzxcvoaewrASDV76s!@#$%^&*")
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}

    DB_DRIVER = "mysql+mysqldb"
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"



class TestingConfig(DevelopmentConfig):
    """Конфиг для тестирования."""

    ENV = "testing"
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Боевой конфиг."""

    # DB_DRIVER = "postgresql+psycopg2"
    # DB_USER = os.getenv("DB_USER")
    # DB_PASS = os.getenv("DB_PASS")
    # DB_HOST = os.getenv("DB_HOST", "localhost")
    # DB_PORT = os.getenv("DB_PORT", "5432")
    # DB_NAME = os.getenv("DB_NAME")
    # SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DB_DRIVER = "sqlite+pysqlite"
    DB_FILE_NAME = f'{os.getenv("DB_FILE_NAME", "app")}.db'
    DB_PATH = os.path.join(BASE_DIR, DB_FILE_NAME)
    SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}:///{DB_PATH}"

    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     "pool_size": 10,
    #     "pool_recycle": 3600,
    #     "pool_pre_ping": True,
    # }

    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "jasdhfgkjhasdgkvD!@#$%^&*")
