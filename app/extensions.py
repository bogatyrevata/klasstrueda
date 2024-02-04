from flask_executor import Executor
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_resize import Resize
from flask_security import Security
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# TODO: вынести в другое место
class Base(DeclarativeBase, MappedAsDataclass):
    """subclasses will be converted to dataclasses"""
    pass

csrf = CSRFProtect()
db = SQLAlchemy(model_class=Base)
executor = Executor()
mail = Mail()
migrate = Migrate()
resize = Resize()
photos = UploadSet("photos", IMAGES)
security = Security()
session = Session()
