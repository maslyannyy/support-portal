import logging
import os
import re
import time

import requests
import urllib3
from bs4 import BeautifulSoup
from constance import config
from django.core.management.base import BaseCommand
from django.db import transaction

from helpers.telegram.bot import Bot

_logger = logging.getLogger(__name__)
_JIRA_DOMAIN = config.JIRA_DOMAIN
_JIRA_FILTER_URL = f'{_JIRA_DOMAIN}/issues/?filter={config.JIRA_FILTER_ID}'
_JIRA_AUTH_URL = f'{_JIRA_DOMAIN}/rest/gadget/1.0/login?os_username={config.JIRA_LOGIN}' \
                 f'&os_password={config.JIRA_PASSWORD}&os_destination=&user_role=&atl_token=' \
                 f'&login=%D0%92%D1%85%D0%BE%D0%B4'
_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/65.0.3325.181 Safari/537.36'}


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        urllib3.disable_warnings()

        session = requests.Session()

        response = session.get(_JIRA_AUTH_URL, headers=_HEADERS, verify=False)
        response.raise_for_status()

        time.sleep(1)

        response = session.get(_JIRA_FILTER_URL, headers=_HEADERS, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'id': 'issuetable'})
        table_rows = table.find_all('tr')[1:-1]
        table_rows.reverse()

        telegram = Bot(os.environ.get('TELEGRAM_BOT_TOKEN'), os.environ.get('ADMIN_TELEGRAM_CHAT_ID'))

        task_number = 0

        for row in table_rows:
            task_link = row.find('td', {'class': 'issuekey'}).find('a').text
            task_number = int(task_link.replace('SD-', ''))
            task_summary = row.find('td', {'class': 'summary'}).find('a').text

            if config.JIRA_LAST_TASK_ID >= task_number:
                continue

            task_summary = re.sub(r'[^\w\s]', r'', task_summary)
            message = f'<a href="{_JIRA_DOMAIN}/browse/{task_link}" target="_blank">' \
                      f'{task_link}</a> {task_summary}'

            telegram.send_message(message, chat_id=config.JIRA_TG_CHAT_ID)

        config.JIRA_LAST_TASK_ID = task_number
