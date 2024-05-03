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


        """ Select wordlist source from certain endpoints. """

        # Read from the consumable list to pick up where we left off.
        if arguments.resume is True:
            with open(arguments.disposable_wordlist, "r") as words:
                wordlist = words.readlines()

        # Read from the full list to avoid the overhead of writing our own list.
        else:
            # NOTE: Make sure we dont already have one in memory.
            try:
                if wordlist: pass

            except NameError:
                # NOTE: Check to see if we have our own if not in memory.
                try:
                    with open(arguments.wordlist, "r") as words:
                        wordlist = words.readlines()
                # NOTE: Request one from Github if we dont have our own.
                except:
                    english = EnglishVocabulary()
                    wordlist = english.words



    else:
        lookup = EnglishLanguageAPI(word)
