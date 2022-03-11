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

    search_word = input("Enter a company your are looking for: ")
