"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


Utility functions- including autocomplete

"""

__author__ = 'SciBite DataScience'
__version__ = '0.4.5'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

import requests


class UtilitiesRequestBuilder():
    """
    Class for creating utility requests
    """

    def __init__(self):
        self.url = 'http://localhost:9090/termite'
        self.basic_auth = ()
        self.verify_request = True

    def set_url(self, url):
        """
        Set the URL of the TERMite instance e.g. for local instance http://localhost:9090/termite/toolkit/autocomplete.api

        :param url: the URL of the TERMite instance to be hit
        """
        self.url = url.rstrip('/')

    def set_basic_auth(self, username='', password='', verification=True):
        """
        Pass basic authentication credentials.
        ** ONLY change verification if you are calling a known source **

        :param username: username to be used for basic authentication
        :param password: password to be used for basic authentication
        """
        self.basic_auth = (username, password)
        self.verify_request = verification

    def call_autocomplete(self, input, vocab, taxon=''):
        """
        Complete a call to the auto complete API

        :param input: input string
        :param vocab: vocabs to limit ac too
        :param taxon: taxon to limit ac too
        """

        if len(input) < 3:
            return 'Please provide a string longer than 3 chars..'
        response = requests.post(("%s/toolkit/autocomplete.api" % self.url),
                                 data={"term": input, "e": vocab, "limit": taxon})

        if response.ok:
            ac_json = response.json()
            return ac_json

        else:
            return response.status_code

    def get_entity(self, entity_id, entity_type):
        """
        Entity lookup function, given and entity type (e.g. GENE, INDICATION) and entity ID (e.g. CSF1, D010024)
        creates and runs GET call of the format: http://localhost:9090/termite/toolkit/tool.api?t=describe&id=INDICATION:D001249

        :param entity_id: id of entity of interest
        :param entity_type: type of entity of interest
        :return: request response
        """
        url = ("%s/toolkit/tool.api?t=describe&id=%s:%s" % (self.url, entity_type, entity_id))
        response = requests.get(url)

        if response.ok:
            entity_json = response.json()
            return entity_json

        else:
            return response.status_code

    def get_entity_details(self, entity_id, entity_type):
        """
        Returns a subset of metadata from the get_entity result: ID, name, mappings to external IDs

        :param entity_id: id of entity of interest
        :param entity_type: type of entity of interest
        :return: entity details
        """
        details = {"id": entity_id, "type": entity_type, "name": "", "mappings": []}
        entity_meta = self.get_entity(entity_id, entity_type)
        if len(entity_meta["TOOL_RESULT"]) > 0:
            e = entity_meta["TOOL_RESULT"][0]
            details["name"] = e["name"]
            if "mappings" in e:
                mappings = e["mappings"]
                for m in mappings:
                    items = m.split('|')
                    details["mappings"].append(items)

        return details
