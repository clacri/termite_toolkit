"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


Demo script making calls with text to the DOCStore API

"""

__author__ = 'SciBite DataScience'
__version__ = '0.2'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

from termite_toolkit import docstore

# replace with a docstore instance
docstore_url = 'https://datascience.scibite.com:9090'
# fill with login details if required
user = 'scibite_admin'
pw= 'weP3vw4ho9ihJka'

#######
# Document-level query of Doc Store
docs = docstore.DocStoreRequestBuilder()
# specify docstore API endpoint and add authentication if necessary
docs.set_url(docstore_url)
docs.set_basic_auth(username=user, password=pw)
# make call to DOCStore Document-level query API
docs_json = docs.get_docs(['id:GENE$HTT', 'id:GENE$EGFR'])
# print unique id of the first hit
uid = docs_json['hits'][0]['uid']
print (uid)

#######
# Retrieve document by id
docs = docstore.DocStoreRequestBuilder()
# specify docstore API endpoint and add authentication if necessary
docs.set_url(docstore_url)
docs.set_basic_auth(username=user, password=pw)
# make call to document lookup by ID API (using the uid of the previous query)
docs_jon = docs.get_doc_by_id(uid)
# print the authors of the document hit
print (docs_json['hits'][0]['authors'])

#######
# Document co-occurrence of a list of entities
docs = docstore.DocStoreRequestBuilder()
# specify docstore API endpoint and add authentication if necessary
docs.set_url(docstore_url)
docs.set_basic_auth(username=user, password=pw)
# make call to DOCStore Document co-occurence API
docs_json = docs.get_dcc_docs(['id:GENE$HTT', 'id:GENE$EGFR'])
# convert json to df
df = docstore.get_docstore_dcc_df(docs_json)
# print titles of hits
print(df['title'])

#######
# Sentence co-occurrence of a list of entities
docs = docstore.DocStoreRequestBuilder()
# specify docstore API endpoint and add authentication if necessary
docs.set_url(docstore_url)
docs.set_basic_auth(username=user, password=pw)
# make call to DOCStore sentence co-occurence API
docs_json = docs.get_scc_docs(['id:GENE$HTT', 'id:GENE$EGFR'])
# convert json to df
df = docstore.get_docstore_scc_df(docs_json)
# print doc_ids of hits
print(df['document_id'])


#######
# Lookup entity synonyms
docs = docstore.DocStoreRequestBuilder()
# specify docstore API endpoint and add authentication if necessary
docs.set_url(docstore_url)
docs.set_basic_auth(username=user, password=pw)
# returns json with list of synonyms and their IDs
synonym = 'BRCA1'
entity_type = 'GENE'
print(docs.entity_lookup_id(synonym,entity_type))
