"""
__init__.py file of views module with
imported auth, employee_view and department_view submodules
Register the user blueprint and specify the logic on '/' and '/home' addresses
"""

# pylint: disable=cyclic-import
from flask import Blueprint
from flask import render_template

user = Blueprint('user', __name__)

# pylint: disable=import-self
# pylint: disable=wrong-import-position
# because the blueprint must be registered before importing the views
from . import auth
from . import employee_view
from . import department_view


@user.route('/')
@user.route('/home')
def home_page():
    """
    Render the home page template on the / or /home route
    """
    return render_template('home.html')
