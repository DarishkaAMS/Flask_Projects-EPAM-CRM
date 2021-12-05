"""
__init__.py file of views module with imported auth, employee_view and department_view submodules
Register user blueprint
Represent the logic on '/' and '/home' routes
"""


# pylint: disable=cyclic-import
from flask import Blueprint
from flask import render_template, session, g

user = Blueprint('user', __name__)

# pylint: disable=import-self
# pylint: disable=wrong-import-position
# because the blueprint must be registered before importing the views
from . import auth
from . import employee_view
from . import department_view
from .. import create_app

@user.route('/')
@user.route('/home')
def home_page():
    """
    Render the home page template on the '/' or '/home' routes
    """
    app = create_app()
    app.logger.info(f'User visited homepage')
    return render_template('home.html')
