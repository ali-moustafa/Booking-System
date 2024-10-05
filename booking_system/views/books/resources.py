"""Books resources"""

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from booking_system.extensions.api import Blueprint, SQLCursorPage
from booking_system.extensions.database import db
from booking_system.models import Book
from booking_system.models.schema import BookSchema, BookQueryArgsSchema

blp = Blueprint(
    'Books',
    __name__,
    url_prefix='/books',
    description="Book Manager"
)


@blp.route('/list', methods=['GET'])
@blp.route('/new', methods=['POST'])
class Books(MethodView):

    @blp.arguments(BookQueryArgsSchema, location='query')
    @blp.response(status_code=200, schema=BookSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        return Book.query.filter_by(**args)

    @blp.arguments(BookSchema)
    @blp.response(status_code=201, schema=BookSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def post(self, new_item):
        item = Book(**new_item)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=e.__class__.__name__, errors="author_id {} not found".format(item.author_id))
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(400, message=e.__class__.__name__, errors=message)

        return item


@blp.route('get/<uuid:item_id>', methods=['GET'])
@blp.route('edit/<uuid:item_id>', methods=['PUT'])
@blp.route('delete/<uuid:item_id>', methods=['DELETE'])
class BooksById(MethodView):

    @blp.response(status_code=200, schema=BookSchema)
    def get(self, item_id):
        return Book.query.get_or_404(item_id)

    @blp.arguments(BookSchema)
    @blp.response(status_code=200, schema=BookSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def put(self, new_item, item_id):
        item = Book.query.get_or_404(item_id)
        try:
            BookSchema().update(item, new_item)
            db.session.add(item)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=e.__class__.__name__, errors="author_id {} not found".format(new_item['author_id']))
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(400, message=e.__class__.__name__, errors=message)

        return item

    @blp.response(status_code=204)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def delete(self, item_id):
        item = Book.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
