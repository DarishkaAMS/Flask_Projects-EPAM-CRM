from flask import render_template

from .views import user

########################
#### error handlers ####
########################


@user.errorhandler(401)
def forbidden_page(error):
    return render_template("errors/401.html"), 401


@user.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@user.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@user.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
