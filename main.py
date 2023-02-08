from location_extraction.LocationExtractorUkr import LocationExtractorUkr
from location_extraction.LocationExtractorRu import LocationExtractorRu
from location_extraction import language_setup
import langdetect

ukr_extractor = LocationExtractorUkr(treshold=95)
ru_extractor = LocationExtractorRu(treshold=95)


def get_locations(text):
    lang = langdetect.detect(text)
    if lang == 'uk':
        locs, regs = ukr_extractor.get_locations(text)
    else:
        locs, regs = ru_extractor.get_locations(text)
    loc_names = list(language_setup.LOCATIONS.loc[locs]['location'].values)  # indexes of locations -> names
    reg_names = list(language_setup.REGIONS['ukr'].iloc[regs]['Region'])  # indexes of regions -> names
    return loc_names, reg_names


if __name__ == '__main__':
    text = 'Уничтожение предположительно склада боеприпасов ВСУ в районе села Змиевка Херсонской области.'
    print(get_locations(text))
