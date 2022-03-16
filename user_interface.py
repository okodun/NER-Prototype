"""
User interface for the prototype.
Contains the program structure.
"""

import ui_library as ui
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
    print("-> Only absolute path format available: C:\\Users\\USERNAME")

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

    # print information for user
    # implement different algorithms
    print("Available algorithms to determine text similarity:")
    print(BoldText.START + "--> cosine distance (c)" + BoldText.END + ": short description bla bla bla...")

    # chose algorithm
    while True:
        search_algorithm = input("Enter your desired search algorithm (default is cosine distance): ")
        if search_algorithm in {"cosine distance", "c", ""}:
            if search_algorithm == "":
                print("Using cosine distance.")
            search_algorithm = "cosine distance"
            print()
            break
        else:
            print(ErrorText.START +
                  "Invalid choice. Please enter one of the above mentioned algorithms!" +
                  ErrorText.END)
            print()

    # get term frequency and print results
    # term frequency with all documents or for each document?
    results = ui.get_term_frequency(files, search_word)
    print(BoldText.START + f'Term Frequency for %s:' % search_word + BoldText.END)
    for result in results:
        print(f'%s: %.2f%%' % (result, results[result]))
