from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_security import current_user, login_required

from app.ext.core.forms import EditProfileForm
from app.ext.core.models import User
from app.extensions import db, photos

customer = Blueprint("customer", __name__, template_folder="templates")
