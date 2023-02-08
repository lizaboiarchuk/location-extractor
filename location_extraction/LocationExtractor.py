import pandas as pd
from rapidfuzz import fuzz, process
from string import punctuation
from location_extraction.language_setup import MODELS, LOCATIONS, LOCATION_COL, ABBREVIATIONS, UNNECESSARY_LOCS, REGIONS, CUSTOM_LEMMATIZER


class LocationExtractor:
    def __init__(self, lang, treshold=95):
        self._language = lang
        self.ner_model = MODELS[lang]
        self.locations_list = list(LOCATIONS[LOCATION_COL[lang]])
        self.abbreviations = ABBREVIATIONS[lang]
        self.unnecessary_locs = UNNECESSARY_LOCS[lang]
        self.regions = REGIONS[lang]
        self.punctuation = punctuation + '–'
        self.locations_lower = [loc.lower() for loc in self.locations_list]
        self.match_treshold = treshold
        self.custom_lemmatizer = CUSTOM_LEMMATIZER[lang]

    def _preprocess(self, text):
        text = text.replace('**', ' ')
        text = "".join([s for s in text if (s.isalnum()) or s == ' ' or s in self.punctuation or s == '\n'])
        text = text.encode('utf-8', 'ignore').decode("utf-8")
        text = text.replace('\n', ' ')
        for abb in self.abbreviations.keys():
            text = text.replace(abb, f'{self.abbreviations[abb]} ')
        text = ' '.join(text.split())
        return text

    def _extract_entities(self, text):
        entities = list(map(lambda x: (x.to_dict()['text'], x.to_dict()['type']), self.ner_model(text).entities))
        loc_entities = list(map(lambda x: x[0], filter(lambda x: x[1] in ['LOC', 'MISC'], entities)))
        return loc_entities

    def _clean_entities(self, values):
        return [''.join([s for s in word if s.isalpha() or s in [' ', '-', 'ʼ']]) for word in values]

    def _lemmatize(self, entities, text):
        return [], []

    def _filter_lemmas(self, values):
        filtered = []
        region_indexes = []
        lemmas = values[1]
        for lemma in lemmas:
            for i in self.regions.index:
                row = self.regions.loc[i]
                if row['Region Lemmatized'] in lemma:
                    region_indexes.append(i)
                    lemma = ' '.join(lemma.replace(row['Region Lemmatized'], '').split())
                if row['Region Lemmatized Name'][:-2] in lemma:
                    region_indexes.append(i)
                    lemma = ' '.join(lemma.replace(row['Region Lemmatized Name'], '').split())
                if row['Region Suffix'] == row['Region Suffix'] and row['Region Suffix'][:-2] in lemma:
                    region_indexes.append(i)
                    lemma = ' '.join(lemma.replace(row['Region Suffix'], '').split())
                if row['Region Abb'].split()[0] in lemma and row['Region Abb'].split()[1][:3] in lemma:
                    region_indexes.append(i)
                    lemma = ' '.join(
                        lemma.replace(row['Region Abb'].split()[0], '#').replace(row['Region Abb'].split()[1],
                                                                                 '').split('#')[0].split())
            if lemma in self.regions['Region Lemmatized'].values:
                region_indexes.append(self.regions[self.regions['Region Lemmatized'] == lemma].index[0])
            elif lemma in self.regions['Region Suffix'].values:
                region_indexes.append(self.regions[self.regions['Region Suffix'] == lemma].index[0])
            elif sum(list(map(lambda x: x in lemma, self.unnecessary_locs))) == 0:
                filtered.append(lemma)
        return values[0], filtered, region_indexes

    def _match_location(self, values):
        not_lemmas = values[0]
        lemmas = values[1]
        location_indexes = []
        region_indexes = values[2]
        for word in lemmas:
            if word in list(self.regions.index):
                region_indexes.append(self.regions.loc[word]['index'])
            if not pd.isna(word):
                res = process.extract(word, self.locations_lower, scorer=fuzz.ratio, score_cutoff=self.match_treshold)
                if len(res) > 0:
                    location_indexes.append(res[0][2])
        for word in not_lemmas:
            if word.lower() in self.locations_lower:
                location_indexes.append(self.locations_lower.index(word.lower()))
        return list(set(location_indexes)), list(set(region_indexes))

    def get_locations(self, text):
        preprocessed = self._preprocess(text)
        entities = self._extract_entities(preprocessed)
        clean_entities = self._clean_entities(entities)
        lemmas = self._lemmatize(clean_entities, text)
        filtered_lemmas = self._filter_lemmas(lemmas)
        found_locations = self._match_location(filtered_lemmas)
        return found_locations
