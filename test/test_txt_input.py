#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: tiago
"""

from termite_toolkit import termite
import os

# specify termite API endpoint
termite_home = "http://localhost:9090/termite"

# input file
parentDir = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))  # this line relatively locates the parent directory
input_file = os.path.join(parentDir, 'sample_scripts/text_sample.txt')  

# TERMite options
options = {"format": "txt", "output": "json", "entities": "DRUG,GENE,INDICATION"}

# TERMite call as JSON result
termite_json_response = termite.annotate_files(termite_home, input_file, options)

filter_entity_types = ['DRUG', 'INDICATION','GENE']

#Because this is tested on a single text file the output should only have 1 row.
#The headers should be docID and filtered_entity_types and respective IDs.
print(termite.termite_entity_hits_df(termite_json_response, filter_entity_types))