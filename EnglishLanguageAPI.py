#!/usr/bin/env python
# coding: utf-8

# # English Vocabulary Database Buildup
# The trick to reading the dictionary is locating your word within an easily indexed store of words and scanning 
# their associated definition into your pool of resources; much like it's python counterpart, the structure is a 
# {key:value} store.
# 
# To interpet the dictionary website as a {k:v} dictionary object the English Language API has been written to scrape 
# any given words entry from raw html through it's meta tags.
# 

# ## Module Imports
# 
#   - [Python Logging](#constants-definition): Logging is always useful; and steps should be taken to include it wherever you can.
# 
#   - [Python Requests](#build-query-url): The class object makes a request to a URL similar to ```https://dictionary.com/browse/{_search_tag}```.
# 
#   - [Beautiful Soup](#retrieve-description-from-data): BS4 is used to extract key points from the request data. 

# In[ ]:


import requests
import logging
from bs4 import BeautifulSoup


# ## Constants Definition
# 
#   - Logging : The logfile is set to output to a file, ```./analysis.log```, unless otherwise stated.
# 
#   - Dictionary: An English Language dictionary with a built-in [URL querying system](#build-query-url).

# In[ ]:


logfile = "./analysis.log"
logging.basicConfig(filename=logfile, encoding="utf-8", level=logging.DEBUG)

# English language dictionary with an easily navigable URL schema.

# English language synonyms database, with URL similar to the dictionaries.
englishThesaurus = "https://thesaurus.com"



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

        logging.getLogger()
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

