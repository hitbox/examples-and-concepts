from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from markupsafe import Markup

from .models import User

fake_okta_bp = Blueprint(
    'fake_okta',
    __name__,
    template_folder = 'templates',
)

@fake_okta_bp.route('/fake-okta-login', methods=['GET', 'POST'])
def login():
    """
    Fake OKTA Login
    """
    if request.method == 'POST':
        # for fake okta just take whatever username and make a user if it
        # doesn't exist.
        user = User.get_or_create(request.form['username'])
        # login user with Flask extension
        login_user(user)
        # - flask_login usually gives us a "next" argument to use to redirect
        #   after login.
        # - the "next" arg should be validated.
        return redirect(request.args.get('next', '/'))

    # a simple, unsafe, login form in the template
    return render_template('_fake-dash-okta-login.html')

@fake_okta_bp.route('/who')
@login_required
def who():
    """
    Show who user is and logout link.
    """
    return render_template('_dash-okta-who.html')

@fake_okta_bp.route('/fake-logout')
@login_required
def logout():
    """
    Logout user.
    """
    logout_user()
    # Dash names endpoints like paths.
    return redirect(url_for('/'))
