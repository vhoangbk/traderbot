import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *
import logger
import telegram

SOCKET = "wss://stream.binance.com:9443/ws/adausdt@kline_5m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ADAUSDT'
TRADE_QUANTITY = 20

# CHAT_ID = "1045854948" # privte
CHAT_ID = "-553545116" # group
TOKEN = "1800779983:AAHNfSzhmigrvdmj2iXrU28d01ywOTngkOM"

closes = []
opens = []
lows = []
highs = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

def send_message(message):
    print("send message to telegram")
    bot = telegram.Bot(TOKEN)
    bot.sendMessage(chat_id=CHAT_ID, text=message)

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order")
        logger.log("Sending order")
        send_message("Sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        logger.log("an exception occurred - {}".format(e))
        print("an exception occurred - {}".format(e))
        send_message("an exception occurred - {}".format(e))
        return False

    return True

    
def on_open(ws):
    print('opened connection')

def on_close(ws, close_status_code, close_msg):
    print("closed connection ${} - ${}".format(close_msg, close_status_code))

def on_message(ws, message):
    global closes, opens, lows, highs, in_position
    print("received message!")
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']
    open = candle['o']
    low = candle['l']
    high = candle['h']

    if is_candle_closed:
        print("candle closed at {}".format(close))
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

        dark_cloud_cover = talib.CDLDARKCLOUDCOVER(np_opens, np_highs, np_lows, np_closes)
        print("dark cloud cover")
        print(dark_cloud_cover)
        last_dcc = dark_cloud_cover[-1]
        print("last dark cloud cover: {}".format(last_dcc))


        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! {}, {}".format(last_rsi, close))
                    send_message("Overbought! {}, {}".format(last_rsi, close))
                    logger.log("Overbought! {}, {}".format(last_rsi, close))
                    # put binance sell logic here
                    if last_dcc != 0:
                        logger.log("Sell! Sell! Sell! {}".format(close))
                        send_message("Sell! Sell! Sell! {}".format(close))
                        order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                        if order_succeeded:
                            in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! {}, {}".format(last_rsi, close))
                    logger.log("Oversold! {}, {}".format(last_rsi, close))
                    send_message("Oversold! {}, {}".format(last_rsi, close))
                    # put binance buy order logic here
                    if last_morning_star != 0:
                        logger.log("Buy! Buy! Buy! {}".format(close))
                        send_message("Buy! Buy! Buy! {}".format(close))
                        order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                        if order_succeeded:
                            in_position = True

logger.log("Bot start...")
send_message("Bot start...")    
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()