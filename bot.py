import telebot
import parser
TOKEN = '1301051793:AAGUAMh8DMsv5bFtJnCKMrwfSP59zZ_5Rtg'
bot = telebot.TeleBot(TOKEN)
print("OK")
@bot.message_handler(commands=['start'])
def start_hndlr(msg):
    bot.send_message(msg.chat.id,'Yes, I\'m working !')
    

bot.polling(none_stop=True)
