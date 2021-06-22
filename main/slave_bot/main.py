from telegram.ext import Dispatcher, CallbackContext, MessageHandler, Filters
from telegram import Bot, Update

from main.models import SlaveBot, IncomingMessage


def get_bot(token: str):
    return Bot(token=token)


def get_dispatcher(bot: Bot):
    dispatcher: Dispatcher = Dispatcher(bot, None)
    dispatcher.add_handler(MessageHandler(Filters.all, handler))
    return dispatcher


def handler(update: Update, context: CallbackContext):
    slave_instance = SlaveBot.objects.get(token=context.bot.token)
    is_reply = update.message.reply_to_message is not None
    is_owner = update.effective_user.id == slave_instance.owner_id

    if is_owner and is_reply:
        try:
            incoming_message = IncomingMessage.objects.get(
                message_id=update.message.reply_to_message.message_id - 1,
                slavebot=slave_instance,
            )
            context.bot.forward_message(
                chat_id=incoming_message.owner_id,
                from_chat_id=slave_instance.owner_id,
                message_id=update.message.message_id
            )
        except Exception as e:
            print(e)
            print('error occured')
            pass
    else:
        context.bot.forward_message(
            chat_id=slave_instance.owner_id,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )

        IncomingMessage.objects.create(
            message_id=update.message.message_id,
            owner_id=update.effective_user.id,
            slavebot=slave_instance,
        )
