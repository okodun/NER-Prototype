"""
User interface for the prototype.
Contains the program structure.
Implements currently only functionality for determining similar organizations.


Created by Mert Caliskan (22442138) and Felix Schuhmann (22749060).
"""

import ui_library as ui
import warnings
from ui_library import BoldText, ErrorText

if __name__ == '__main__':
    # print title
    print(BoldText.START + "Named Entity Recognition Prototype For Company Names" + BoldText.END)
    print()

    # print information for user
    print(BoldText.START + "Unix, Linux and other *nix distributions" + BoldText.END)
    print("-> Format for absolute path: /home/USERNAME/DIRECTORY")
    print("-> Format for relative path: ~/DIRECTORY")
    print(BoldText.START + "Windows" + BoldText.END)
    print("-> Only absolute path format available: C:\\Users\\USERNAME\\DIR")

    # get files
    while True:
        path = input("Enter a path to a file or directory which contains the text(s) to be searched: ")
        files = ui.check_path(path)
        if files is not None:
            print()
            break
        print(ErrorText.START +
              "Error occurred. Either path is invalid or directory does not contain any .txt files!" +
              ErrorText.END)
        print()

    # print found files
    print(BoldText.START + "Following files were found:" + BoldText.END)
    for file in files:
        print(file)
    print()

    # get search word
    while True:
        search_word = input("Enter a company your are looking for: ")
        if search_word != "":
            print()
            break
        print(ErrorText.START + "Please enter a search word!" + ErrorText.END)
        print()

    # print information for user (other algorithms could be implemented here)
    print("Currently available algorithms to determine text similarity:")
    print(BoldText.START + "--> most similar named entities (ner)" + BoldText.END)

    # chose algorithm
    while True:
        search_algorithm = input("Enter your desired search algorithm (default is ner): ")
        if search_algorithm in {"most similar named entities", "ner", ""}:
            if search_algorithm == "":
                print("Using ner.")
            print()
            break
        else:
            print(ErrorText.START +
                  "Invalid choice. Please enter one of the above mentioned algorithms!" +
                  ErrorText.END)
            print()

    # find most similar organizations and print result
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        results = ui.get_spacy_organizations(files, search_word)
        print(BoldText.START + f'Following named entities were found for %s:' % search_word + BoldText.END)
        for result in results:
            print(" " + result)
            for r in results[result]:
                print(" ", r, ":", results[result][r][0])
            print()
    print(BoldText.START + "Values closer to 1 are more similar to the searched company." + BoldText.END)
