from marshmallow import fields, Schema
import datetime
from . import db
from . import bcrypt

class SubscriberModel(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.email = data.get('email')
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_subscribers():
        return SubscriberModel.query.all()

    def __repr(self):
        return '<id {}>'.format(self.id)
class SubscriberSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)

  email = fields.Email(required=True)
