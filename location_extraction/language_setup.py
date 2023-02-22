import stanza

MODELS = {
    'ukr': stanza.Pipeline(lang='uk', processors='tokenize,ner,lemma'),
    'ru': stanza.Pipeline(lang='ru', processors='tokenize,ner,lemma')
}

LOCATION_NAME_COLUMNS = {
    "ukr": "location_name_ukr",
    "ru": "location_name_ru"
}

ABBREVIATIONS = {
    'ukr': {'м.': 'місто', 'с.': 'село', 'смт.': 'селище'},
    'ru': {'г.': 'город', 'с.': 'село', 'пгт.': 'поселок'}
}

UNNECESSARY_LOCS = {
    'ukr': ['район', 'вул.', 'вулиця', 'пров.', 'вул ', 'площа', 'р-н', ' вул'],
    'ru': ['район', 'ул.', 'улица', 'пер.', 'ул ', 'площадь', 'р-н', ' ул']
}

CUSTOM_LEMMATIZER = {
    'ukr': {
        "лнр": "луганський область",
        "днр": "донецький область",
        "донбас": "донецький область",
    },

    'ru': {
        "лнр": "луганский область",
        "днр": "донецкий область",
        "донбасс": "донецкий область",
    }
}