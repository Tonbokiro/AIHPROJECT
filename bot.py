import telebot
import os
from dotenv import load_dotenv
import model


load_dotenv()


load_dotenv("./.env")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
bot.set_webhook()   

@bot.message_handler(commands=['start'])
def start(message):
    """
    Bot will introduce itself upon /start command, and prompt user for his request
    """
    try:
        # Start bot introduction
        start_message = "Hello! Ask me anything about life in Singapore, or if you need help! Before we get started, we'd like to share something important with you. Your privacy matters to us! As you interact with this chatbot, you might share some personal information to help us better understand and address your health benefit queries. We want you to know that your data is protected under Singapore's Personal Data Protection Act (PDPA)."
        bot.send_message(message.chat.id, start_message)

    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    response = model.getResponse(message.text)
    bot.send_message(message.chat.id, response)

def main():
    """Runs the Telegram Bot"""
    print('Loading configuration...') # Perhaps an idea on what you may want to change (optional)
    print('Successfully loaded! Starting bot...')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
    
    print(f"TOKEN: {TELEGRAM_BOT_TOKEN}")
