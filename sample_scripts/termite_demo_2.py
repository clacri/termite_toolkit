"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


Demo script for sending a file to be annotated via the TERMite API, with some post processing of the returned JSON

"""

__author__ = 'SciBite DataScience'
__version__ = '0.2'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

from termite_toolkit import termite
from pprint import pprint

input_file = "fuzzy_sample.txt"
termite_home = "http://localhost:9090/termite"
entities = "INDICATION,CELLTYP,GENE,DRUG"

# build the request
t = termite.TermiteRequestBuilder()
t.set_input_format("txt")
t.set_url(termite_home)
t.set_binary_content(input_file)
t.set_subsume(True)
t.set_entities(entities)
t.set_fuzzy(True)

# make request
result = t.execute(display_request=True)

# do some post-processing
filtered_hits = termite.get_entity_hits_from_json(result, entities, reject_ambig=False)
pprint(filtered_hits)
