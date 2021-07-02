from pandas._libs.tslibs.timestamps import Timestamp
import config
import csv
import pandas as pd
from binance.client import Client
from binance.enums import *
import numpy as np
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import datetime

client = Client(config.API_KEY, config.API_SECRET)

closes = []
opens = []
lows = []
highs = []
levels = []
dates = []

candles = client.get_klines(symbol='ADAUSDT', interval=Client.KLINE_INTERVAL_1DAY, limit=100)
# print(json.dumps(candles, indent=2))

def saveCSV():
  csvfile = open('ada.csv', 'w', newline='')
  csvWriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
  for candle in candles:
    csvWriter.writerow(candle)

def isSupport(df,i):
  support = df[i] < df[i-1]  and df[i] < df[i+1] \
  and df[i+1] < df[i+2] and df[i-1] < df[i-2]
  return support

def isResistance(df,i):
  resistance = df[i] > df[i-1]  and df[i] > df[i+1] \
  and df[i+1] > df[i+2] and df[i-1] > df[i-2] 
  return resistance

def isFarFromLevel(l):
  np_highs = np.array(highs)
  np_lows = np.array(lows)
  s =  np.mean(np_highs - np_lows)
  return np.sum([abs(l-x[1]) < s  for x in levels]) == 0

for x in np.array(candles)[:]:
  closes.append(float(x[4]))
  highs.append(float(x[2]))
  lows.append(float(x[3]))
  opens.append(float(x[1]))
  t = int(int(x[0]) * 0.001)
  d = datetime.datetime.fromtimestamp(t)
  dates.append(d.date())


for i in range(2,len(closes)-2):
  if isSupport(lows,i):
    l = lows[i]
    if isFarFromLevel(l):
      levels.append((i,l))
  elif isResistance(highs,i):
    l = highs[i]
    if isFarFromLevel(l):
      levels.append((i,l))

quotes = [tuple([mpl_dates.date2num(dates[i]),
                 opens[i],
                 highs[i],
                 lows[i],
                 closes[i]]) for i in range(len(dates))] #_1

def plot_all():
  fig, ax = plt.subplots()
  candlestick_ohlc(ax,quotes,width=0.6, \
                   colorup='green', colordown='red', alpha=0.8)
  
  ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
  ax.grid(True)

  fig.autofmt_xdate()
  fig.tight_layout()
  for level in levels:
    plt.hlines(level[1],xmin=dates[level[0]],\
                xmax=max(dates),colors='blue')
  plt.show()


plot_all()

# print("levels") 
# print(levels)

