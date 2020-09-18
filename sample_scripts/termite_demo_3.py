"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


Demo script making calls via the TERMite API and post-processing, using either files or text

"""

__author__ = 'SciBite DataScience'
__version__ = '0.2'
__copyright__ = '(c) 2019, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'

from pprint import pprint
from termite_toolkit import termite

# specify termite API endpoint
termite_home = "http://localhost:9090/termite"
input_file = "medline_sample.zip"

# running a file through termite
options = {"format": "medline.xml", "output": "json", "entities": "DRUG,GENE"}
termite_json_response = termite.annotate_files(termite_home, input_file, options)
entity_hits = termite.get_entity_hits_from_json(termite_json_response, "DRUG,GENE", score_cutoff=2)
pprint(entity_hits)

# running a list of strings through termite one at a time and post-processing response
text_list = [
    "sildenafil is a drug. sildenafil is a drug. sildenafil is a drug. sildenafil is a drug. sildenafil is a drug",
    "macrophage colony stimulating factor"]
options = {"format": "txt", "output": "json", "entities": "DRUG,GENE"}

for i, text in enumerate(text_list):
    termite_json_response = termite.annotate_text(termite_home, text, options)
    entity_hits = termite.get_entity_hits_from_json(termite_json_response, "DRUG,GENE")
    print("row_" + str(i), ":", entity_hits)

