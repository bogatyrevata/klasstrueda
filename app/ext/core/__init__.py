"""Базовое расширение Joker Core."""

__version__ = "0.4.0"
__author__ = "MakeHTML Team"

from .views import core
from .views.admin import admin
from .views.error import error
from .views.user import user

bps = [(core, "/"), (error, "/"), (user, "/lk"), (admin, "/admin")]
