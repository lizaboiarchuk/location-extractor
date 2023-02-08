import pandas as pd
import stanza


LOCATIONS = pd.read_csv('./files/location/ukraine-locations-v3.csv')

MODELS = {
    'ukr': stanza.Pipeline(lang='uk', processors='tokenize,ner,lemma'),
    'ru': stanza.Pipeline(lang='ru', processors='tokenize,ner,lemma')
}

LOCATION_COL = {
    'ukr': 'location_uk',
    'ru': 'russian_new'
}

ABBREVIATIONS = {
    'ukr': {'м.': 'місто', 'с.': 'село', 'смт.': 'селище'},
    'ru': {'г.': 'город', 'с.': 'село', 'пгт.': 'поселок'}
}

UNNECESSARY_LOCS = {
    'ukr': ['район', 'вул.', 'вулиця', 'пров.', 'вул ', 'площа', 'р-н', ' вул'],
    'ru': ['район', 'ул.', 'улица', 'пер.', 'ул ', 'площадь', 'р-н', ' ул']
}

REGIONS = {
    'ukr': pd.read_csv('files/location/region_names_ukr.csv'),
    'ru': pd.read_csv('files/location/region_names_ru.csv')
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