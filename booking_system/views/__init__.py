from . import books
from . import authors
from . import users
from . import auth


MODULES = (
    auth,
    authors,
    books,
    users
)


def register_blueprints(api):
    for module in MODULES:
        api.register_blueprint(module.blp)
