"""
  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

Preprocessing functions- using your TERMite output to make AI-ready data

"""

__author__ = 'SciBite DataScience'
__version__ = '0.3'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

import requests
import pandas as pd


class DocStoreRequestBuilder():
    """
    Class for creating DOCStore requests
    """

    def __init__(self):
        self.url = "https://tyrion.scibite.com:9999"
        self.input_file_path = ''
        self.payload = {"output": "json"}
        self.options = {}
        self.binary_content = None
        self.basic_auth = ()
        self.verify_request = True

    def set_basic_auth(self, username='', password='', verification=True):
        """
        Pass basic authentication credentials
        **ONLY change verification if you are calling a known source**
        :param username: username to be used for basic authentication
        :param password: password to be used for basic authentication
        :param verification: if set to False requests will ignore verifying the SSL certificate, can also pass the path
        to a certificate file
        """
        self.basic_auth = (username, password)
        self.verify_request = verification

    def set_url(self, url):
        """
        Set the URL of the DOCStore instance e.g. for local instance http://localhost:9090/termite
        :param url: the URL of the DOCStore instance to be hit
        """
        self.url = url

    def get_dcc_docs(self, entity_list, source, options_dict):
        """
        Retrieve document co-occurrence of provided entities
        :param entity_list: list of entities to be searched for
        :param source: name of data source(s) to be searched against
        :param options_dict: search parameters
        :return: results of search in json format
        """
        base_url = self.url
        query_url = (base_url) + "/api/ds/v1/search/co/document/{}/*/*/*".format(source)
        entity_string = " ".join(entity_list)

        options = {"fmt": "json",
                   "fields": "*",
                   "terms": entity_string,
                   "limit": "10",
                   "from": "0",
                   "facettype": "NONE",
                   "significantTerms": "false",
                   "excludehits": "false",
                   "sortby": "document_date:desc",
                   }

        try:
            for k, v in options_dict.items():
                if k in options.keys():
                    options[k] = v
        except:
            pass

        response = requests.get(query_url, params=options, verify=False)
        resp_json = response.json()

        return resp_json

    def get_boolean_docs(self, query_string, source, options_dict):
        """
        Retrieve document co-occurrence of provided entities
        :param query_string: query to be completed
        :param source: name of data source(s) to be searched against
        :param options_dict: search parameters
        :return: results of search in json format
        """
        base_url = self.url
        query_url = (base_url) + "/api/ds/v1/search/document/{}/*/*/*".format(source)

        options = {"fmt": "json",
                   "fields": "*",
                   "query": query_string,
                   "limit": "10",
                   "from": "0",
                   "facettype": "NONE",
                   "significantTerms": "false",
                   "excludehits": "false",
                   "sortby": "document_date:desc",
                   "filters": ""
                   }

        try:
            for k, v in options_dict.items():
                if k in options.keys():
                    options[k] = v
        except:
            pass

        response = requests.get(query_url, params=options, verify=False)
        resp_json = response.json()

        return resp_json

    def get_scc_docs(self, entity_list, source, options_dict):
        """
        Retrieve sentence co-occurrence of provided entities
        :param entity_list: list of entities to be searched for
        :param source: name of data source(s) to be searched against
        :param options_dict: search parameters
        :return: results of search in json format
        """
        base_url = self.url
        query_url = (base_url) + "/api/ds/v1/search/co/sentence/sentencedetail/flat/{}/*/*/*".format(
            source)
        entity_string = " ".join(entity_list)

        options = {"fmt": "json",
                   "fields": "*",
                   "terms": entity_string,
                   "inorder": "false",
                   "slop": "2",
                   "limit": "10",
                   "from": "0",
                   "sortby": "document_date:desc",
                   "zip": "false"}

        try:
            for k, v in options_dict.items():
                if k in options.keys():
                    options[k] = v
        except:
            pass

        response = requests.get(query_url, params=options, verify=False)  # May need to add authentication details here
        resp_json = response.json()

        return resp_json


def get_docstore_dcc_df(json):
    """
    Converts document co-occurrence json into a dataframe
    :param json: dcc json
    :return: dcc dataframe
    """
    df_rows = []
    hits = json["hits"]

    for h in hits:
        hit_dict = {}

        # Document id
        doc_id = h["id"]

        # Document date
        doc_date = (h["documentDate"])[0:10]

        # Title
        highlighted_sections = (h['highlightedSections'])[0]
        title_words = highlighted_sections['titleWords']

        title_list = []

        for t in title_words:
            word = (t['p']).rstrip()
            title_list.append(word)

        title = ((' ').join(title_list))

        # Authors
        authors = ""
        try:
            authors = h["authors"]
        except:
            pass

        # Citation
        citation = h["citation"]

        hit_dict.update([("document_id", doc_id), ("document_date", doc_date), ("title", title),
                         ("authors", authors), ("citation", citation)])
        df_rows.append(hit_dict)

    dcc_df = pd.DataFrame(df_rows)
    return (dcc_df)


def get_docstore_scc_df(json):
    """
     Converts sentence co-occurrence json into a dataframe
     :param json: scc json
     :return: scc dataframe
     """
    df_rows = []
    hits = json["hits"]

    for h in df_rows:
        hit_dict = {}

        # Document id
        doc_id = h["docId"]

        # Document date
        doc_date = (h["docDate"])[0:10]

        # SCC Sentence
        doc_sent = h["sentence"]

        hit_dict.update([("document_id", doc_id), ("document_date", doc_date), ("scc_sentence", doc_sent)])
        df_rows.append(hit_dict)

    scc_df = pd.DataFrame(df_rows, columns=["document_id", "document_date", "scc_sentence"])
    return (scc_df)
