import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
def datetotimestamp(date):
    time_tuple=date.timetuple()
    timestamp=round(time.mktime(time_tuple))
    return timestamp
def timestamptodate(timestamp):
    return datetime.fromtimestamp(timestamp)
start=datetotimestamp(datetime(2023,1,1))
end=datetotimestamp(datetime.today())
url='https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=INFY&resolution=1D&from='+str(start)+'&to='+str(end)+'&countback=365&currencyCode=INR'
# url='https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol=INFY&resolution=1D&from='+str(start)+'&to='+str(end)+'&countback=323&currencyCode=INR'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36'
}

resp = requests.get(url, headers=headers).json()
data=pd.DataFrame(resp)

date =[]
for dt in data['t']:
    date.append({'Date':timestamptodate(dt).date()})
date=pd.DataFrame(date)

final_data=pd.concat([date,data['o'],data['h'],data['l'],data['c'],data['v']],axis=1).rename(columns={'o':'Open','h':'High','l':'Low','c':'Close','v':'Volume'})
print(final_data)





print(final_data[356:366])

