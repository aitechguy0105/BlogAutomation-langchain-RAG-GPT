# /src/views/BlogpostView.py
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.GoldPriceModel import GoldPriceModel, GoldPriceSchema
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import timedelta
goldprice_api = Blueprint('goldprice_api', __name__)
goldprice_schema = GoldPriceSchema()



@goldprice_api.route('/', methods=['GET'])
def get_current_gold_price():
    """
    Create Blogpost Function
    """
    price = GoldPriceModel.get_current_price()
    data = goldprice_schema.dump(price)
    print('first invoked')
    return custom_response(data, 200)
@goldprice_api.route('/chart/<int:days>', methods=['GET'])
def get_gold_prices_for_chart(days):
    """
    Create Blogpost Function
    """
    datetime_cur = datetime.utcnow()
    date_cur = datetime_cur.date()
    date_delta = timedelta(days = days)
    date_start = date_cur - date_delta
    date_delta = timedelta(days = 0)
    date_end = date_cur - date_delta
    gold_price_api_key = '7gRDFMlHumWeRX7R0ImtHwdkKDhvGRL1'
    
    limit = 5000
    url = f"https://api.polygon.io/v2/aggs/ticker/C:XAUUSD/range/1/day/{date_start}/{date_end}?adjusted=true&sort=asc&limit={limit}&apiKey={gold_price_api_key}"
    
    response = requests.get(url)
    
    data = response.json()
    lt_result = []
    highest_price = 0
    lowest_price = 9999999999999
    for item in data['results']:

        date_obj = datetime.fromtimestamp(item['t']/1000)
        day_of_week = date_obj.strftime("%A")
        date_str = date_obj.strftime("%Y-%m-%d")
        # print(date_str, day_of_week,  item['o'], item['h'], item['l'])
        if highest_price < item['h']:
            highest_price = item['h']
        if lowest_price > item['l']:
            lowest_price = item['l']
        item_result = {'date': date_str, 'open_price': item['o'], 'high_price': item['h'], 'low_price': item['l']}
        lt_result.append(item_result)

    result = {'highest_price': highest_price, 'lowest_price': lowest_price, 'prices': lt_result}
    # print(result)
    return custom_response(result, 200)
def save_gold_price(data):
    """
    Create Blogpost Function
    """
    data = goldprice_schema.load(data)
    price = GoldPriceModel(data)
    price.save()
    

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

