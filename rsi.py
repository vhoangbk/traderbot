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

    if is_candle_closed:
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                print("Overbought! Sell! Sell! Sell! {}, {}".format(last_rsi, close))
                send_message("Overbought! Sell! Sell! Sell! {}, {}".format(last_rsi, close))
            
            if last_rsi < RSI_OVERSOLD:
                print("Oversold! Buy! Buy! Buy! {}, {}".format(last_rsi, close))
                send_message("Oversold! Buy! Buy! Buy! {}, {}".format(last_rsi, close))

print("RSI 30m bot stared!")  
send_message("RSI 30m bot stared!")   
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()