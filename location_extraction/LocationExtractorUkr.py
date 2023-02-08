from location_extraction.LocationExtractor import LocationExtractor
import pymorphy2


class LocationExtractorUkr(LocationExtractor):
    def __init__(self, treshold):
        super().__init__('ukr', treshold)
        self.moph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')

    def _lemmatize(self, entities, text):
        not_lemmas = list(map(lambda x: x.lower(), entities))
        lemmas = []
        for loc in entities:
            parts = []
            for token in loc.split():
                lemma = self.moph_analyzer.parse(token)[-1].normal_form
                if lemma in self.custom_lemmatizer:
                    lemma = self.custom_lemmatizer[lemma]
                parts.append(lemma)
            lemmas.append(' '.join(parts))
        return list(set(not_lemmas)), list(set(lemmas))