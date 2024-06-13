from flask import Blueprint, current_app, g, jsonify, render_template, request
from flask_wtf.csrf import CSRFError

error = Blueprint("error", __name__, template_folder="templates")


@error.app_errorhandler(CSRFError)
def csrf_error(error_message):
    g.breadcrumbs = [{"title": "Ошибка CSRF"}]
    title = "Ошибка CSRF"
    message = "Попробуйте отправить заново"
    current_app.logger.info(f"CSRF: {request.url} {error_message}")
    if request.is_json:
        return jsonify({"success": False, "title": title, "message": message}), 400
    return (
        render_template("errors/error.j2", error=error_message, title=title, message=message, link=request.url_rule),
        400,
    )


@error.app_errorhandler(403)
def forbidden(error_message):
    g.breadcrumbs = [{"title": "Forbidden"}]
    current_app.logger.info(f"403: {request.url} {error_message}")
    return render_template("errors/403.j2", error=error_message), 403


@error.app_errorhandler(404)
def page_not_found(error_message):
    g.breadcrumbs = [{"title": "Not found"}]
    current_app.logger.info(f"404: {request.url} {error_message}")
    return render_template("errors/4xx.j2", error=error_message), 404


@error.app_errorhandler(405)
def method_not_allowed(error_message):
    g.breadcrumbs = [{"title": "Error"}]
    current_app.logger.info(f"405: {request.url} {error_message}")
    return render_template("errors/4xx.j2", error=error_message), 405


@error.app_errorhandler(500)
def internal_server(error_message):
    g.breadcrumbs = [{"title": "System error"}]
    current_app.logger.error(f"500: {request.url} {error_message}")
    return render_template("errors/500.j2", error=error_message), 500
