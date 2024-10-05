from . import books
from . import authors
from . import auth

MODULES = (
    auth,
    authors,
    books
)


def register_blueprints(api):
    for module in MODULES:
        api.register_blueprint(module.blp)
