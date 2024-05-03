#!/usr/bin/env python
import requests
import logging
from bs4 import BeautifulSoup


class EnglishLanguageAPI:
    """
    The EnglishLanguageAPI class accepts a single word and searches
    the dictionary for a matching description.
    """

    def __init__(self, word, dictionary=True):
        """
        The searchTag is a callers search request given as a
        raw text string which is then formatted to the dictionary.com
        built-in api standards.  By default the search tag is compared
        against the thesaurus unless explicitly told to check the dictionary.
        """

        logging.getLogger(__name__)
        base_url = "https://dictionary.com/browse"


        # TODO: Handle multiple words.
        self.word = word.split()[0]\
                        .lower()

        request_url = f"{base_url}/{self.word.lower()}"

        logging.info(f"Requesting definition for: {self.word}")
        page = BeautifulSoup(
            requests.get(request_url)\
                    .content,
            "html.parser"
        )


        description = \
            page.find("meta", {"name": "description"})\
                .get("content")

        description = description.replace(f"{self.word.title()} definition: ", "")
        description = description.replace(" See more.", "")
        description = description.replace("..", ".")
        description = " ".join(description.split(".")[0:-2])

        self.description = f"{description.capitalize()}."

