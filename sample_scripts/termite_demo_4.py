"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


Demo script making calls to the TERMite API and returnign annotations in a dataframe

"""

__author__ = 'SciBite DataScience'
__version__ = '0.2'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

from termite_toolkit import termite

small_input_file = "medline_sample.zip"

# initialise a request builder
t = termite.TermiteRequestBuilder()

# build the request
t.set_binary_content(small_input_file)
t.set_input_format("medline.xml")
t.set_output_format("doc.jsonx")

# make request
termite_multidoc_docjsonx = t.execute(display_request=True)

# load the json returned by TERMite into a dataframe
termite_dataframe = termite.get_termite_dataframe(termite_multidoc_docjsonx)
print(termite_dataframe)

# load the json returned by TERMite into a dataframe, whilst specifying additional columns to be included in the output
termite_dataframe_extended = termite.get_termite_dataframe(termite_multidoc_docjsonx, cols_to_add='kvp,dictSynList')
print(termite_dataframe_extended['kvp'])

# get all the entities from the termite json
print(termite.all_entities(termite_multidoc_docjsonx))

# get all the entities from the termite json in a dataframe#
print(termite.all_entities_df(termite_multidoc_docjsonx))

termite_dataframe = termite.get_termite_dataframe(termite_multidoc_docjsonx)
print(list(termite_dataframe.columns))

# get a list of all the TERMite entity hits
print(termite.entity_freq(termite_multidoc_docjsonx))

# get a list of all the most frequently hit entities
top_hits = termite.top_hits_df(termite_multidoc_docjsonx, entity_subset='GENE,MPATH, SBIO', selection=5,
                               include_docs=True)
print(top_hits)
