from flask.views import MethodView
from flask_jwt_extended import jwt_required

from booking_system.extensions.api import Blueprint, SQLCursorPage
from booking_system.extensions.database import db
from booking_system.models import Author, Book
from booking_system.models.schema import AuthorSchema, AuthorQueryArgsSchema

blp = Blueprint(
    'Authors',
    __name__,
    url_prefix='/authors',
    description="Author Manager"
)


@blp.route('/')
class Authors(MethodView):

    @blp.arguments(AuthorQueryArgsSchema, location='query')
    @blp.response(status_code=200, schema=AuthorSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        book_id = args.pop('book_id', None)
        ret = Author.query.filter_by(**args)
        if book_id is not None:
            ret = ret.join(Author.books).filter(Book.id == book_id)
        return ret

    @blp.arguments(AuthorSchema, example=dict(first_name="ali", last_name="Mostafa", birth_date="1999-01-01"))
    @blp.response(status_code=201, schema=AuthorSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def post(self, new_item):
        item = Author(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route('/<uuid:item_id>')
class AuthorsById(MethodView):

    @blp.response(status_code=200, schema=AuthorSchema)
    def get(self, item_id):
        return Author.query.get_or_404(item_id)

    @blp.arguments(AuthorSchema)
    @blp.response(status_code=201, schema=AuthorSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def put(self, new_item, item_id):
        item = Author.query.get_or_404(item_id)
        AuthorSchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item

    @blp.response(status_code=204)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def delete(self, item_id):
        item = Author.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
