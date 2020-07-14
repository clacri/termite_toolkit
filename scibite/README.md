### Project Description

Python library for making calls to [SciBite](https://www.scibite.com/)'s TERMite, TExpress and DOCstore
The library also enables post-processing of the JSON returned from such requests.

## Install

```
$ pip3 install termite_toolkit
```
Versions listed on [PyPi](https://pypi.org/project/termite-toolkit/)!

## Example call to TERMite

```python
from termite_toolkit import termite
from pprint import pprint


# specify termite API endpoint
termite_home = "http://localhost:9090/termite"

# specify entities to annotate
entities = "DRUG"

# initialise a request builder
t = termite.TermiteRequestBuilder()
# individually add items to your TERMite request
t.set_url(termite_home)
t.set_fuzzy(True)
t.set_text("citrate macrophage colony sildenafil stimulating factor influenza hedgehog")
t.set_entities(entities)
t.set_subsume(True)
t.set_input_format("txt")
t.set_output_format("doc.jsonx")
t.set_reject_ambiguous(False)
t.set_options({'fragmentSize': 20})

# execute the request
termite_response = t.execute(display_request=True)

pprint(termite_response)
```

## Example call to TExpress

```python
from pprint import pprint
from termite_toolkit import texpress

# specify termite API endpoint
termite_home = "http://localhost:9090/termite"
# specify the pattern you wish to search for- this can created in the TERMite UI
pattern = ":(INDICATION):{0,5}:(GENE)"

t = texpress.TexpressRequestBuilder()

# individually add items to your TERMite request
t.set_url(termite_home)
t.set_text("breast cancer brca1")
t.set_subsume(True)
t.set_input_format("txt")
t.set_output_format("json")
t.set_allow_ambiguous(False)
t.set_pattern(pattern)

# execute the request
texpress_response = t.execute(display_request=True)
pprint(texpress_response)
```

## Example call to DOCstore

```python
from termite_toolkit import docstore

# Document co-occurrence of a list of entities
docs = docstore.DocStoreRequestBuilder()
# specify docstore API endpoint and add authentication if necessary
docs.set_url('docstore_address')
docs.set_basic_auth(username='user', password='pw')
# make call to DOCStore
docs_json = docs.get_dcc_docs(['id:GENE$HTT', 'id:GENE$EGFR'], '*', {})
# convert json to df
df = docstore.get_docstore_dcc_df(docs_json)
# print titles of hits
print(df['title'])
```

## License 

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.