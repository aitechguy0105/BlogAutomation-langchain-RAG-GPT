import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.app import create_app, db
from src.models.BlogpostModel import *
from src.models.UserModel import *
from src.models.CategoryModel import *

from ecrivai.add_blog import ArticleWriter

env_name = os.getenv('FLASK_ENV')
db_url = os.getenv('DATABASE_URL')
print("manage", db_url, env_name)
article_writer  =  ArticleWriter()
app = create_app(env_name, article_writer)

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()