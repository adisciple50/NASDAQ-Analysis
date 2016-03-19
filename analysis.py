from yahoo_finance import Share
import time
import functions
from datetime import date

symbol = "AMD"
now = time.strftime("%Y-%m-%d")

tradingdays =  (days // 7)*2 + days % 7

print("Todays Date: ",now)

amd = functions.get_google_data(symbol,)


current_stock = amd.get_historical("2016-01-01",now)
test = amd.get_trade_datetime()

print(current_stock)
print(test)