from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from prayer_times import PrayerTimes

jakim_api = "https://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=today&zone=WLY01"

# def get_waktu_solat(update: Update, context: ContextTypes.DEFAULT_TYPE):
def get_waktu_solat():
    
    try:
        response = requests.get(jakim_api)
        response.raise_for_status()
        prayer_times_dict = response.json()
        
        pt = PrayerTimes(prayer_times_dict['prayerTime'][0])
        
        # Contoh
        print(pt.date)
        print(pt.subuh.strftime('%I:%M %p'))
        print(pt.zohor.strftime('%I:%M %p'))
        print(pt.asar.strftime('%I:%M %p'))
        print(pt.maghrib.strftime('%I:%M %p'))
        print(pt.isyak.strftime('%I:%M %p'))

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action('TYPING')
    await update.message.reply_text(f'{update.effective_user.first_name} memang hensem')

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    today = datetime.now()
    
    await update.message.reply_chat_action('TYPING')
    await update.message.reply_text('Today is: ' + today.strftime('%d-%b-%Y'))

app = ApplicationBuilder().token("5602722406:AAHrCpTfseKcmvK5hZibD6QmX8H3xkXgU3I").build()

# Letak command sini
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("today", get_date))

app.run_polling()

if __name__ == "__main__":
    get_waktu_solat()