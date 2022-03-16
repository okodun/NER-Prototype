"""
Library for keeping the user interface small.
Uses naive_library as base for its own functions.
"""

import os
import platform
import naive_library
from colorama import Fore
import re
from math import log2
from string import punctuation, whitespace
from spacy_library import SpacyModel


class BoldText:
    """ class contains constants for bold text """
    START = '\033[1m'
    END = '\033[0m'


class ErrorText:
    """ class contains constants for colored error text """
    START = Fore.RED
    END = Fore.RESET


def check_path(path: str) -> []:
    """ returns text files in a given directory or only the file if the path points to only a text file """

    # format given path
    home_dir = os.path.expanduser("~")
    path = path.replace("~", home_dir)

    # find text files
    entries = []
    if os.path.isdir(path):
        # path format for different platforms
        if platform.system() == "Windows":  # Windows path format
            path = path + "\\" if path[-1:] != "\\" else path
        else:  # Unix/Linux path format
            path = path + "/" if path[-1:] != "/" else path
        [entries.append(path + entry) for entry in os.listdir(path) if
         os.path.isfile(path + entry) and entry[-4:] == ".txt"]
    elif os.path.isfile(path) and path[-4:] == ".txt":
        entries.append(path)
    else:
        return None

    # return entries or None if nothing was found
    if len(entries) != 0:
        return entries
    else:
        return None


def get_term_frequency(files: [], search_term: str, min_similarity=None) -> {}:
    """ returns term frequency of a search term for each given file """

    # define default minimum similarity if undefined
    min_similarity = 0.8 if min_similarity is None or min_similarity <= 0 else min_similarity

    # create result dictionary
    results = {}

    # calculate term frequency for search word in each file
    for file in files:
        tokens = naive_library.tokenize(file)
        results.update({file: naive_library.term_frequency(tokens, search_term, min_similarity)})

    return results


def get_tf_idf(files: [], search_term: str, min_similarity=None) -> {}:
    """ returns term frequency of search term for all given files combined """

    # define default minimum similarity if undefined
    min_similarity = 0.8 if min_similarity is None or min_similarity <= 0 else min_similarity

    def contains(file_tokens: []) -> bool:
        search_tokens = []
        [search_tokens.append(tok) for tok in re.split(f'[%s%s]' % (punctuation, whitespace), search_term) if
         tok != ""]
        for ft in set(file_tokens):
            for st in search_tokens:
                if naive_library.cosine_distance(ft, st) >= min_similarity:
                    return True
        return False

    # create result dictionary
    results = {}

    # create pool of tokens
    tokens = []
    for file in files:
        text_tokens = naive_library.tokenize(file)
        tokens.append(text_tokens)

    # calculate inverse document frequency
    r = 0
    for token in tokens:
        if contains(token):
            r += 1
    n = log2(len(files) / r)

    # calculate term frequency for search word in each file
    term_frequencies = get_term_frequency(files, search_term)
    for tf in term_frequencies:
        results.update({tf: log2(1 + term_frequencies[tf]) * n})

    return results


def get_spacy_similarities(files: [], search_term: str) -> {}:
    """ returns average similarity of tokens compared to search term """

    # create spaCy model
    sm = SpacyModel()

    # calculate average similarity
    results = {}
    for file in files:
        results.update({file: sm.find_similarities(search_term, file)})

    return results


def get_spacy_organizations(files: [], search_term: str, top_n=None) -> {}:
    """ returns similar organizations with spacy """

    # define default number of return values
    top_n = 5 if top_n is None or top_n <= 0 else top_n

    # create spaCy model
    sm = SpacyModel()

    # calculate organizations
    results = {}
    for file in files:
        similar = sm.find_organizations(search_term, file)
        for s in sorted(similar, key=lambda x: similar[x][0], reverse=True)[:top_n]:
            results.update({s: (similar[s][0], similar[s][1])})

    return results
