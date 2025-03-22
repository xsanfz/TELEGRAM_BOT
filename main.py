from dotenv import load_dotenv
import os
import ptbot
from pytimeparse import parse
from functools import partial


def render_progressbar(total, iteration, prefix='', suffix='', length=20, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def wait(bot, chat_id, question):
    delay = parse(question)
    if delay is None:
        bot.send_message(chat_id, "Неверный формат времени")
        return

    message_id = bot.send_message(chat_id, render_progressbar(delay, delay, prefix="Осталось:"))

    bot.create_countdown(delay, notify_progress, bot=bot, chat_id=chat_id, message_id=message_id, delay=delay)
    bot.create_timer(delay, choose, bot=bot, chat_id=chat_id, question=question)


def notify_progress(secs_left, bot, chat_id, message_id, delay):
    progressbar = render_progressbar(delay, delay - secs_left, prefix="Осталось:")
    bot.update_message(chat_id, message_id, progressbar)


def choose(bot, chat_id, question):
    message = "Время вышло"
    bot.send_message(chat_id, message)


def main():
    load_dotenv()
    bot = ptbot.Bot(os.getenv("TELEGRAM_TOKEN"))
    bot.reply_on_message(partial(wait, bot=bot))
    bot.run_bot()


if __name__ == "__main__":
    main()
