from flask import Flask
import os
from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint # add this line
from .views.CategoryView import category_api as category_blueprint
from .views.BlogpostView import blogpost_api as blogpost_blueprint
from .views.GoldPriceView import goldprice_api as goldprice_blueprint
from .views.SubscriberView import subscriber_api as subscriber_blueprint
from .views.BlogpostView import save_daily_article, get_one_article_by_new
from .views.GoldPriceView import save_gold_price
from .views.SubscriberView import get_subscribers
from apscheduler.schedulers.background import BackgroundScheduler
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
from requests import HTTPError
import random
import requests
from datetime import datetime
import json
import time
from bs4 import BeautifulSoup
from flask import send_from_directory

scheduler = BackgroundScheduler()
def create_app(env_name, article_writer):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__, static_folder="static/dist", template_folder="static/dist")
    print('app.py', os.getenv('DATABASE_URL'))
    a = app_config[env_name]
    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)  # add this line
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')  # add this line
    app.register_blueprint(blogpost_blueprint, url_prefix='/api/v1/blogposts')
    app.register_blueprint(category_blueprint, url_prefix='/api/v1/categories')
    app.register_blueprint(subscriber_blueprint, url_prefix='/api/v1/subscribers')
    app.register_blueprint(goldprice_blueprint, url_prefix='/api/v1/goldprices')
    @app.route('/api/v1/get_server_time', methods=['GET'])
    def send_server_time():
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return current_time
    @app.route('/api/v1/contact_us/<string:user>/<string:email>/<string:content>', methods=['POST'])
    def contact_us(user, email, content):
        with app.app_context():
            SCOPES = [
                    "https://www.googleapis.com/auth/gmail.send"
                ]
            creds = gmail_credentials()
            
            service = build('gmail', 'v1', credentials=creds)
            
            
            message = MIMEMultipart("related")
            content = content + '<br>' + 'from  ' + user + '<br>' + email 
            msg = MIMEText(content, "html")
            message.attach(msg)
            
            message['to'] = 'vegaventures@gmail.com'
            message['subject'] = 'ContactUs'
        
            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        
            try:
                message = (service.users().messages().send(userId="me", body=create_message).execute())
                print(F'sent message to {message} Message Id: {message["id"]}')
            except HTTPError as error:
                print(F'An error occurred: {error}')
                message = None
                
        return 'ok'
    @app.route('/')
    def send_report():
        print (app.static_folder)
        return send_from_directory(app.static_folder, "index.html")
        # return send_from_directory(app.static_folder, path)
        # # return path
    
    @app.route("/assets/<path:path>")
    def send_assets(path):
        return send_from_directory(app.static_folder + "/assets/", path)

    @app.route("/images/<path:path>")
    def send_images(path):
        return send_from_directory(app.static_folder + "/images/", path)
    
    @app.route("/icons/<path:path>")
    def send_icons(path):
        return send_from_directory(app.static_folder + "/icons/", path)
        
    @app.route("/opacitybackground/<path:path>")
    def send_opacitybackgrounds(path):
        return send_from_directory(app.static_folder + "/opacitybackground/", path)
    @app.route('/<path:path>')
    def send_article(path):
        print (app.static_folder)
        return send_from_directory(app.static_folder, "index.html")
    
    categories = ["Gold Mining",
"Gold Investment",
"The art of goldwork",
"Types of gold in jewelry",
"Gold rush",
"Formation of gold deposits",
"Gold standard",
"Different forms of gold",
"Gold jewellery demand and trends",
"Gold in history",
"Gold investment and portfolio management", 
"Gold as a hedge against inflation",
"Gold bars and coins pricing and purchasing",
"Gold purity and quality standards",
"Gold mining and production",
"Gold trading and market analysis",
"Gold ETFs and mutual funds",
"Gold futures and options trading",
"Gold reserves and central bank holdings",
"Investing in Gold Jewelry"]

    def create_daily_articles():
        with app.app_context():
            try:
                random_number = random.randint(0, 19)
                title, summary, article, img_url = article_writer.create_article_openai(categories[random_number])
                if title == None or article == None or article == 'None':
                    print('none error occured')   
                    raise Exception('Failed to create article')  # Raise an exception to trigger a retry
     
                rating = random.randint(0, 10)
                data = {"owner_id": 1, "title": title, "contents": article, "category_id": random_number + 1, "rating":rating}
                save_daily_article(data)
                print("article created and saved")
            except Exception as e:
                print(f"Error: {e}. Retrying in 60 seconds...")
                time.sleep(60)  # Wait for 60 seconds before retrying
                create_daily_articles()  # Call the function recursively after the retry interval
    # def create_daily_articles():
    #     with app.app_context():
          
    #         random_number = random.randint(0, 9)
    #         title, summary, article, img_url = article_writer.create_article_openai(categories[random_number])
    #         if title == None or article == None or article == 'None':
                
    #             print('None Error')
    #             return 
 
            
    #         data = {"owner_id": 1, "title": title, "contents": article, "category_id": random_number + 1, "rating":0}
    #         save_daily_article(data)
    #         print("article created and saved")


    def save_gold_price_per_day():
        with app.app_context():
            api_key = "goldapi-c3a3rlrjb6990-io"
            symbol = "XAU"
            curr = "USD"
            date = ""

            url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"
            
            headers = {
                "x-access-token": api_key,
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                result = response.json()
                print(result['price'])
                
                save_gold_price({'price': result['price']})
                print('gold price successfully saved')
            except requests.exceptions.RequestException as e:
                print("Error:", str(e))
    def gmail_credentials():
    # Set up OAuth2 credentials
        try:
            creds = Credentials.from_authorized_user_file('token.json')
        except FileNotFoundError: #-- token.json file does NOT exist --#
            #-- generate token by authorizing via browser (1st time only, I hope so :D) --#
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_ronan.json',  #credentials JSON file
                ['https://www.googleapis.com/auth/gmail.send']
                )
            creds = flow.run_local_server(port=0)
        
        #-- token.json exists --#    
        if creds and creds.valid:
            pass
        
        #-- token is expired--#      
        elif creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        # Save the credentials as token
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
        
        # return the creds
        
        return creds
    def send_daily_article():
        with app.app_context():
            SCOPES = [
                    "https://www.googleapis.com/auth/gmail.send"
                ]
            creds = gmail_credentials()
            
            service = build('gmail', 'v1', credentials=creds)
            subscribers = get_subscribers()
            print (subscribers)
            data = get_one_article_by_new()
            title = '<h1>' + data['title'] + '</h1>'
            data_for_send = data['contents']
            soup = BeautifulSoup(data_for_send,'html.parser')
            image_element = soup.find('img')
            image_name = image_element['src'][8:]
            print("image_name: ",image_name)
            image_element['src'] = "cid:image.jpg"
            data_for_send = str(soup)
            image_path = 'src/static/dist/images/' + image_name
  
            
            soup = BeautifulSoup(data_for_send,'html.parser')
            print("data_for_send:", soup.find('img'))
            for subscriber in subscribers:
                print(subscriber['email'])
                message = MIMEMultipart("related")
                
                msg = MIMEText(data_for_send, "html")
                message.attach(msg)
                with open(image_path, 'rb') as f:
                    # img_data = f.read()
                    image_part = MIMEImage(f.read(), _subtype = 'jpg')
                    # image_part.add_header('Content-ID', "<"+image_name+">")
                    image_part.add_header('Content-ID', '<image.jpg>')
                    message.attach(image_part)
                    
                # Attach the image part to the message
                message['from'] = 'goldexcg.com <ronanlee0105@gmail.com>'
                message['to'] = subscriber['email']
                message['subject'] = 'New Article From GOLDEXCG'
            
                create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            
                try:
                    message = (service.users().messages().send(userId="me", body=create_message).execute())
                    print(F'sent message to {message} Message Id: {message["id"]}')
                except HTTPError as error:
                    print(F'An error occurred: {error}')
                    message = None
            
    def stop_scheduler():
        scheduler.shutdown()
        return 'Scheduler stopped successfully!'
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your first endpoint is workin'



    @app.before_first_request
    def setup():
    
        
        # scheduler.add_job(create_daily_articles, 'cron', hour=9)
        scheduler.add_job(func=create_daily_articles, trigger="interval", hours = 12)
        # scheduler.add_job(func=create_daily_articles, trigger="interval", minutes = 10)
        scheduler.add_job(func=save_gold_price_per_day, trigger="interval", hours=12)
    
        # send_daily_article()
        # save_gold_price_per_day()
        scheduler.add_job(send_daily_article, 'cron', hour = 12)

        # for i in range(30):
            
        #     create_daily_articles()

        # Start the scheduler
        scheduler.start()
    return app