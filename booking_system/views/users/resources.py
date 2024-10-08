from flask.views import MethodView
from flask_jwt_extended import jwt_required

from booking_system.extensions.api import Blueprint, SQLCursorPage
from booking_system.extensions.database import db
from booking_system.models import User
from booking_system.models.schema import UserSchema, UserQueryArgsSchema

blp = Blueprint(
    'Users',
    __name__,
    url_prefix='/users',
    description="User Manager"
)


@blp.route('/list', methods=['GET'])
@blp.route('/signUp', methods=['POST'])
class Users(MethodView):

    @blp.arguments(UserQueryArgsSchema, location='query')
    @blp.response(status_code=200, schema=UserSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        return User.query.filter_by(**args)

    @blp.arguments(UserSchema, example=dict(first_name="ali", last_name="Mostafa", email="ali@gmail.com"))
    @blp.response(status_code=201, schema=UserSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    def post(self, new_item):
        item = User(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route('/<string:user_email>')
class UsersByEmail(MethodView):

    @blp.response(status_code=200, schema=UserSchema)
    def get(self, user_email):
        return User.query.get_or_404(user_email)

    @blp.arguments(UserSchema)
    @blp.response(status_code=201, schema=UserSchema)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def put(self, new_item, user_email):
        item = User.query.get_or_404(user_email)
        UserSchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item

    @blp.response(status_code=204)
    @blp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def delete(self, user_email):
        item = User.query.get_or_404(user_email)
        db.session.delete(item)
        db.session.commit()
