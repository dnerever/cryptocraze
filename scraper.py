#Notes: May need to switch output to a csv for Snowflake import

import config   #import API Key
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas

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
    jsonData = json.loads(response.text)
    print('Data Scraped')
    try:
        with open('output.json', 'w', encoding='utf-8') as output:
            json.dump(jsonData, output, ensure_ascii=False, indent=4)
        print('JSON data saved to output.json')
    except:
        print("**Failed to save to File**")
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

try:
    df = pandas.DataFrame.from_dict(pandas.json_normalize(jsonData), orient='columns')
    df.to_csv('output.csv', encoding='utf-8', index=False)
    df.to_json('pandasOutput.json')
    print('Data saved to pandas')
except:
    print('**Failed to load to pandas**')