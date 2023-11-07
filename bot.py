import telebot
import os
from dotenv import load_dotenv
import model


load_dotenv()


load_dotenv("./.env")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
bot.set_webhook()   

# Dictionary to store user language preferences
user_language = {}

@bot.message_handler(commands=['start'])
def start(message):
    """
    Bot will introduce itself upon /start command, and prompt user for his request
    """
    try:
        # Start bot introduction
        start_message = "Hello! Feel free to ask about migrant healthcare in Singapore in your language.  We respect your privacy—by using this bot, you agree to data handling as per Singapore's PDPA. Your info is safe with us! \n\nহ্যালো! আপনার ভাষায় সিঙ্গাপুরে অভিবাসী স্বাস্থ্যসেবা সম্পর্কে নির্দ্বিধায় জিজ্ঞাসা করুন। আমরা আপনার গোপনীয়তাকে সম্মান করি—এই বটটি ব্যবহার করে, আপনি সিঙ্গাপুরের PDPA অনুযায়ী ডেটা পরিচালনা করতে সম্মত হন। আপনার তথ্য আমাদের কাছে নিরাপদ! \n\nவணக்கம்! சிங்கப்பூரில் புலம்பெயர்ந்தோர் மருத்துவம் பற்றி உங்கள் மொழியில் கேட்கலாம். உங்கள் தனியுரிமையை நாங்கள் மதிக்கிறோம்—இந்தப் போட்டைப் பயன்படுத்துவதன் மூலம், சிங்கப்பூரின் PDPA இன் படி தரவு கையாளுதலை ஒப்புக்கொள்கிறீர்கள். உங்கள் தகவல் எங்களிடம் பாதுகாப்பாக உள்ளது!"
        bot.send_message(message.chat.id, start_message)

    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')

# Function to handle '/help' command
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Here are some commands you can use:\n"
    help_text += "/start - Start the bot| শুরু করুন| தொடங்கு \n"
    help_text += "/language - View the language options| ভাষা | மொழிகள் \n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['language'])
def change_language(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("English", callback_data="English"),
        telebot.types.InlineKeyboardButton("Tamil", callback_data="Tamil"),
        telebot.types.InlineKeyboardButton("Bengali", callback_data="Bengali")
    )
    bot.reply_to(message, "Choose a language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Store the user's language choice
    user_language[call.message.chat.id] = call.data

    # Confirmation message in the chosen language
    confirmation_message = {
        "English": "Language set to English.",
        "Tamil": "மொழி தமிழாக அமைக்கப்பட்டுள்ளது.",
        "Bengali": "ভাষা বাংলা হিসাবে সেট করা হয়েছে."
    }

    additional_message = {
        "English": "Welcome! Feel free to ask any questions about migrant workers' healthcare in Singapore.",
        "Tamil": "நாங்கள் தொடங்குவதற்கு முன், உங்கள் தனியுரிமையின் முக்கியத்துவத்தை வலியுறுத்த விரும்புகிறோம். \n\nஉங்கள் தனியுரிமையை நாங்கள் மதிக்கிறோம்! இந்த சாட்போட் உடன் தொடர்பு கொள்ளும்போது, உங்கள் கேள்வியைச் செயலாக்குவதற்கும் பதிலை உங்களுக்கு வழங்குவதற்கும் தேவையான அளவிற்கு உங்கள் தனிப்பட்ட தரவை சேகரிப்பது, பயன்படுத்துதல் மற்றும்/அல்லது வெளிப்படுத்துதல் ஆகியவற்றை ஒப்புக்கொள்கிறீர்கள். சிங்கப்பூரின் தனிப்பட்ட தரவுப் பாதுகாப்புச் சட்டத்தின் (PDPA) விதிகளின் கீழ் உங்கள் தரவு பாதுகாக்கப்படுகிறது.",
        "Bengali": "আমরা শুরু করার আগে, আমরা আপনার গোপনীয়তার গুরুত্বের উপর জোর দিতে চাই। \n\nআমরা আপনার গোপনীয়তাকে সম্মান করি! এই চ্যাটবটের সাথে ইন্টারঅ্যাক্ট করার সময়, আপনি আপনার প্রশ্ন প্রক্রিয়াকরণ এবং আপনাকে একটি উত্তর প্রদান করার জন্য প্রয়োজনীয় পরিমাণে আপনার ব্যক্তিগত ডেটা সংগ্রহ, ব্যবহার এবং/অথবা প্রকাশে সম্মত হন। আপনার ডেটা সিঙ্গাপুরের ব্যক্তিগত ডেটা সুরক্ষা আইন (PDPA) এর বিধানের অধীনে সুরক্ষিত।"
    }

    # Send confirmation message
    bot.answer_callback_query(call.id, confirmation_message[call.data])
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=confirmation_message[call.data]
    )
    # Send additional message
    bot.send_message(
        chat_id=call.message.chat.id,
        text=additional_message[call.data]
    )
    
@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Show 'typing...' action
    response = model.getResponse(message.text)
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

# Function to handle regular text messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "I didn't understand that. Type /help for commands.")
def main():
    """Runs the Telegram Bot"""
    print('Loading configuration...') # Perhaps an idea on what you may want to change (optional)
    print('Successfully loaded! Starting bot...')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
    
    print(f"TOKEN: {TELEGRAM_BOT_TOKEN}")
