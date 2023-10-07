from flask import Flask

from .extensions import db
from .views import database_bp
from .views import interact_bp
from .views import main_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_envvar('DRAGDROP_CONFIG')

    db.init_app(app)

    app.register_blueprint(database_bp)
    app.register_blueprint(interact_bp)
    app.register_blueprint(main_bp)

    return app
