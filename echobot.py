import logging
import threading
from telegram.ext import Filters, MessageHandler, Updater
import pytimeparse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('echobot')


def draw_progress_bar(progress, width=10):

    filled = int(round(progress * width))
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]"


class EchoBot:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Токен не указан")
        self.api_key = api_key
        self.updater = Updater(self.api_key, use_context=True)
        self.dispatcher = self.updater.dispatcher
        logger.info('Эхобот инициализирован')


    def create_timer(self, delay, function):
        timer = threading.Timer(delay, function)
        timer.start()
        logger.info("Таймер создан, функция будет вызвана через {} секунд".format(delay))


    def notify_progress(self, secs_left, total_secs, chat_id, message_id, context):
        if secs_left > 0:
            progress = 1 - (secs_left / total_secs)
            progress_bar = draw_progress_bar(progress)
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="Осталось {} секунд...\n{}".format(secs_left, progress_bar)
            )
            threading.Timer(1, self.notify_progress, args=(secs_left - 1, total_secs, chat_id, message_id, context)).start()
        else:
            context.bot.send_message(chat_id=chat_id, text="Время вышло!")


    def reply_on_message(self):
        def handle_text(update, context):
            users_reply = update.message.text
            chat_id = update.message.chat_id
            delay = pytimeparse.parse(users_reply)

            if delay is not None:
                message = context.bot.send_message(
                    chat_id=chat_id,
                    text="Таймер установлен на {}.".format(users_reply)
                )
                self.notify_progress(delay, delay, chat_id, message.message_id, context)
            else:
                context.bot.send_message(
                    chat_id=chat_id,
                    text="Некорректный формат времени. Используйте, например, '3s' или '5m'."
                )

        self.dispatcher.add_handler(MessageHandler(Filters.text, handle_text))


    def run_bot(self):
        logger.info("Эхобот запущен и ожидает сообщений...")
        self.updater.start_polling()
        self.updater.idle()


def main():
    from dotenv import load_dotenv
    import os

    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    bot = EchoBot(TELEGRAM_TOKEN)
    bot.reply_on_message()
    bot.run_bot()


if __name__ == "__main__":
    main()