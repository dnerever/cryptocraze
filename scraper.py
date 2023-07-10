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
    print('* Data Scraped')
    try:
        with open('output.json', 'w', encoding='utf-8') as output:
            json.dump(jsonData, output, ensure_ascii=False, indent=4)
        print('* data saved to output.json')
    except:
        print("**Failed to save to File**")
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

try:
    df = pandas.DataFrame.from_dict(pandas.json_normalize(jsonData), orient='columns')
    df.to_csv('output.csv', encoding='utf-8', index=False)
    df.to_json('pandasOutput.json')
    print('* Data saved to pandas')
except:
    print('**Failed to load to pandas**')

try:
    df.to_html('test.html')
    # dataID = pandas.read_clipboard(
    #     sep=",",
    #     header="infer",
    #     index_col=0,
    #     names=["Order", "ID", "Category", "Sales", "Quantity", "Discount"],
    # )
    # pandas.set_option("display.max_rows", None, "display.max_columns", None)
    # print(dataID)
    df['data'].to_json('dataOnly.json')
    df['data'].to_csv('dataOnly.csv')
    # dataID.to_csv('clipboardData.csv')
    # print('* Data: ')
except:
    print('**Failed to print panda data**')

if df['status.error_message'].isna().all():
    print('* Scrape success')
else:
    print('** Error scraping **')
    print(df['status.error_message'])