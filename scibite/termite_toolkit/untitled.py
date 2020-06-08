"""

  ____       _ ____  _ _         _____ _____ ____  __  __ _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _| ____|  _ \|  \/  (_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | | |  _| | |_) | |\/| | | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | | |___|  _ <| |  | | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_| |_____|_| \_\_|  |_|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|


Demo script using a SciBite AI client for named entity recognition and relationship extraction.

"""

import scibiteai

# define credentials for SciBite AI (and TERMite if needed)
scibite_ai_credentials = {
	'scibite_ai_addr': '127.0.0.1:8000',
	'scibite_ai_user': None,
	'scibite_ai_pass': None
	}

termite_credentials = {
	'termite_addr': '127.0.0.1:9090',
	'termite_user': None,
	'termite_pass': None
	}

# create a SciBite AI client - credentials can also be specified later
sbclient = SciBiteAIClient(scibite_ai_credentials=scibite_ai_credentials,
	termite_credentials=termite_credentials)

# show the model types available
sbclient.list_model_types()

# show the list of available models of a certain type
sbclient.list_models('relex')

# load a model
sbclient.load_model('ppi-1400')

# predict whether a sentence contains a given relationship
sentence = 'BRCA1 binds to BRCA2'
pred = relex_from_sent('ppi-1400', sentence)
print('Does \'%s\' contain a protein-protein interaction?' % sentence)
print(pred)

# if you try to predict with an unloaded model, it will be loaded automatically
pred = ner_from_sent('gene', sentence)
print(pred)

# you can also use w2v models to get vectors for words...
vec = sbclient.w2v_vector(model='medline_basic', word='lung')

# or to find similar words...
sims = sbclient.w2v_most_similar(model='medline_basic', word='lung')
print('The most similar words to \'lung\' are...', sims)