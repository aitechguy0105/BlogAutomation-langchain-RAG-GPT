# /src/views/BlogpostView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.SubscriberModel import SubscriberModel, SubscriberSchema
from bs4 import BeautifulSoup
subscriber_api = Blueprint('subscriber_api', __name__)
subscriber_schema = SubscriberSchema()



def get_subscribers():
    """
    Create Blogpost Function
    """
    subscribers = SubscriberModel.get_all_subscribers()
 
    data = subscriber_schema.dump(subscribers, many=True)
  
    return data
    # return custom_response(data, 200)
@subscriber_api.route('/subscribe_email/<string:email>', methods=['POST'])
def subscribe_email(email):
    try:
        print('function invoked')
        req_data = {'email': email}
        subscriber = subscriber_schema.load(req_data)
        print(subscriber)
        if 'error' in subscriber:
            return custom_response(subscriber, 400)
        # Check if the email address already exists
        existing_subscriber = SubscriberModel.query.filter_by(email=email).first()
        print(existing_subscriber)
        if existing_subscriber is not None:
            return custom_response({'error': 'Email address already exists'}, 400)
        subscriber = SubscriberModel(subscriber)
        print("----------")
        subscriber.save()
        print("saved")
        data = subscriber_schema.dump(subscriber)
        return custom_response(data, 200)
    except Exception as e:
        print(e)
        return custom_response(e, 400)
    # finally:
    #     error = {'error': 'unknown'}
    #     return custom_response(error, 400)
def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )