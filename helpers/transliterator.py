def transliterate(word: str) -> str:
    """Функция транслитерирует слово переданное в параметрах с RU на EN"""
    case_letters = str.maketrans(
        {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y',
            'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
        }
    )

    word = word.lower()

    return word.translate(word.maketrans(case_letters))
