from location_extraction.extractors import LocationExtractorUkr, LocationExtractorRu
from location_extraction import locations_setup
import langdetect

ukr_extractor = LocationExtractorUkr(treshold=95, countries=['ua', 'ru', 'by'])
ru_extractor = LocationExtractorRu(treshold=95, countries=['ua', 'ru', 'by'])

def get_locations(text):
    lang = langdetect.detect(text)
    if lang == 'uk':
        locs, regs = ukr_extractor.get_locations(text)
    else:
        locs, regs = ru_extractor.get_locations(text)

    location_items = []
    for (country, ind) in locs:
        raw = locations_setup.LOCATIONS[country].loc[ind]
        item = {
            "country": country,
            "region": raw['region_name_ukr'],
            "location": raw['location_name_ukr'],
            "lon": raw['lon'],
            "lat": raw['lat']
        }
        if item['location'] not in locations_setup.SKIP_LOCATIONS[country]:
            location_items.append(item)

    region_items = []
    for (country, ind) in regs:
        region_items.append((country, locations_setup.REGIONS[country]['ukr'].loc[ind]['Region']))
    return location_items, region_items



if __name__ == '__main__':
    text = 'У білоруському Гомелі помітили ешелон із САУ та танками: деталі'
    print(get_locations(text)[0])
