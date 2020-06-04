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
input_file = os.path.join(parentDir, 'sample_scripts/csv_sample.csv')  

# TERMite options. Note we're only targeting the ANALYTE column
options = {"format": "csv", "output": "json", "entities": "GENE",'fieldTarget.GENE': 'ANALYTE'}


# TERMite call as JSON result
termite_json_response = termite.annotate_files(termite_home, input_file, options)

termite.all_entities_df(termite_json_response).to_csv('hitlevel.csv')


filter_entity_types = ['GENE']

#Expected output: A dataframe with headers: docID, GENE and GENE_ID, with 10 rows (1 per input csv row and respective hits )
print(termite.termite_entity_hits_df(termite_json_response, filter_entity_types))