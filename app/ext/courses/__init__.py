"""База данных курсов"""

__version__ = "0.1.0"
__author__ = "KLASSTRUEDA"

from .views import courses
from .views.user import user_courses
from .views.admin import admin_courses

bps = [(courses, "/courses"), (user_courses, "/lk/courses"), (admin_courses, "/admin/courses")]
