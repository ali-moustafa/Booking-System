import uuid
import sqlalchemy_utils
from sqlalchemy.orm import backref

from booking_system.extensions.database import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(sqlalchemy_utils.types.uuid.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(length=80), nullable=False)
    category = db.Column(db.String(length=40), nullable=False)
    price = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    author_id = db.Column(sqlalchemy_utils.types.uuid.UUIDType(binary=False),
                          db.ForeignKey("authors.id", ondelete='CASCADE'))
    author = db.relationship('Author', backref=backref('books', passive_deletes=True))
