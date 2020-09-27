import logging
import os

import urllib3
from constance import config
from django.core.management.base import BaseCommand
from django.db import transaction

from helpers.telegram.bot import Bot
from tasks.models import Dictionary

_logger = logging.getLogger(__name__)


def _get_random_message() -> str:
    return Dictionary.objects.all().order_by('?').first().message


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        urllib3.disable_warnings()
        telegram = Bot(os.environ.get('TELEGRAM_BOT_TOKEN'), os.environ.get('ADMIN_TELEGRAM_CHAT_ID'))

        result = telegram.get_updates(config.SPAM_TG_LAST_MESSAGE_ID)
        for updates in result:
            if updates.edited_message or updates.channel_post or updates.message.sticker:
                continue

            if updates.message.chat.id_ != config.SPAM_TG_CHAT_ID:
                continue

            if not updates.message.text:
                continue

            if (updates.message.reply_to_message
                and 'pepesaysbot' in updates.message.reply_to_message.from_.username) \
                    or 'пепе' in updates.message.text.lower():

                phrase_dictionary = {
                    'расскажи про': 'Я тебе не Шма',
                    'расскажи историю': 'Я тебе не Шма',
                    'карма': 'Ты ...',
                    'тоша': 'Тоша как всегда, дорогу через бабушку переводит',
                }

                def_dictionary = {
                    'пепе, скажи': lambda x: x[12:],
                    'пепе скажи': lambda x: x[11:]
                }

                response = ''

                for phrase in phrase_dictionary:
                    if phrase in updates.message.text.lower():
                        response = phrase_dictionary[phrase]
                        break

                for phrase in def_dictionary:
                    if phrase in updates.message.text.lower():
                        response = def_dictionary[phrase](updates.message.text)

                if not response:
                    response = _get_random_message()

                telegram.send_message(response, chat_id=updates.message.chat.id_,
                                      reply_to_message_id=updates.message.message_id)

                if updates.message.from_.username \
                        and ('?' not in updates.message.text or 'пепе' not in updates.message.text):
                    Dictionary.objects.create(author=updates.message.from_.username,
                                              message=updates.message.text)

                config.SPAM_TG_LAST_MESSAGE_ID = updates.update_id + 1
