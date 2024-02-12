from . import db
from datetime import datetime, timedelta

from marshmallow import fields, Schema
from sqlalchemy.orm import relationship
from sqlalchemy import and_
class BlogpostModel(db.Model):
    """
    Blogpost Model
    """

    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # add this new line
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    rating = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, data):
        self.title = data.get('title')
        self.contents = data.get('contents')
        self.owner_id = data.get('owner_id') # add this new line
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()
        self.category_id = data.get('category_id')
        self.rating = data.get('rating')
        

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_blogposts():
        return BlogpostModel.query.all()
    @staticmethod
    def get_all_blogposts_count():
        return BlogpostModel.query.count()
    @staticmethod
    def get_one_blogpost(id):
        return BlogpostModel.query.get(id)

    @staticmethod
    def get_most_popular_article():
        most_popular_article = BlogpostModel.query.order_by(BlogpostModel.rating.desc(), BlogpostModel.created_at.desc()).first()
      
        return most_popular_article
    
    @staticmethod
    def get_popular_articles_with_category(category_id):
        related_articles_with_category = BlogpostModel.query.filter_by(category_id=category_id).order_by(BlogpostModel.rating.desc()).limit(3).all()
        return related_articles_with_category
    
    @staticmethod
    def get_popular_articles_month():
        last_month = datetime.utcnow() - timedelta(days=30)
        popular_articles_month = BlogpostModel.query.filter(BlogpostModel.created_at >= last_month).order_by(BlogpostModel.rating.desc()).limit(4).all()
        # current_month = datetime.datetime.now().month
        # current_year = datetime.datetime.now().year
        # popular_articles_month = (BlogpostModel.query.filter(and_(db.extract('year', BlogpostModel.created_at) == current_year,db.extract('month', BlogpostModel.created_at) == current_month)).order_by(BlogpostModel.rating.desc()).limit(4).all())
        return popular_articles_month
    @staticmethod
    def get_articles_by_category(category_id, page_num, articles_per_page):
        articles = BlogpostModel.query.filter_by(category_id=category_id).order_by(BlogpostModel.created_at.desc()).paginate(page=page_num, per_page=articles_per_page)
        return articles
    @staticmethod
    def get_articles_by_new_search(page_num, articles_per_page, search_keywords):
        articles = BlogpostModel.query.filter(
            (BlogpostModel.title.ilike(f"%{search_keywords}%")) |
            (BlogpostModel.contents.ilike(f"%{search_keywords}%"))
        ).order_by(BlogpostModel.created_at.desc()).paginate(page=page_num, per_page=articles_per_page)
        return articles
    
    @staticmethod
    def get_one_article_by_new():
        article = BlogpostModel.query.order_by(BlogpostModel.created_at.desc()).first()
        return article
    @staticmethod
    def get_articles_by_new(page_num, articles_per_page):
        articles = BlogpostModel.query.order_by(BlogpostModel.created_at.desc()).paginate(page=page_num, per_page=articles_per_page)
        return articles
    @staticmethod
    def get_articles_by_popular_search(page_num, articles_per_page, search_keywords):
        articles = BlogpostModel.query.filter(
            (BlogpostModel.title.ilike(f"%{search_keywords}%")) |
            (BlogpostModel.contents.ilike(f"%{search_keywords}%"))
        ).order_by(BlogpostModel.rating.desc()).paginate(page=page_num, per_page=articles_per_page)
        return articles
    @staticmethod
    def get_articles_by_popular(page_num, articles_per_page):
        articles = BlogpostModel.query.order_by(BlogpostModel.rating.desc()).paginate(page=page_num, per_page=articles_per_page)
        return articles
    @staticmethod
    def get_search_result(search_keywords):
        articles = BlogpostModel.query.filter(
            (BlogpostModel.title.ilike(f"%{search_keywords}%")) |
            (BlogpostModel.contents.ilike(f"%{search_keywords}%"))
        ).paginate(page=1, per_page=10)
        return articles
    def __repr__(self):
        return '<id {}>'.format(self.id)
class BlogpostSchema(Schema):
  """
  Blogpost Schema
  """
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  
  contents = fields.Str(required=True)
  owner_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  category_id = fields.Int(required=True)
  rating = fields.Int()
