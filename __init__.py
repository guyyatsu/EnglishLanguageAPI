from EnglishLanguageAPI import *
from createdatabase import *

from argparse import ArgumentParser
from sqlite3 import connect


if __name__ == "__main__":

    arguments = ArgumentParser()


    # Heres a long block of arguments.
    arguments.add_argument("-W", "--word")
    arguments.add_argument("-Db", "--database", action="store_true")
    arguments.add_argument(
        "-Df", "--database-file",
        default="/home/library/dictionary.db"
    )

    arguments = arguments.parse_args()

    database = connect(arguments.database_file)
    cursor = database.cursor()

    
    # TODO: Write out a database.
    if arguments.database:

        create_database(arguments.database_file)

        with open("wordlist.txt", "r") as wordlist:
            wordlist = wordlist.readlines()

        try:

            for word in wordlist:
            
                lookup = EnglishLanguageAPI(word)
                cursor.execute("""
                    INSERT OR IGNORE INTO english(
                        word, definition
                    ) VALUES ( ?, ? );""",
                    (lookup.word, lookup.description)
                )

                database.commit()
          
                wordlist.remove(word)

        except Exception as error:

            with open("wordlist.txt", "w") as words:
                words.write("")

            for word in wordlist: 
                with open("wordlist.txt", "a") as words:
                    words.write(word)
