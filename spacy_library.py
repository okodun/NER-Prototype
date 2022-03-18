"""
Library for spaCy implementation.
Contains nlp functionality based on the spaCy toolkit.

Created by Mert Caliskan (22442138) and Felix Schuhmann (22749060).
"""

import en_core_web_lg
import spacy.tokens
from collections import Counter


class SpacyModel(object):
    """ class for spacy implementation """

    def __init__(self):
        """ initialize object by loading pre-trained spaCy pipeline """
        self.nlp = en_core_web_lg.load()

    def tokenize(self, path_to_text_file: str) -> spacy.tokens.Doc:
        """ tokenizes a text and returns the tokens in a spaCy Doc object """
        text = open(path_to_text_file, "r").read()
        return self.nlp(text)

    def find_avg_max_similarity(self, search_term: str, path_to_text_file: str) -> float:
        """ returns the average of the maximum similarity between a given search word and all text tokens """

        # tokenize search word
        search_words = self.nlp(search_term)

        # find tokens with maximum similarity to keywords
        result = {}
        tokens = self.tokenize(path_to_text_file)
        for token in tokens:
            for sw in search_words:
                similarity = sw.similarity(token)
                if sw not in result.keys() or similarity >= result[sw][0]:
                    result.update({sw: (similarity, token)})

        # return maximum similarity
        return sum(result[r][0] for r in result) / len(result)

    def find_organizations(self, search_word: str, path_to_text_file: str) -> {}:
        """ find and return named entities and their similarity to the search term """

        # tokenize search word
        search_words = self.nlp(search_word)

        # tokenize tokens
        tokens = self.tokenize(path_to_text_file)

        # find entities and organizations
        entities = []
        organizations = []
        for token in tokens.ents:
            if token.label_ == "ORG":
                entities.append(token)
                organizations.append(token.text)

        # count unique organizations
        organizations = Counter(organizations)

        # return similar entities
        result = {}
        for ent in entities:
            result.update({ent.text: (ent.similarity(search_words), organizations[ent.text])})

        return result
