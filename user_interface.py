class BoldText:
    """ class contains constants for bold text """
    START = '\033[1m'
    END = '\033[0m'


if __name__ == '__main__':
    print(BoldText.START + "Named Entity Recognition Prototype For Company Names" + BoldText.END)
    search_term = input("Enter a company to search for: ")
