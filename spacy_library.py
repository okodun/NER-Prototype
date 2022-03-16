"""
Library for spacy implementation.
Contains only functions that work in the background.
"""

import en_core_web_lg
import spacy.tokens
from collections import Counter


class SpacyModel(object):
    """ class for spacy implementation """

    def __init__(self):
        self.nlp = en_core_web_lg.load()

    def tokenize(self, path_to_text_file: str) -> spacy.tokens.Doc:
        text = open(path_to_text_file, "r").read()
        return self.nlp(text)

    def find_similarities(self, search_term: str, path_to_text_file: str) -> float:
        """ returns the maximum similarity of a given search word to tokens in a text """

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
