import itertools
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Union

import requests
import urllib3
from bs4 import BeautifulSoup
from constance import config

from helpers.telegram.bot import Bot
from tasks.models import Domain, Feed

_ONE_DAY = 60 * 60 * 24
_FEEDS_TG_CHAT_ID = config.FEED_TG_CHAT_ID

urllib3.disable_warnings()


def _check_feed(feed_link: str) -> Union[str, None]:
    """
    Проверяет фид, если при полуении возникла ошидка или фид собран больше чем за 24 часа, вернет url и текст ошибки
    """
    try:
        response = requests.get(feed_link)
        response.raise_for_status()
        response.encoding = 'UTF-8'
        feed = BeautifulSoup(response.text, 'lxml')
        try:
            last_update = datetime.strptime(feed.find('yml_catalog')['date'], '%Y-%m-%d %H:%M').timestamp()
        except TypeError:
            last_update = datetime.strptime(feed.find('catalog')['date'], '%Y-%m-%dT%H:%M:%S%z').timestamp()

        if datetime.now().timestamp() - last_update > _ONE_DAY:
            return f'{feed_link}\nНе обновлялся больше суток'

    except requests.exceptions.HTTPError as e:
        return f'{feed_link}\n{e.response.status_code} ошибка получения фида'


def check_feeds():
    """Проверяет все фиды, в случае ошибки отправляет сообщение в telegram"""
    telegram = Bot(os.environ.get('TELEGRAM_BOT_TOKEN'), os.environ.get('ADMIN_TELEGRAM_CHAT_ID'))

    solo_feeds = list(Feed.objects.filter(is_active=True, is_multi=False).values_list('url', flat=True))
    multi_feeds = list(Feed.objects.filter(is_active=True, is_multi=True).values_list('url', flat=True))
    domains = list(Domain.objects.filter(is_active=True).values_list('url', flat=True))

    feeds = list(map(lambda x: x[0] + x[1], itertools.product(domains, multi_feeds)))
    feeds += solo_feeds

    telegram.send_message(f'Пошел проверять {len(feeds)} фид(ов)', chat_id=_FEEDS_TG_CHAT_ID)

    with ThreadPoolExecutor(max_workers=3) as pool:
        alerts = pool.map(_check_feed, feeds)

    alerts = [alert for alert in alerts if alert]

    for alert in alerts:
        telegram.send_message(alert, chat_id=_FEEDS_TG_CHAT_ID)

    telegram.send_message(f'{len(feeds) - len(alerts)} фид(ов) актуальны', chat_id=_FEEDS_TG_CHAT_ID)
