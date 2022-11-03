import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat, bot
from config import BOTKEY, chatID, MY_SOLAR_EDGE_SITE, API_KEY, POLLING_RATE_SEC
from threading import Timer,Thread,Event
from random import uniform
import requests
from datetime import datetime

def getTimestamp():
    dt = datetime.now()
    return dt


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)




# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def now(update, context):
    """Send a message when the command /now is issued."""
    getDataFromSolarEdge(update, True)


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/now per ricevere dati attuali\nLe notifiche imporanti te le mando io!')


def startBot():
    global updater
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True
    updater = Updater(BOTKEY, use_context=True)

    # Get the dispatcher to register handlers  (callbacks)
    dp = updater.dispatcher

    # add an handler for each command
    # start and help are usually defined
    dp.add_handler(CommandHandler("now", now))
    dp.add_handler(CommandHandler("help", help_command))

    # Start the Bot (polling of messages)
    # this call is non-blocking
    updater.start_polling()

    return updater

# call a function each t seconds
class perpetualTimer():

    def __init__(self, t, hFunction, param):
        self.t = t
        self.hFunction = hFunction
        self.param = param
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction(self.param)
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

def getDataFromSolarEdge(updater, forcePrint=False):
    url = 'https://monitoringapi.solaredge.com/site/{}/currentPowerFlow?api_key={}'.format(MY_SOLAR_EDGE_SITE, API_KEY)
    responseJsonBody = requests.get(url).json()
    response = responseJsonBody.get('siteCurrentPowerFlow')

    sun = response.get('PV')
    battery = response.get('STORAGE')
    load = response.get('LOAD')

    sun_value = float(sun.get('currentPower'))
    battery_perc = int(battery.get('chargeLevel'))
    load_value = float(load.get('currentPower'))

    connections = response.get('connections')
    sending_to_grid = False
    for k in connections:
        print(k)
        if k.get('to').upper() == 'GRID':
            sending_to_grid = True
            break

    #time passed from last update
    global ts
    hours = 100000000 #sempre all'avvio
    if(ts != None):
        now = getTimestamp()
        diff = now - ts
        hours = diff.total_seconds() / 60 / 60
    
    #check if we want to send the update
    print('hours:{}'.format(hours))
    check = False
    if(hours >= 1 and sending_to_grid): 
        ts = getTimestamp()
        check = True
    if(hours >= 4): 
        ts = getTimestamp()
        check = True
    if(forcePrint): check = True

    if(not check): return
    #send message to the chat
    sun_text = 'Sun Power 🌤️: {}kW, stato: {}'.format(sun_value,sun.get('status'))
    battery_text = 'Battery% 🔋: {}%, stato: {}'.format(battery_perc,battery.get('status'))
    load_text = 'Consumi 🏠: {}kW, stato: {}'.format(load_value,load.get('status'))

    message = [sun_text,battery_text,load_text]
    message_txt = ''
    if(sending_to_grid):
        message_txt += '⚠️Attenzione stai mandando energia in rete! Sfruttala ORA⚠️\n'
    message_txt += 'STATO ATTUALE:\n'
    message_txt += ('\n').join(message)

    print(message)
    if(hasattr(updater, 'bot')):
        updater.bot.send_message(chat_id=chatID, text=message_txt)
    else:
        updater.message.reply_text(message_txt)



if __name__ == '__main__':
    ts = None
    # start bot_
    updater = startBot()
    
    # start polling thread
    poller = perpetualTimer(POLLING_RATE_SEC,getDataFromSolarEdge,updater)
    poller.start()
    

    # idle (blocking)
    updater.idle()