import telebot
import parser
import yfinance as yf
import requests
import logging
import time
SINGLE_RUN = 60
TOKEN = '1301051793:AAGUAMh8DMsv5bFtJnCKMrwfSP59zZ_5Rtg'
DIALOGUE = '509779359'
bot = telebot.TeleBot(TOKEN)
print("OK")
@bot.message_handler(commands=['start'])
def start_hndlr(msg):
    bot.send_message(msg.chat.id,'Yes, I\'m working !')
    
def get_price(stock_name):
    ticker = yf.Ticker(stock_name)
    stck = ticker.get_info()
    return stck['ask']
#bot.polling(none_stop=True)

if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    while True:
        bot.send_message(DIALOGUE,'The AAPL price is ' + str(get_price('AAPL')))
        time.sleep(30)
