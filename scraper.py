import config   #import API Key
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start':'1',
    'limit':'10',
    'convert':'USD'
}
headers = {
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY': config.CMCAPIKEY
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    rawData = json.loads(response.text)
    # rawStatus = json.loads(response)
    # print(rawData['status'])
    try:
        with open('output.json', 'w', encoding='utf-8') as output:
            json.dump(rawData, output, ensure_ascii=False, indent=4)
    except:
        print("\n\n\nFailed to save to File\n\n\n")
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)