from marshmallow import fields, Schema
import datetime
from . import db

class GoldPriceModel(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = 'goldprices'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime)


    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.price = data.get('price')
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_prices():
        return GoldPriceModel.query.all()

    @staticmethod
    def get_one_price(id):
        return GoldPriceModel.query.get(id)
    @staticmethod
    def get_current_price():
        price = GoldPriceModel.query.order_by(GoldPriceModel.created_at.desc()).first()
        return price

    def __repr(self):
        return '<id {}>'.format(self.id)
class GoldPriceSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  price = fields.Float(required=True)

  created_at = fields.DateTime(dump_only=True)
