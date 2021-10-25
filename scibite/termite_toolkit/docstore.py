"""
  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

Preprocessing functions- using your TERMite output to make AI-ready data

"""

__author__ = 'SciBite DataScience'
__version__ = '0.4.5'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

import requests
import pandas as pd


class DocStoreRequestBuilder():
    """
    Class for creating DOCStore requests
    """

    def __init__(self):
        self.url = ""
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
        Set the URL of the DOCStore instance
        :param url: the URL of the DOCStore instance to be hit
        """
        self.url = url.rstrip('/')

    def get_dcc_docs(self, entity_list, source='*', options_dict=None):
        """
        - Document co-occurrence - 
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

        response = requests.get(query_url, params=options, auth=self.basic_auth)

        resp_json = response.json()
        

        return resp_json

    def get_boolean_docs(self, query_string, source='*', options_dict=None):
        """
        - Document-level query of Doc Store - 
        Document-level query of Doc Store, produced both hit and facet data
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

        response = requests.get(query_url, params=options, auth=self.basic_auth)
        resp_json = response.json()

        return resp_json

    def get_docs(self, query_string, source='*', options_dict=None):
        """
        - Document-level query of Doc Store, returning only the documents hit, 
        no facet data. -
        The output is TERMite/TEXpress ready
        :param query_string: query to be completed
        :param source: name of data source(s) to be searched against
        :param options_dict: search parameters
        :return: results of search in json format
        """
        base_url = self.url
        query_url = (base_url) + '/api/ds/v1/search/document/docs/{}/*/*/*'.format(source)  
        options = {"fields": "*",
                   "fmt":"json",
                   "query": query_string,
                   "limit": "10",
                   "from": "0",
                   "sortby": "document_date:desc",
                   "filters": "",
                   "zip":"false",
                   "metaonly":"false"
                   }

        try:
            for k, v in options_dict.items():
                if k in options.keys():
                    options[k] = v
        except:
            pass

        response = requests.get(query_url, params=options, auth=self.basic_auth)
        resp_json = response.json()
        return resp_json

    def get_scc_docs(self, entity_list, source='*', options_dict=None):
        """
        - Sentence co-occurrence on entity ids or types, returns documents 
        containing sentences fulfilling the co-occurrence. - 
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

        response = requests.get(query_url, params=options, auth=self.basic_auth)
        resp_json = response.json()

        return resp_json
    
    def get_doc_by_id(self,doc_id, fmt='json'):
        """Retrieves document by its unique ID"""
        options = {"fmt": fmt,
                   "uid":doc_id}
        base_url = self.url
        query_url = (base_url) + "/api/ds/v1/lookup/doc"
        response = requests.get(query_url, params=options, auth=self.basic_auth)
        resp_json = response.json()
        return resp_json
    
    def entity_lookup_id(self, syn, entity_type, options_dict=None):
        """Lookup IDs for a synonym and type"""
        options = {"syn": syn,
                   "type":entity_type}
        base_url = self.url
        query_url = (base_url) + "/api/entity/v1/lookup/id"
        response = requests.get(query_url, params=options, auth=self.basic_auth)
        resp_json = response.json()
        return resp_json
    def get_facets_only(self,query_string,facetFilter, source ='*', significantTerms = False, options_dict = None):
        """Document-level query of Doc Store, returning only the facets"""
        options ={"fmt": "json",
                   "fields": "*",
                   "query": query_string,
                   "facetFilter":facetFilter,
                   "limit": "10",
                   "from": "0",
                   "facettype": "BY_TYPE",
                   "significantTerms": "false",
                   "excludehits": "false",
                   }
        try:
            for k, v in options_dict.items():
                if k in options.keys():
                    options[k] = v
        except:
            pass
        base_url = self.url
        query_url = (base_url) + '/api/ds/v1/search/document/facets/{}/*/*/*'.format(source)  
        response = requests.get(query_url, params=options, auth=self.basic_auth)
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
        doc_date = ""
        try:
            doc_date = h["documentDate"][0:10]
        except:
            pass
        # Title
        highlighted_sections = h['highlightedSections'][0]
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
        citation = ""
        try:
            citation = h["citation"]
        except:
            pass
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

    for h in hits:
        hit_dict = {}

        # Document id
        doc_id = h["docId"]

        # Document date
        doc_date = ""
        try:
            doc_date = h["docDate"][0:10]
        except:
            pass

        # SCC Sentence
        doc_sent = h["sentence"]

        hit_dict.update([("document_id", doc_id), ("document_date", doc_date), ("scc_sentence", doc_sent)])
        df_rows.append(hit_dict)

    scc_df = pd.DataFrame(df_rows, columns=["document_id", "document_date", "scc_sentence"])
    return (scc_df)


