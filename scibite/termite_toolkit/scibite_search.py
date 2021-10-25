
"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


SearchRequestBuilder- make requests to the Scibite Search API and process results.

"""

__author__ = 'SciBite DataScience'
__version__ = '0.4.5'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

import requests

class SBSRequestBuilder():
    """
    Class for creating TEXpress requests
    """

    def __init__(self):
        self.url = ""
        self.token_url =""
        self.payload = {"output": "json", "method": "texpress"}
        self.options = {}
        self.basic_auth = ()
        self.verify_request = True
    
    def set_oauth2(self,client_id,username,password, verification = True):
        """Pass username and password for the Scibite Search token api
        It then uses these credentials to generate an access token and adds 
        this to the request header.
        :client_id: client_id to access the token api
        :username: scibite search username
        :password: scibite search password for username above
        """
        if self.token_url !="":
            token_address = self.token_url+"/auth/realms/Scibite/protocol/openid-connect/token"
        else:
            token_address = self.url+"/auth/realms/Scibite/protocol/openid-connect/token"
		
        req = requests.post(token_address, data= {"grant_type": "password","client_id":client_id,"username":username, "password":password}, 
            headers = {"Content-Type": "application/x-www-form-urlencoded"})
        access_token = req.json()["access_token"]
        self.headers = {"Authorization": "Bearer "+ access_token}
        self.verify_request = verification
        
    def set_token_url(self, token_url):
        """Set the URL for the token API
        :token_url: the URL for the token API
        """
        self.token_url = token_url.rstrip('/')
		
    def set_url(self, url):
        """
        Set the URL of the Scibite Search instance
        :url: the URL of the Scibite Search instance to be hit
        """
        self.url = url.rstrip('/')
        
    def get_docs(self,query ='',markup=True, limit = 20,offset = 0):
        """This endpoint allows searching and retrieval of documents. 
		:query: SSQL query
		:markup: Whether annotated text should markup the entities
		:limit: Limits the number of results
		:offset: The number of resources to skip before returning results. Used for implementing paging.
		"""
        options ={"markup":markup,"limit":limit, "offset":offset}
        if query:
            options["queries"]=query

        req = requests.get(self.url+"/api/search/v1/documents/",params = options, headers = self.headers)
        return req.json()
	
    def get_sentences(self,query='',markup =True, limit =20, offset =0):
        """This endpoint allows searching and retrieval of the sentences in the documents. 
		:query: SSQL query
		:markup: Whether annotated text should markup the entities\
		:limit: Limits the number of results
		:offset: The number of resources to skip before returning results. Used for implementing paging.
		"""
        options ={"markup":markup,"limit":limit, "offset":offset}
        if query:
            options["queries"]=query

        req = requests.get(self.url+"/api/search/v1/sentences/",params = options, headers = self.headers)
        return req.json()

    def entity_mentions (self,text):
        """This endpoint annotates a text string with termite annotations.
        Efectively it works as an API endpoint"""
        options = {"text":text}
        req = requests.get(self.url+"/jobserver/v1/entitymentions", params = options,headers = self.headers)
        return req.json()

    def document_schemas (self,json_body):
        """This endpoint posts a new document schema to a ScibiteSearch instance"""
        headers = self.headers
        headers['Content-type']='application/json' 
        requests.post(self.url+ '/api/search/v1/document-schemas', json = json_body,headers = headers)

        