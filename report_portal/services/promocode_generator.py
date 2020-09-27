import random
import string
from typing import List


def generate_promo_codes(count: int, length: int, prefix: str, postfix: str) -> List[str]:
    """Генерирует count промокдов, с длиной length, добавляет prefix в начале и postfix в конце"""
    alpha = string.ascii_lowercase + string.digits

    list_promo = set()
    while len(list_promo) < count:
        promo_code = ''
        for j in range(length):
            promo_code += alpha[random.randint(0, len(alpha) - 1)]
        promo_code = (prefix + promo_code + postfix).upper()
        list_promo.add(promo_code)
    return list(list_promo)
