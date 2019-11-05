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


#######
# Document co-occurrence of a list of entities
docs = docstore.DocStoreRequestBuilder()
# make call to DOCStore
docs_json = docs.get_dcc_docs(['id:GENE$HTT', 'id:GENE$EGFR'], '*', {})
# convert json to df
df = docstore.get_docstore_dcc_df(docs_json)
# print titles of hits
print(df['title'])


#######
# Sentence co-occurrence of a list of entities
docs = docstore.DocStoreRequestBuilder()
# make call to DOCStore
docs_json = docs.get_scc_docs(['id:GENE$HTT', 'id:GENE$EGFR'], '*', {})
# convert json to df
df = docstore.get_docstore_scc_df(docs_json)
# print doc_ids of hits
print(df['document_id'])
