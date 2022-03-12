"""
Library for keeping the user interface small.
Uses naive_library as base for its own functions.
"""

import os
import platform
import naive_library
from colorama import Fore


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


def compare_tf_idf(files: [], search_term: str, min_similarity=None) -> {}:
    """ returns term frequency of search term for all given files """

    # create result dictionary
    results = {}

    # calculate term frequency for search word in each file
    for file in files:
        tokens = naive_library.tokenize(file)
        results.update({file: naive_library.tf_idf(tokens, search_term, min_similarity)})

    return results


def compare_tf_idf_all(files: [], search_term: str, min_similarity=None) -> {}:
    """ returns term frequency of search term for all given files combined """

    # create result dictionary
    results = {}

    # create pool of tokens
    tokens = []
    for file in files:
        text_tokens = naive_library.tokenize(file)
        [tokens.append(tt) for tt in text_tokens]

    # calculate term frequency for search word in each file
    for file in files:
        results.update({file: naive_library.tf_idf(tokens, search_term, min_similarity)})

    return results
