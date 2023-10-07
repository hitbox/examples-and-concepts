from flask_login import LoginManager
from flask_login import login_required

from .models import User
from .views import fake_okta_bp

def require_login_for_dash(
    app,
    flask_secret_key,
    login_manager = None,
    login_blueprint = None,
):
    """
    :param app:
        A Dash app instance.
    :param flask_secret_key:
        Secret key for Flask instance and extensions. This is not the Okta
        secret key.
    :param login_manager:
        Instance of Flask-Login's LoginManager or None and dash_okta will
        provide its own.
    :param login_blueprint:
        Blueprint to register for responding to login requests. By default this
        is an unsecure fake login that takes whatever username is given.
    """
    # NOTE
    # - Wrap all Dash's view functions with login_required.
    # - This is how we redirect for login for unauthenticated users.
    # - Dash has hooked up all endpoint functions after initialization.
    # - It's callback functionality is maintained in a separate map and list,
    #   testing and code browsing confirms.
    flask_instance = app.server
    view_functions = flask_instance.view_functions
    for endpoint in list(view_functions):
        func = view_functions[endpoint]
        view_functions[endpoint] = login_required(func)

    if login_manager is None:
        flask_instance.logger.warn('Using fake Okta login.')

        # hook up our own login_manager to a fake login page.
        # setup flask-login extension
        login_manager = LoginManager(flask_instance)

        @login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)

        # this should become a redirect to okta instead of our fake login:
        login_manager.login_view = 'fake_okta.login'

    # flask requires registering is done after all routes
    app.server.register_blueprint(fake_okta_bp)

    if flask_instance.secret_key is None:
        flask_instance.secret_key = flask_secret_key

