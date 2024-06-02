"""База данных курсов"""

__version__ = "0.1.0"
__author__ = "KLASSTRUEDA"

from .views import courses
from .views.product import product
from .views.customer import customer

bps = [(courses, "/"), (customer, "/user"), (product, "/course")]
