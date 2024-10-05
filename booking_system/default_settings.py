import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig:
    """Default configuration"""
    API_VERSION = 0.1
    API_TITLE = 'Booking System'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'

    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_ECHO = True

    JWT_TOKEN_LOCATION = 'headers'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_SECRET_KEY = 'super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_ERROR_MESSAGE_KEY = 'message'

    SECRET_KEY = secrets.token_urlsafe(16)
    WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(16)
    WTF_CSRF_CHECK_DEFAULT = False
