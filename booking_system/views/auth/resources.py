from datetime import datetime

from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, decode_token

from booking_system.models import User
from booking_system.extensions.api import Blueprint
from booking_system.models.schema import LoginQueryArgsSchema, JWTSchema

blp = Blueprint(
    'Auth',
    __name__,
    url_prefix='/login',
    description="login using token JWT"
)


@blp.route('/')
class Auth(MethodView):

    @blp.arguments(LoginQueryArgsSchema, location='query')
    @blp.response(status_code=200, schema=JWTSchema)
    def post(self, args):
        user_email = args.get('user_email')
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': f'Email <{user_email}> not found!'}), 404

        access_token = create_access_token(identity=user.email)
        pure_decoded = decode_token(access_token)
        return jsonify(access_token=access_token,
                       token_type='Bearer',
                       expires=datetime.fromtimestamp(pure_decoded["exp"]).strftime('%Y-%m-%d %H:%M:%S')), 200
