import telebot
import parser
import yfinance as yf
import requests
import logging
import time
TOKEN = '1301051793:AAGUAMh8DMsv5bFtJnCKMrwfSP59zZ_5Rtg'
DIALOGUE = '509779359'
STOCKS = 'AAPL NVDA AMD MSFT NFLX INTC CSCO ATHX ADBE AEP AAL T BA KO NKE SLB AXP CAT IBM JNJ MCD MA DIS PYPL FB BABA WMT' 
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_hndlr(msg):
    bot.send_message(msg.chat.id,'Yes, I\'m working !')
    
def get_price(stock_name):
    ticker = yf.Ticker(stock_name)
    stck = ticker.get_info()
    return stck['ask']
#bot.polling(none_stop=True)
def get_ask(stock):
    return stock['ask']
def get_bid(stock):
    return stock['bid']
def is_strange_activity(stock,last_price):
    current_price = get_bid(stock)
    delta = current_price - last_price
    return delta , current_price
def make_alert_if_needed(stock, last_price,bot):
    delt, price = is_strange_activity(stock,last_price)
    if True:#abs(delt) > 0.0005*price:        
        text = '🌊Attention!!!!!!!!!!!!\n Stock {0} ({1}) is in unusual activity.'.format(stock['longName'],stock['symbol'])
        text += '💵Low price : {0}, High: {1}, Current - {2}'.format(stock['dayLow'],stock['dayHigh'],price)
        text += '\n Move on {0}$ to {1}$\n'.format(delt,price)    
        text += '\n regularMarketPrice: {0}\n'.format(stock['regularMarketPrice'])
        text += 'earningsQuarterlyGrowth: {0}'.format(stock['earningsQuarterlyGrowth'])
        bot.send_message(DIALOGUE,text)
    return price
def see_all(stock_list, last_prices,bot):
    current = 0
    tickers = yf.Tickers(stock_list).tickers
    new_prices = []
    for t in tickers:    
        stock = t.get_info()
        new_prices.append(make_alert_if_needed(stock,last_prices[current],bot))
        current += 1
    return new_prices
def get_prices(stocks):
    tickers = yf.Tickers(stocks).tickers
    new_prices = []
    for s in tickers:
        new_prices.append(get_bid(s.get_info()))
    return new_prices


if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    prices = get_prices(STOCKS)
    while True:
        #bot.send_message(DIALOGUE,'The AAPL price is ' + str(get_price('AAPL')))
        prices = see_all(STOCKS,prices,bot)
        time.sleep(10)
        