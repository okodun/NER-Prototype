"""
Library for naive implementation.
Contains only functions that work in the background.
"""

import re
from string import punctuation, whitespace
from collections import Counter
from math import sqrt


def tokenize(path_to_text_file: str) -> []:
    """ open a text file and return its contents as list of tokens """

    # read text file into string
    text = open(path_to_text_file, "r").read()

    # tokenize text
    tokens = []
    for token in re.split(f'[%s%s]' % (punctuation, whitespace), text):
        if token != "":  # ignore empty tokens
            tokens.append(token)

    # return tokens
    return tokens


def cosine_distance(word1: str, word2: str) -> float:
    """ return cosine distance of two words """

    def __vectorize(word: str) -> ():
        """
        vectorize word and return its vector as triple
        source of code: (checked March 11, 2022 11:27 AM)
            https://stackoverflow.com/questions/29484529/cosine-similarity-between-two-words-in-a-list
        """

        # count different characters in word
        cw = Counter(word)

        # calculate set of different characters in word
        sw = set(cw)

        # calculate length of word vector
        lw = sqrt(sum(c * c for c in cw.values()))

        # return word vector
        return cw, sw, lw

    # calculate word vectors of given words
    v1, v2 = __vectorize(word1), __vectorize(word2)

    # return cosine distance
    try:
        return sum(v1[0][ch] * v2[0][ch] for ch in v1[1].intersection(v2[1])) / v1[2] / v2[2]
    except ZeroDivisionError:
        return 0.0


def tf_idf(tokens: [], search_term: str, min_similarity=None) -> float:
    """ return the term frequency of a given search word in a list of tokens """

    # define minimum similarity if undefined
    min_similarity = 0.8 if (min_similarity is None or min_similarity > 1 or min_similarity <= 0) else min_similarity

    # get occurrence of max occurring token in tokens
    unique_terms = Counter(tokens)
    max_occurrence = max(unique_terms.values())

    # tokenize search word
    search_tokens = []
    [search_tokens.append(token) for token in re.split(f'[%s%s]' % (punctuation, whitespace), search_term) if
     token != ""]

    # count occurrence of token in tokens that are similar to search_term
    similar = []
    for token in tokens:
        for st in search_tokens:
            if cosine_distance(token, st) >= min_similarity:
                similar.append(token)
    similar = set(similar)
    similar_occurrence = sum(unique_terms[s] for s in similar)

    # return quotient
    return similar_occurrence / max_occurrence
