# Intelligent Systems Section 4
# Platik Hitam

import telegram
import requests
from datetime import datetime

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# API endpoint for prayer times
PRAYER_TIMES_API = 'http://api.aladhan.com/v1/timingsByCity'

# Default city for prayer times
DEFAULT_CITY = 'Cairo'

# Create a Telegram Bot object
bot = telegram.Bot(token=TOKEN)

# Handler function for the '/start' command
def start(update, context):
    user = update.message.from_user
    context.bot.send_message(chat_id=update.message.chat_id, text=f"Assalamu Alaikum {user.first_name}! Welcome to the Prayer Time Bot.")
    context.bot.send_message(chat_id=update.message.chat_id, text="Type /prayertime to get the prayer times for today.")

# Handler function for the '/prayertime' command
def prayer_time(update, context):
    city = DEFAULT_CITY
    if len(context.args) > 0:
        city = ' '.join(context.args)
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Send API request to get prayer times
    params = {'city': city, 'country': 'Malaysia', 'method': 5, 'date': today}
    response = requests.get(PRAYER_TIMES_API, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        timings = data['data']['timings']
        message = f"Prayer Times for {city} on {today}:\n\n"
        message += f"Subuh: {timings['Subuh']}\n"
        message += f"Zuhur: {timings['Zuhur']}\n"
        message += f"Asri: {timings['Asri']}\n"
        message += f"Maghrib: {timings['Maghrib']}\n"
        message += f"Isya: {timings['Isya']}\n"
    else:
        message = "Sorry, I couldn't retrieve the prayer times for the specified city."
    
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

# Create an instance of the Updater class and pass the bot token
updater = telegram.Updater(token=TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the command handlers
dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
dispatcher.add_handler(telegram.ext.CommandHandler('prayertime', prayer_time))

# Start the bot
updater.start_polling()
