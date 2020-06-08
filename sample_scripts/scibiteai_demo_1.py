"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


Demo script making pre-processing calls to the TERMite toolkit

"""

from termite_toolkit import scibiteai
from termite_toolkit import termite

# specify termite API endpoint
termite_home = "http://localhost:9090/termite"

# specify entities to annotate
entities = "GENE,INDICATION,DRUG,HPO"

# initialise a request builder
t = termite.TermiteRequestBuilder()

# individually add items to your TERMite request
t.set_url(termite_home)
t.set_fuzzy(True)
t.set_text("BRCA1 is associated with breast cancer")
t.set_entities(entities)
t.set_subsume(True)
t.set_input_format("txt")
t.set_output_format("doc.jsonx")

# execute the request
termite_response = t.execute(display_request=True)

# markup takes doc.jsonx output and replaces/augments hits found in your processed documents
# full list of options can be found in the docstring
print('\nmarkup docstring: \n%s' % (scibiteai.markup.__doc__))
print('\nmarkup output:')
print(scibiteai.markup(termite_response, vocabs=entities.split(','), wrap=True))

# text_markup is a minimal version of the above which accepts and returns plain text
# you do not need to TERMite the text before sending it to text_markup
print('\ntext_markup output:')
print(scibiteai.text_markup('Albert was the first in his family to be affected by asthma', 
	vocabs=['INDICATION']))

# replacementDict allows you to define what text you want to be used to replace found entities
# ~NAME~, ~TYPE~ and ~ID~ are special terms that get replaced by data from the TERMite results
print('\ntext_markup with replacementDict output:')
print(scibiteai.text_markup('Albert was the first in his family to be affected by asthma', 
	vocabs=['INDICATION'], 
	replacementDict={'INDICATION':'~NAME~ (~ID~)'}))

# label text as to which characters/words refer to which type of entity for use in NER ML tasks
print('\nlabel output (word level first, then character level:')
print(scibiteai.label(termite_response, vocabs=entities.split(',')))
print(scibiteai.label(termite_response, vocabs=entities.split(','), labelLevel='char'))
