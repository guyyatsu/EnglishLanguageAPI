from EnglishLanguageAPI import *

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

    
    if arguments.database:

        # Read the list of words into memory.
        with open("wordlist.txt", "r") as wordlist:
            words = wordlist.readlines(); wordlist = words


        """ Make the dictionary query to define a word; then
        record both the word and its definition to a database.
        """
        for word in wordlist:

            # Request the definition of a word;
            lookup = EnglishLanguageAPI(word)
            
            # Record it to the english table;
            cursor.execute("""
                INSERT OR IGNORE INTO english(
                    word, definition
                ) VALUES ( ?, ? );""",
                (lookup.word, lookup.description)
            )
            
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
