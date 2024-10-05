from flask_smorest import Api as ApiOrig, Blueprint as BlueprintOrig, Page


class Blueprint(BlueprintOrig):
    """Blueprint override"""


class Api(ApiOrig):
    def __init__(self, app=None, *, spec_kwargs=None):
        spec_kwargs = spec_kwargs or {}
        super().__init__(app, spec_kwargs=spec_kwargs)
        self.spec.components.security_scheme("bearerAuth", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"})


class SQLCursorPage(Page):
    @property
    def item_count(self):
        return self.collection.count()
