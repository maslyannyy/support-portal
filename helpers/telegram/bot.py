import logging
import time
from typing import Union, Dict, List

import requests

from helpers.telegram.parsing import SendMessageResponse, GetUpdatesResponse, GetUpdatesResult, Message
from helpers.telegram.proxy_list import get_proxy_list, save_proxy_list

_logger = logging.getLogger(__name__)


def _try_to_send_message(url: str, params: Dict[str, Union[str, int]]) -> requests.models.Response:
    """Отправляет запрос с новой прокси, пока запрос не будет отправлен"""
    proxies = get_proxy_list()
    current_proxy = {}
    response = False

    while not response:
        try:
            with requests.get(url=url, params=params, proxies=current_proxy) as response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            _logger.error(e)
            if response.status_code == 400:
                break
            if response.status_code == 429:
                _logger.warning(response)
                wait_time = int(response.headers['Retry-After'])
                time.sleep(wait_time)
        except requests.exceptions.ProxyError:
            current_proxy = proxies.pop(0)
        except StopIteration:
            proxies = iter(get_proxy_list())
    else:
        proxies.insert(0, current_proxy)
        save_proxy_list(proxies)
        return response


class Bot:
    def __init__(self, token: str, error_chat_id: Union[str, int]):
        if not token:
            raise TypeError('missing argument token')

        if not error_chat_id:
            raise TypeError('missing argument error_chat_id')

        self.token = token
        self.error_chat_id = error_chat_id

    def send_message(self, text: str, chat_id: Union[str, int] = '',
                     reply_to_message_id: Union[str, int] = '') -> SendMessageResponse:
        """Отправляет сообщение в telegram"""
        if not chat_id:
            chat_id = self.error_chat_id

        request_url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        request_params = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
            'reply_to_message_id': reply_to_message_id
        }

        response = _try_to_send_message(request_url, request_params)

        try:
            message = SendMessageResponse(**response.json())
            return message
        except KeyError as e:
            _logger.error(f"SendMessageResponse parsing error {e}")

    def get_updates(self, last_update_id: Union[str, int]) -> List[GetUpdatesResult]:
        """Получает обновления из telegram"""
        request_url = f'https://api.telegram.org/bot{self.token}/getUpdates'
        request_params = {
            'offset': last_update_id
        }

        response = _try_to_send_message(request_url, request_params)

        try:
            Message.update_forward_refs()
            message = GetUpdatesResponse(**response.json())
            return message.result
        except KeyError as e:
            _logger.error(f"GetUpdatesResponse parsing error {e}")
