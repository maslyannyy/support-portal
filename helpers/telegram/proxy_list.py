import json
import os
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

_PATH = os.path.dirname(os.path.abspath(__file__))
_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/65.0.3325.181 Safari/537.36'}


def _parse_proxy_list() -> List[Dict[str, str]]:
    """Парсит список proxy из free-proxy-list"""
    with requests.get('https://free-proxy-list.net/', headers=_HEADERS) as response:
        soup = BeautifulSoup(response.text, "html.parser")
        proxy_rows = soup.find('div', class_='table-responsive').find_all('tr')[1:-1]
        proxy_list = []

        for proxy_row in proxy_rows:
            ip, port = proxy_row.find_all('td')[0:2]
            proxy_list.append({'https': f'https://{ip.text}:{port.text}'})

        proxy_list.insert(0, {'https': ''})
        return proxy_list


def save_proxy_list(proxy_list: list):
    """Сохраняет список proxy в файл"""
    with open(os.path.join(_PATH, 'proxy_list.json'), 'w', encoding='utf-8') as file:
        json.dump(proxy_list, file)


def get_proxy_list() -> List[Dict[str, str]]:
    """Читает список proxy из файла"""
    proxy_list = []
    try:
        with open(os.path.join(_PATH, 'proxy_list.json'), 'a+', encoding='utf-8') as file:
            proxy_list = json.load(file)
    except json.decoder.JSONDecodeError:
        pass
    except FileNotFoundError:
        pass

    if not proxy_list:
        proxy_list = _parse_proxy_list()

    return proxy_list
