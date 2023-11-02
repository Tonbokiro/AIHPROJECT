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
        start_message = "Hello! Feel free to ask me any questions about a migrant worker's healthcare in Singapore. Before we begin, we want to emphasize the importance of your privacy. \n\n We value your privacy! While interacting with this chatbot, you agree to our collection, use and/or disclosure of your personal data to the extent necessary to process your question and provide you with an answer. Rest assured, your data is safeguarded under the provisions of Singapore's Personal Data Protection Act (PDPA)."
        bot.send_message(message.chat.id, start_message)

    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Show 'typing...' action
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
