import pandas as pd
import json


with open('files/locations/ua-decom-dict.json', 'r') as f:
    UA_DECOMMUNIZATION = json.load(f)

DECOMMUNIZATION_DICT = {
    "ua": UA_DECOMMUNIZATION,
    "ru": {},
    "by": {}
}

LOCATIONS = {
    "ua": pd.read_csv('files/locations/ua-locations-decom.csv'),
    "ru": pd.read_csv('files/locations/ru-locations.csv'),
    "by": pd.read_csv('files/locations/by-locations.csv')
}

REGIONS = {
    "ua": {
        "ukr": pd.read_csv('files/regions/region_ua_ukr.csv'),
        "ru": pd.read_csv('files/regions/region_ua_ru.csv')
    },
    "ru": {
        "ukr": pd.read_csv('files/regions/region_ru_ukr.csv'),
        "ru": pd.read_csv('files/regions/region_ru_ru.csv')
    },
    "by": {
        "ukr": pd.read_csv('files/regions/region_by_ukr.csv'),
        "ru": pd.read_csv('files/regions/region_by_ru.csv')
    }
}

SKIP_LOCATIONS = {
    "ua": ["Українець", "Берлин", "Республіка", "Воронеж", "Саша"],
    "ru": [],
    "by": []
}