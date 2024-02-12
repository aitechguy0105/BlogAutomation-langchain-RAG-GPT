import os
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
print(os.getenv('OPENAI_API_KEY'))
from src.app import create_app
from article_ai.article_writer import ArticleWriter


if __name__ == '__main__':
  article_writer = ArticleWriter()
  env_name = os.getenv('FLASK_ENV')
  app = create_app(env_name, article_writer)
  CORS(app)
  # run app
  app.run(host='0.0.0.0', port=5000)