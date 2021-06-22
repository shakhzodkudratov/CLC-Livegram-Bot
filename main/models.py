import uuid

from django.db import models
from django.conf import settings


class SlaveBot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    token = models.CharField(max_length=50, unique=True)
    owner_id = models.PositiveIntegerField()

    @property
    def webhook_url(self):
        return f'{settings.HOST}/bot/{self.id}/'


class IncomingMessage(models.Model):
    slavebot = models.ForeignKey(SlaveBot, on_delete=models.CASCADE)
    owner_id = models.PositiveIntegerField()
    message_id = models.PositiveIntegerField()
