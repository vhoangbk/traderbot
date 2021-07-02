import websocket, json
import config
from binance.client import Client
from binance.enums import *
import telegram
import numpy as np

SOCKET = "wss://stream.binance.com:9443/ws/adausdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ADAUSDT'
TRADE_QUANTITY = 10

CHAT_ID = "-553545116"
TOKEN = "1800779983:AAHNfSzhmigrvdmj2iXrU28d01ywOTngkOM"

closes = []
opens = []
lows = []
highs = []
levels = []

client = Client(config.API_KEY, config.API_SECRET)

def send_message(message):
    bot = telegram.Bot(TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text=message)

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def isSupport(df,i):
  support = df[i] < df[i-1]  and df[i] < df[i+1] \
  and df[i+1] < df[i+2] and df[i-1] < df[i-2]
  return support

def isResistance(df,i):
  resistance = df[i] > df[i-1]  and df[i] > df[i+1] \
  and df[i+1] > df[i+2] and df[i-1] > df[i-2] 
  return resistance


def isFarFromLevel(l):
   return np.sum([abs(l-x) < np.mean(highs - lows)  for x in levels]) == 0

def on_message(ws, message):
    global closes, opens, highs, lows, levels

    json_message = json.loads(message)

    candle = json_message['k']
    is_candle_closed = candle['x']

    if is_candle_closed:
        print("candle closed at {}".format(candle['c']))
        closes.append(float(candle['c']))
        opens.append(float(candle['o']))
        lows.append(float(candle['l']))
        highs.append(float(candle['h']))

        print("closes")
        print(closes)

        for i in range(2,len(closes)-2):
          if isSupport(lows,i):
            l = lows[i]
            # if isFarFromLevel(l):
            levels.append((i,l))
          elif isResistance(highs,i):
            l = highs[i]
            # if isFarFromLevel(l):
            levels.append((i,l))

        print("levels") 
        print(levels)

        

# send_message("Supply demand bot stared!")   
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()