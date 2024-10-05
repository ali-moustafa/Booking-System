from . import database, JWT
from .api import Api


def create_api(app):
    new_api = Api(app)

    for extension in (
            database,
            JWT
    ):
        extension.init_app(app)

    return new_api
