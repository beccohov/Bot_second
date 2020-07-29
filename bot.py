import requests
from lxml import html as lhtml
import re
import telebot
import logging
import time
TOKEN = '1301051793:AAGUAMh8DMsv5bFtJnCKMrwfSP59zZ_5Rtg'
DIALOGUE = '509779359'
STOCKS = 'AAPL NVDA AMD MSFT NFLX INTC CSCO ATHX ADBE AEP AAL T BA KO NKE SLB AXP CAT IBM JNJ MCD MA DIS PYPL FB BABA WMT HD PEP QCOM' 
STOCKS += ' UAL HAS MMM HOG SBUX GM EBAY SPOT APRN NOW ORLY UPS KHC MA PG EA XOM PINS JPM GS RACE DPZ MO ATVI WFC C' 

def get_prev_close_and_borders(tree):
    prev_close = tree.xpath(r'//span[@class="price-row-price"]')[0].text_content()
    dayL = tree.xpath(r'//div[@class="col-xs-6 no-padding-left text-left"]')[0].text_content()
    dayL = re.search(r'\d{1,}.\d{1,}',dayL)
    if dayL:
      dayL = dayL.group(0)
    else:
      dayL = 'No data'
    day_H = tree.xpath(r'//div[@class="col-xs-6 no-padding-right text-right"]')[0].text_content()
    day_H = re.search(r'\d{1,}.\d{1,}', day_H)
    if day_H:
      day_H = day_H.group(0)
    else:
      day_H = 'No data'
    
    return prev_close,dayL,day_H

def get_names(page_tree):
    texts = page_tree.xpath(r'//h1[@class="text-uppercase no_margin"]')[0].text_content()
    texts = texts.replace('\r','').replace('\n','')
    texts = texts.split()
    return texts[0],texts[1]

def get_price_and_day_change(page_tree):
    object_ = page_tree.xpath(r'//span[@data-format="maximumFractionDigits:2"]')
    price = object_[0].text
    change = object_[1].text
    return price, change


def get_information_pack(stock_label):
    base = 'https://markets.businessinsider.com/stocks/'
    url = base + stock_label.lower() + '-stock'
    page = requests.get(url)
    tree = lhtml.fromstring(page.text)
    price, change = get_price_and_day_change(tree)
    full_name, short_name = get_names(tree)
    prev_close, l,h = get_prev_close_and_borders(tree)
    result = {'price' : price, 'day_change' : change,'full_name':full_name, 'short_name':short_name}
    result['prev_close'] = prev_close
    result['Day_l'] = l
    result['Day_h'] = h
    return result

def get_only_price(stock):
    base = 'https://markets.businessinsider.com/stocks/'
    url = base + stock.lower() + '-stock'
    page = requests.get(url)
    if not page.status_code == 200:        
        raise ConnectionError
    tree = lhtml.fromstring(page.text)
    price, some = get_price_and_day_change(tree)
    price = float(price)
    return price



bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_hndlr(msg):
    bot.send_message(msg.chat.id,'Yes, I\'m working !')
    


def make_alert_if_needed(stock_label, last_price,bot):
    stock_data = get_information_pack(stock_label)
    price = float(stock_data['price']) 
    delt = price - last_price
    if abs(delt) > 0.003*price:     
        if delt > 0:
            trand = '📈'
        else:
            trand = '📉'
        text = trand + '🌊Attention!!!!!!!!!!!!\n Stock {0} {1} is in unusual activity.'.format(stock_data['full_name'],stock_data['short_name'])
        text += '💵Previous close price : {0}, Current - {1}'.format(stock_data['prev_close'],price)
        text += '\n Day low : {0},Day high : {1}'.format(stock_data['Day_l'], stock_data['Day_h'])
        text += '\n Move on {0}$ to {1}$\n'.format(delt,price)            
        text += '\n Daychange {0}'.format(stock_data['day_change'])
        bot.send_message(DIALOGUE,text)
    return price
def see_all(stock_list, last_prices,bot):
    current = 0  
    new_prices = []
    for t in stock_list.split():    
        try:
            new_prices.append(make_alert_if_needed(t,last_prices[current],bot))
            current += 1
        except:
            new_prices.append(last_prices[current])
            current += 1
            bot.send_message(DIALOGUE,'Exception')
        
    return new_prices
def get_prices(stocks):
    new_prices = []
    for s in stocks.split():
        new_prices.append(get_only_price(s))
    return new_prices
 









 
if __name__ == '__main__':
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    prices = get_prices(STOCKS)
    iteration = 0
    bot.send_message(DIALOGUE,'Started!')
    while True:
        #bot.send_message(DIALOGUE,'The AAPL price is ' + str(get_price('AAPL')))
        prices = see_all(STOCKS,prices,bot)
        iteration +=1
        iteration %= 5
        if iteration == 0:
            bot.send_message(DIALOGUE,'Robot is working...')
        
        time.sleep(10)
        #time.sleep(10)
        