import websocket, json, talib, numpy
import config
from binance.client import Client
from binance.enums import *
import telegram

SOCKET = "wss://stream.binance.com:9443/ws/adausdt@kline_30m"

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

client = Client(config.API_KEY, config.API_SECRET)

def send_message(message):
    bot = telegram.Bot(TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text=message)

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, opens, lows, highs
    json_message = json.loads(message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']
    open = candle['o']
    low = candle['l']
    high = candle['h']

    if is_candle_closed:
        closes.append(float(close))
        opens.append(float(open))
        lows.append(float(low))
        highs.append(float(high))
        print("closes")
        print(closes)

        np_closes = numpy.array(closes)
        np_opens = numpy.array(opens)
        np_lows = numpy.array(lows)
        np_highs = numpy.array(highs)

        morning_star = talib.CDLMORNINGSTAR(np_opens, np_highs, np_lows, np_closes)

        print("morning_star")
        print(morning_star)
        last_morning_star = morning_star[-1]
        print("last morning star: {}".format(last_morning_star))
        if last_morning_star != 0:
            send_message("Morning star Buy! Buy! Buy! {}".format(close))

        dark_cloud_cover = talib.CDLDARKCLOUDCOVER(np_opens, np_highs, np_lows, np_closes)
        print("dark cloud cover")
        print(dark_cloud_cover)
        last_dcc = dark_cloud_cover[-1]
        print("last dark cloud cover: {}".format(last_dcc))
        if last_dcc != 0:
            send_message("Dark cloud cover Sell! Sell! Sell! {}".format(close))

print("Morning star and Dark cloud cover 30m bot stared!")
send_message("Morning star and Dark cloud cover 30m bot stared!")
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()