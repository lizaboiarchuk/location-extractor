from location_extraction.LocationExtractor import LocationExtractor
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc


class LocationExtractorRu(LocationExtractor):
    def __init__(self, treshold):
        super().__init__('ru', treshold)
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.embed = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.embed)

    def _lemmatize(self, entities, text):
        not_lemmas = list(map(lambda x: x.lower(), entities))
        lemmas = []
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)
        lemmas_dict = {}
        for token in doc.tokens:
            lemmas_dict[token.text] = token.lemma
        for entity in entities:
            parts = []
            for part in entity.split(' '):
                if part in lemmas_dict:
                    lemma = lemmas_dict[part]
                    if lemma in self.custom_lemmatizer:
                        lemma = self.custom_lemmatizer[lemma]
                    parts.append(lemma)
            lemmas.append(' '.join(parts))
        return list(set(not_lemmas)), list(set(lemmas))
