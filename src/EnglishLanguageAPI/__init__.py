from .API import *

from argparse import ArgumentParser
from sqlite3 import connect


if __name__ == "__main__":

    arguments = ArgumentParser()


    # Heres a long block of arguments.
    arguments.add_argument("-W", "--word")

    arguments.add_argument("-Bw", "--build-wordlist", action="store_true")
    arguments.add_argument("-Dw", "--disposable-wordlist", default="/home/library/disposable-wordlist.txt")
    arguments.add_argument("-Wl", "--wordlist", default="/home/library/50000-wordlist.txt")
    arguments.add_argument("-R", "--resume", action="store_true")
    arguments.add_argument("-Db", "--database", action="store_true", default=False)
    arguments.add_argument("-Lf", "--logfile", default="/home/logs/EnglishLanguageAPI.log")
    arguments.add_argument(
        "-Df", "--database-file",
        default="/home/library/dictionary.db"
    )

    arguments = arguments.parse_args()

    database = connect(arguments.database_file)
    cursor = database.cursor()

    
    if arguments.database:
        
        """ Request a source-file for local use if we need one. """

        # Request 50000 word list from github.
        if arguments.build_wordlist is True:
            english = EnglishVocabulary()
            wordlist = english.words

            with open(arguments.wordlist, "a") as source:
                for word in wordlist:
                    source.write(word)

            
            # Save our change to the database.
            database.commit()
            
            # Remove the word from the MEMORY list.
            wordlist.remove(word)

            """ Remove the word from the INPUT list by overwriting
            the file with the MEMORY list without the word we just wrote.
            """
          
            # Clear the file by overwriting it with nothing.
            with open("wordlist.txt", "w") as words:
                words.write("")
            
            # Re-write file with list we just removed a word from.
            for word in wordlist: 
                with open("wordlist.txt", "a") as words:
                    words.write(word)

    else:
        lookup = EnglishLanguageAPI(word)
