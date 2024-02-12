from . import db
import datetime
from marshmallow import fields, Schema
from sqlalchemy.orm import relationship
class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, data):
        self.title = data.get('name')
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return '<id {}>'.format(self.id)
class CategorySchema(Schema):
    """
    Category Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

