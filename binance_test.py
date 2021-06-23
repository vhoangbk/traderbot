import config
import csv
from binance.client import Client
from binance.enums import *
import json, talib, numpy

client = Client(config.API_KEY, config.API_SECRET)

closes = []
opens = []
lows = []
highs = []
times = []

candles = client.get_klines(symbol='ADAUSDT', interval=Client.KLINE_INTERVAL_1DAY)
# print(json.dumps(candles, indent=2))

# csvfile = open('ada.csv', 'w', newline='')
# csvWriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
# for candle in candles:
#   csvWriter.writerow(candle)

for candle in candles:
  o = float(candle[1])
  h = float(candle[2])
  l = float(candle[3])
  c = float(candle[4])
  t = float(candle[0])
  times.append(t)
  closes.append(c)
  highs.append(h)
  opens.append(o)
  lows.append(l)

np_closes = numpy.array(closes)
np_opens = numpy.array(opens)
np_lows = numpy.array(lows)
np_highs = numpy.array(highs)

dark_cloud_cover = talib.CDL3INSIDE(np_opens, np_highs, np_lows, np_closes)

i = 0
for d in dark_cloud_cover:
  if d != 0:
    print("{} : {}".format(times[i],d))
  i += 1


# rsi = talib.RSI(np_closes, 5)

# arr = [1.2765, 1.2778, 1.276]# numpy.random.rand(100,1)
# print(closes)
# an = numpy.array(closes)
# rsi = talib.RSI(an, 14)
# print(rsi)