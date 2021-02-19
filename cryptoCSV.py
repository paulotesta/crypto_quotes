import requests
import json
import csv
import datetime
import time
# import sqlite3

CONFIG_FILENAME = 'config.json'
QUOTES_FILENAME = 'quotes.csv'
TIME_FORMAT = "%y/%m/%d %H:%M"
INTERVAL = 3600

assets = None
api_key = None
currency_key = None
currency = None


def main():
    assets = get_config()
    while True:
        get_quote(assets)
        timer()


def get_config():
    with open(CONFIG_FILENAME) as config_file:
        data = json.load(config_file)

    global assets = data['currencies']
    global api_key = data['api_key']
    global currency_key = data['currency_key']
    global currency = data['currency']


def get_quote(assets):
    names_list = []
    quotes_list = []
    for asset_id in assets:
        crypto_url = "https://rest.coinapi.io/v1/assets/{}/?apikey={}".\
                    format(asset_id, API_KEY)

        response = requests.get(crypto_url)
        response = response.json()
        names_list.append(response[0]['asset_id'])
        quotes_list.append(response[0]['price_usd'])

    quotes_list = convert_ponds(quotes_list)

    names_list = remove_brakets(names_list)
    quotes_list = remove_brakets(quotes_list)

    append_csv(quotes_list, names_list)
    # append_sql(quotes_list, names_list)


def append_csv(quotes, names):
    try:
        with open(QUOTES_FILENAME, 'a') as csv_file:
            quotes_writer = csv.writer(csv_file, delimiter=',', quotechar=' ',
                                       quoting=csv.QUOTE_MINIMAL)
            now = datetime.datetime.now()
            quotes_writer.writerow([now.strftime(TIME_FORMAT), quotes])
    except IOError:
        with open(QUOTES_FILENAME, 'x') as csv_file:
            quotes_writer = csv.writer(csv_file, delimiter=',', quotechar=' ',
                                       quoting=csv.QUOTE_MINIMAL)
            quotes_writer.writerow(["Time", names])

# def append_sql(quotes, names):


def timer():
    time.sleep(INTERVAL)
    return


def convert_ponds(quotes_list):
    currency_url = "http://data.fixer.io/api/latest?access_key={}&format=1"\
                    format(currency_key)
    response = requests.get(currency_url)
    response = response.json()
    conversion_rate = response['rates'][currency] / response['rates']['USD']

    for i in range(4):
        quotes_list[i] = quotes_list[i] * conversion_rate

    return quotes_list


def remove_brakets(info):
    x = str(info)
    x = x.replace('[', '')
    x = x.replace(']', '')
    return x


main()