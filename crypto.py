import requests, json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

# only for sale 5$ per transction #
resp = requests.get('https://api.wazirx.com/api/v2/tickers')
txt = resp.json()
df1 = pd.DataFrame(txt)
df1 = df1.loc[['name','last']].swapaxes("index", "columns").reset_index(drop=True)
df1 = df1.loc[df1['name'].str.contains("/INR", case=True)]
df1 = df1.astype({"name": str, "last": float})
df1['name'] = df1.name.replace({'/INR':''}, regex=True)
#print(df1)



def exchange_rate():
  main_url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=INR&apikey=B83ZTLV6AKT8L7GS"
  req_ob = requests.get(main_url)
  result = req_ob.json()
  text1 = json.dumps(result, sort_keys=True, indent=4)
  exchange_dict = json.loads(text1)
  #print(exchange_dict.keys())
  exchangevalue=exchange_dict["Realtime Currency Exchange Rate"]['5. Exchange Rate']
  return float(exchangevalue)


binance_url = "https://api.binance.com/api/v3/ticker/price"
r= requests.get(binance_url)
r=r.json()
df2 = pd.json_normalize(r)
df2 = df2.loc[df2['symbol'].str.contains("USDT", case=True)]
df2 = df2.astype({"symbol": str, "price": float})
df2['price'] = df2['price'] * exchange_rate()
df2['symbol'] = df2.symbol.replace({'USDT':''}, regex=True)
df2 = df2.rename(columns={"symbol" : "name"})
df2 = df2.rename(columns={'price':'last'})
df2=df2.reset_index(drop=True)
#print(df2)


#---------------------comparing------------------------------------------------------------------------------#

#df1['pricesMatch?'] = np.where(str(df1['last']) > str(df2['last']), 'True', 'False')
#print(df1)
#------------------------------------------------------------------------------------------------------------#
a=len(df1)
b=len(df2)
for x in range(a):
  for y in range(b):
    if df1['name'][x] == df2['name'][y]:
      diff = df1['last'][x] - df2['last'][y]
      per = (diff*100) / df2['last'][y]
      print(str(df1['name'][x]) + "            " + str(df1['last'][x]) +"         " +str(df2['last'][y]) + "          "+str(diff)+"            "+ str(per))
      

