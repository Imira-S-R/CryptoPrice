import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import json


app = Flask(__name__)


def get_price(name):
    index = -1
    URL = f'https://bitflyer.com/en-us/{name}-chart'
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    text = soup.find('div', attrs={"class":"p-currencyInfo__price c-text--number"}).text
    text2 = soup.find('div', attrs={'id':"rate"}).text
    text3 = soup.find_all('li', attrs={'class':'c-breadcrumb__item'})
    for value in text3[1].text.split():
        index += 1
        if 'USD' in value:
            symbol = text3[1].text.split()[index].split('/')[0].lstrip('(')
    data = {'name': name, 'symbol': symbol, 'price': text.strip().split('*')[0], '%Change':text2.strip().split('\n')[0]}
    return data

@app.route('/', methods=["GET"])
def hello_world():
    return "Hello World"

@app.route('/all')
def get_list():
    data = {'1': 'ethereum', '2':'tezos', '3':'litecoin', '4':'polkadot', '5':'ethereum-classic', '6':'bitcoin-cash'}
    return json.dumps(data)

@app.route('/price')
def query_example():
    name = request.args.get('name')
    data = get_price(name)
    return json.dumps(data)
