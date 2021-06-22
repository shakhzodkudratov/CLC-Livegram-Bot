import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from main.master_bot.main import bot as master_bot, \
    dispatcher as master_dispatcher
from main.slave_bot.main import get_bot as get_slave_bot, \
    get_dispatcher as get_slave_dispatcher
from main.models import SlaveBot


@method_decorator(csrf_exempt, 'dispatch')
class MasterView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            data = json.loads(body)
            update: Update = Update.de_json(data, master_bot)
            master_dispatcher.process_update(update)
        except Exception as e:
            print('\n\n Exception:\n')
            print(e)

        return HttpResponse('ok', status=200)


@method_decorator(csrf_exempt, 'dispatch')
class SlaveView(View):
    http_method_names = ['post']

    def post(self, request, id, *args, **kwargs):
        try:
            bot_instance = SlaveBot.objects.get(id=id)
            bot = get_slave_bot(token=bot_instance.token)
            dispatcher = get_slave_dispatcher(bot)
            body = request.body
            data = json.loads(body)
            update: Update = Update.de_json(data, bot)
            dispatcher.process_update(update)
        except Exception as e:
            print('\n\n Exception:\n')
            print(e)
        return HttpResponse('ok', status=200)
