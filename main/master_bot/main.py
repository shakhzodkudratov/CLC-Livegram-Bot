from django.conf import settings
from django.db.utils import IntegrityError
from telegram import Bot, Update
from telegram.error import InvalidToken
from telegram.ext import Dispatcher, CallbackContext, CommandHandler

from main.models import SlaveBot


def ready():
    pass
#     hostname = f'{settings.HOST}/bot/'
#     print(f'setting MASTER webhook at {hostname}')
#     bot.set_webhook(hostname)


bot: Bot = Bot(token='')

dispatcher: Dispatcher = Dispatcher(bot, None)


def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Hello!')


def new_bot_handler(update: Update, context: CallbackContext):
    args = context.args
    token = ''.join(args)

    try:
        slave_bot = Bot(token=token)
        bot.get_me()
        slave_bot_instance = SlaveBot.objects.create(
            token=token, owner_id=update.effective_user.id)
        slave_bot.set_webhook(slave_bot_instance.webhook_url)
        update.message.reply_text("Tabriklaymiz, bot muvaffaqiyatli ulandi")
    except InvalidToken:
        update.message.reply_text("Siz noto'g'ri token kiritdingiz")
    except IntegrityError:
        update.message.reply_text("Afsuski, ushbu bot allaqachon ulangan")


dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('new_bot', new_bot_handler))
