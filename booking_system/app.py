from flask import Flask

from booking_system import extensions, views
from booking_system.default_settings import DefaultConfig


def create_app():
    """Create application"""
    app = Flask(__name__)

    app.config.from_object(DefaultConfig)
    # Override config with optional settings file
    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)

    api = extensions.create_api(app)
    views.register_blueprints(api)

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    create_app()
