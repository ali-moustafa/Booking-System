import uuid

import sqlalchemy_utils

from booking_system.extensions.database import db


class User(db.Model):
    __tablename__ = "users"

    # id = db.Column(sqlalchemy_utils.types.uuid.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(length=80), primary_key=True)
    first_name = db.Column(db.String(length=40), nullable=False)
    last_name = db.Column(db.String(length=40), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    __table_args__ = (
        db.PrimaryKeyConstraint('email'),
    )
