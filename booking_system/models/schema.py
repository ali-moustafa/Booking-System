import marshmallow as mar
from marshmallow import EXCLUDE
from marshmallow.validate import Length
from marshmallow_sqlalchemy import field_for

from booking_system.extensions.database import ma
from booking_system.models import Book, Author


class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        ordered = True
        unknown = EXCLUDE

    id = field_for(Book, "id", dump_only=True)
    title = field_for(Book, "title", required=True)
    category = field_for(Book, "category", required=True)
    price = field_for(Book, "price", required=True)
    release_date = field_for(Book, "release_date", required=True)
    author_id = field_for(Book, "author_id", required=True)
    created_at = field_for(Book, "created_at", dump_only=True)
    updated_at = field_for(Book, "updated_at", dump_only=True)

    def update(self, obj, data):
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class BookQueryArgsSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE

    name = mar.fields.Str()
    title = mar.fields.Str()
    category = mar.fields.Str()
    price = mar.fields.Float()
    release_date = mar.fields.DateTime()
    author_id = mar.fields.UUID()


class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author
        ordered = True
        unknown = EXCLUDE
        dateformat = "%Y-%m-%d"

    id = field_for(Author, "id", dump_only=True)
    first_name = field_for(Author, "first_name", required=True)
    last_name = field_for(Author, "last_name", required=True)
    birth_date = field_for(Author, "birth_date", required=True)
    created_at = field_for(Author, "created_at", dump_only=True)
    updated_at = field_for(Author, "updated_at", dump_only=True)

    def update(self, obj, data):
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))


class AuthorQueryArgsSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    first_name = mar.fields.Str()
    last_name = mar.fields.Str()


class LoginQueryArgsSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    user_email = mar.fields.Str(required=True)
    password = mar.fields.Str(required=True, validate=Length(min=2, max=8))


class JWTSchema(mar.Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    access_token = mar.fields.Str()
    token_type = mar.fields.Str()
    expires = mar.fields.Str()
