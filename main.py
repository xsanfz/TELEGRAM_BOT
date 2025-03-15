from dotenv import load_dotenv
import os
from echobot import EchoBot

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


if __name__ == "__main__":
    bot = EchoBot(TELEGRAM_TOKEN)
    bot.reply_on_message()
    bot.run_bot()
