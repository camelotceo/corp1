import time
import requests
import datetime
import pandas as pd
import json
from telegram import Bot

# Set your Telegram bot token
TELEGRAM_BOT_TOKEN = '5806115909:AAFLqqi4un2ltqMYopUqS1_uaHzqBfxVqUg'
# Set the chat ID of 'cryptoblack fam chat' group
TELEGRAM_CHAT_ID = '6941630183'
TELEGRAM_CBFAM_CHAT_ID = '-1002100379153'
# def send_telegram_message1(message):
#     bot = Bot(token=TELEGRAM_BOT_TOKEN)
#     bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def send_telegram_message(message):
    telegram_token = TELEGRAM_BOT_TOKEN
    telegram_chat_id = TELEGRAM_CBFAM_CHAT_ID
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    params = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to send telegram message: {response.text}")

def price(symbol, comparison_symbols=['USD'], exchange='Coinbase'):
    url = 'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'\
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    response = requests.get(url) #{'USD': 42609.22}
    data = response.json()
    price = data['USD']
    return price

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    price = data['bitcoin']['usd']
    return price

previous_price = price('btc')

while True:
    # Extract the current Bitcoin price in USD
    
    #Coinbase
    # response = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD')
    # data = json.loads(response.text)
    # current_price = float(data['data']['amount'])
    # print(f"CoinBase Price: ${current_price}")

    current_price = price('btc')
    price_difference = (current_price - previous_price) 
    percent_difference = ((current_price - previous_price) / previous_price) * 100
    
    num_minutes = 3
    num_seconds = 60*num_minutes
    plus_minus = "+"
    short_long = "LONG"
    fell_rose = "RISEN"

    if price_difference < 0:
        plus_minus = "-"
        short_long = "SHORT"
        fell_rose = "FALLEN"


    message = f"LOG: BTC Price: {current_price:.2f} | ${price_difference:.2f} | {percent_difference:.2f}%"
    print(message)

    if percent_difference > 0.25 or percent_difference < -0.25:
        message = f"ALERT from Legion. BTC on the move! Possible {short_long} Opportunity. BTC has {fell_rose} {percent_difference:.2f}% in the last {num_minutes} minutes by ${price_difference:.2f} From ${previous_price:.2f} TO {current_price:.2f} "
        print(message)
        send_telegram_message(message)
    previous_price = current_price
    time.sleep(num_seconds)  # Sleep for 1 minute before checking again

