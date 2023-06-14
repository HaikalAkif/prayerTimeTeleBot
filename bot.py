from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from prayer_times import PrayerTimes
from bot_config import BotConfig
from supabase import create_client, Client

url: str = "https://otpxpqhixwzojqxidshg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90cHhwcWhpeHd6b2pxeGlkc2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODY2ODQ0NDEsImV4cCI6MjAwMjI2MDQ0MX0.ReKar3Lrf8wBDfOpU6FfeUR0wFYtYDtMzHlo41gA21g"
supabase: Client = create_client(url, key)

data_store = {}

# def get_waktu_solat(update: Update, context: ContextTypes.DEFAULT_TYPE):
def get_waktu_solat(zone: str) -> PrayerTimes:

    jakim_api = "https://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=today&zone=" + zone

    try:
        
        response = requests.get(jakim_api)
        response.raise_for_status()
        prayer_times_dict = response.json()

        pt = PrayerTimes(prayer_times_dict['prayerTime'][0])
        
        return pt

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action('TYPING')
    await update.message.reply_text(f'Hello {update.effective_user.first_name}!')

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    today = datetime.now()

    await update.message.reply_chat_action('TYPING')
    await update.message.reply_text('Today is: ' + today.strftime('%d-%b-%Y'))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action('TYPING')
    await update.message.reply_text(f'''
All Commands

/start - bot start
/prayer_times - get today's prayer times
/hello - greeting the bot
/today - show today's date
/change_location - choose Selangor's zone
/help - show all commands
''')
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action('TYPING')
    await update.message.reply_text(f'''
السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ

👋🏻 It's great connecting with you, {update.message.chat.first_name}.

🤖 I am WaqtBot, your assistant in finding accurate prayer times in Selangor for various purposes.

📌 Gombak(Zone 1) has been set as your default location, you can change your main zone by choosing /change_location

''', parse_mode='Markdown')
    
async def get_prayer_times_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    pref = data_store.get(str(context._chat_id), 'SGR01')
    
    pt = get_waktu_solat(zone=pref)
    
    hijri_formatted = pt.hijrah.split('-')
    hijri_formatted.reverse()
    
    await update.message.reply_chat_action('TYPING')
    await update.message.reply_text(f'''
<strong>IIUM Prayer Times ({BotConfig.get_zone_full_name(pref)})</strong>

📅 <strong>Date:</strong> {pt.date.strftime('%d %B %Y')} ({pt.day})
🌙 <strong>Hijri:</strong> {hijri_formatted[0]} {BotConfig.get_malay_hijri_month(hijri_formatted[1])} {hijri_formatted[2]}
    
<strong>Imsak:</strong> {pt.imsak.strftime('%I:%M %p')}
<strong>Subuh:</strong> {pt.subuh.strftime('%I:%M %p')}
<strong>Syuruk:</strong> {pt.syuruk.strftime('%I:%M %p')}
<strong>Zohor:</strong> {pt.zohor.strftime('%I:%M %p')}
<strong>Asar:</strong> {pt.asar.strftime('%I:%M %p')}
<strong>Maghrib:</strong> {pt.maghrib.strftime('%I:%M %p')}
<strong>Isyak:</strong> {pt.isyak.strftime('%I:%M %p')}
''', parse_mode='HTML')

async def change_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    keyboard = BotConfig.get_available_locations()
    
    result = map(lambda x: InlineKeyboardButton(x['name'].split(' - ')[1], callback_data=x['name'].split(' - ')[0]), keyboard)
    
    reply_markup = InlineKeyboardMarkup([list(result)])
    
    await update.message.reply_text('Choose your preferred location', reply_markup=reply_markup)

app = ApplicationBuilder().token("5602722406:AAHrCpTfseKcmvK5hZibD6QmX8H3xkXgU3I").build()

# Define the function to handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    # Handle different button clicks based on the data
    if data == 'Gombak, Petaling, Sepang, Hulu Langat, Hulu Selangor, S.Alam':
        await query.answer('You clicked Button 1')
        # Do something when Button 1 is clicked
    elif data == 'Kuala Selangor, Sabak Bernam':
        await query.answer('You clicked Button 2')
    elif data == 'Klang, Kuala Langat':
        await query.answer('You clicked Button 3')
        
async def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    data_store.update({ str(context._chat_id): query.data })

    await query.edit_message_text(text=f"Your location preference has been set to: {BotConfig.get_zone_full_name(query.data)}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    pref = data_store.get(str(context._chat_id), 'SGR01')

    await update.message.reply_text(pref)

# All telegram commands here
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("prayer_times", get_prayer_times_today))
app.add_handler(CommandHandler("change_location", change_location))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("today", get_date))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("check", check))

# app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()