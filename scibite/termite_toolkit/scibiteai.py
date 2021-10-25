"""
  ____       _ ____  _ _         _____           _ _    _ _
 / ___|  ___(_) __ )(_) |_ ___  |_   _|__   ___ | | | _(_) |_
 \___ \ / __| |  _ \| | __/ _ \   | |/ _ \ / _ \| | |/ / | __|
  ___) | (__| | |_) | | ||  __/   | | (_) | (_) | |   <| | |_
 |____/ \___|_|____/|_|\__\___|   |_|\___/ \___/|_|_|\_\_|\__|

AI functions- using your TERMite output to make AI-ready data, and using the SciBite AI api to
generate insights.

"""


__author__ = 'SciBite AI'
__version__ = '0.4.5'
__copyright__ = '(c) 2020, SciBite Ltd'
__license__ = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'


import json
import os
import requests
import nltk.data
from requests.auth import HTTPBasicAuth
import termite_toolkit.termite as termite


scibite_ai_credentials = {
	'scibite_ai_addr': None,
	'scibite_ai_user': None,
	'scibite_ai_pass': None
	}

termite_credentials = {
	'termite_addr': None,
	'termite_user': None,
	'termite_pass': None
	}

docstore_credentials = {
	'docstore_addr': None,
	'docstore_user': None,
	'docstore_pass': None
	}


class SciBiteAIClient():
	def __init__(self, scibite_ai_credentials=scibite_ai_credentials, 
		termite_credentials=termite_credentials, docstore_credentials=docstore_credentials):

		self.scibite_ai_credentials = scibite_ai_credentials
		self.termite_credentials = termite_credentials
		self.docstore_credentials = docstore_credentials
		self.models = None
		self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

		if scibite_ai_credentials['scibite_ai_addr']:
			self.populate_models_dict()


	###
	#Core functionality
	###


	def populate_models_dict(self, scibite_ai_addr=None, scibite_ai_user=None, 
		scibite_ai_pass=None):
		'''
		Populate a dictionary with models, descriptions and loaded statuses

		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		self.models = {}

		typeList = self.list_model_types()['results']
		for type_ in typeList:
			models = self.list_models(type_)
			self.models[type_] = models['results']


	def set_scibite_ai_credentials(self, scibite_ai_addr, scibite_ai_user=None, 
		scibite_ai_pass=None):
		'''
		Set credentials for the SciBite AI server.

		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr
		if scibite_ai_user:
			scibite_ai_credentials['scibite_ai_user'] = scibite_ai_user
		if scibite_ai_pass:
			scibite_ai_credentials['scibite_ai_pass'] = scibite_ai_pass


	def set_termite_credentials(self, termite_addr, termite_user=None, termite_pass=None):
		'''
		Set credentials for the TERMite server.

		:param string termite_addr: Address for the TERMite server (e.g. 127.0.0.1:9090)
		:param string termite_user: Username for the TERMite server http (if required)
		:param string termite_pass: Password for the TERMite server http (if required)
		'''

		termite_credentials['termite_addr'] = termite_addr
		if termite_user:
			termite_credentials['termite_user'] = termite_user
		if termite_pass:
			termite_credentials['termite_pass'] = termite_pass


	def set_docstore_credentials(self, docstore_addr, docstore_user=None, docstore_pass=None):
		'''
		Set credentials for the DOCstore server

		:param string docstore_addr: Address for the DOCstore server (e.g. 127.0.0.1:8000)
		:param string docstore_user: Username for the DOCstore server http (if required)
		:param string docstore_pass: Password for the DOCstore server http (if required)
		'''

		self.docstore_credentials['docstore_addr'] = docstore_addr
		if docstore_user:
			self.docstore_credentials['docstore_user'] = docstore_user
		if docstore_pass:
			self.docstore_credentials['docstore_pass'] = docstore_pass


	###
	#Models functionality
	###


	def list_model_types(self, scibite_ai_addr=None, scibite_ai_user=None, scibite_ai_pass=None):
		'''
		List the broad categories of models supported by the SciBite AI platform.

		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if scibite_ai_addr.endswith('/api'):
			req = '/models'
		else:
			req = '/api/models'

		if not scibite_ai_user:
			print ('http://' + scibite_ai_addr + req)
			r = requests.get('http://' + scibite_ai_addr + req)

		else:
			print('Shouldnt get here...')
			r = requests.get('https://' + scibite_ai_addr + req, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))


		j = json.loads(r.text)

		return j


	def list_models(self, type_, scibite_ai_addr=None, scibite_ai_user=None, scibite_ai_pass=None):
		'''
		List models of a specific type.
		
		:param string type_: The category of models you would like to list (e.g. 'ner')
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if scibite_ai_addr.endswith('/api'):
			req = '/models/%s' % type_	
		elif scibite_ai_addr.endswith('/models'):
			req = '/%s' % type_	
		elif scibite_ai_addr.endswith('/%s' % type_):
			req = ''
		else:
			req = '/api/models/%s' % type_

		if not scibite_ai_user:
			r = requests.get('http://' + scibite_ai_addr + req)
		else:
			r = requests.get('https://' + scibite_ai_addr + req, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		j = json.loads(r.text)

		return j


	def load_model(self, type_, model, scibite_ai_addr=None, scibite_ai_user=None, 
		scibite_ai_pass=None):
		'''
		Load a specific model of a specific type.
		
		:param string type_: The category of the model you would like to load
		:param string model: The specific name of the model you would like to load
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if scibite_ai_addr.endswith('/api'):
			req = '/models/%s/load' % type_
		elif scibite_ai_addr.endswith('/models'):
			req = '/%s/load' % type_	
		elif scibite_ai_addr.endswith('/%s' % type_):
			req = '/load'
		elif scibite_ai_addr.endswith('/%s' % model):
			req = ''
		else:
			req = '/api/models/%s/load' % type_

		data = {'model': model}

		if not scibite_ai_user:
			r = requests.post('http://' + scibite_ai_addr + req, data=data)
		else:
			r = requests.post('https://' + scibite_ai_addr + req, data=data,
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		j = json.loads(r.text)

		return j


	def unload_model(self, type_, model, scibite_ai_addr=None, scibite_ai_user=None, 
		scibite_ai_pass=None):
		'''
		Unload a specific model of a specific type.

		:param string type_: The category of the model you would like to unload
		:param string model: The specific name of the model you would like to unload
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if scibite_ai_addr.endswith('/api'):
			req = '/models/%s/unload' % type_
		elif scibite_ai_addr.endswith('/models'):
			req = '/%s/unload' % type_	
		elif scibite_ai_addr.endswith('/%s' % type_):
			req = '/unload'
		elif scibite_ai_addr.endswith('/%s' % model):
			req = ''
		else:
			req = '/api/models/%s/unload' % type_

		data = {'model': model}

		if not scibite_ai_user:
			r = requests.post('http://' + scibite_ai_addr + req, data=data)
		else:
			r = requests.post('https://' + scibite_ai_addr + req, data=data,
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		return j


	###
	#RE functionality
	###


	def relex_from_sent(self, model, sent, scibite_ai_addr=None, scibite_ai_user=None, 
		scibite_ai_pass=None, termite_addr=None, termite_user=None, termite_pass=None, split_paragraphs = 'false'):
		'''
		Pass a sentence within which you would like to identify a relationship using a specific 
		model.

		:param string model: The model trained to identify your relationship of interest
		:param string sent: The sentence you wish to assess for your relationship of interest
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		:param string termite_addr: Address for the TERMite server (e.g. 127.0.0.1:9090)
		:param string termite_user: Username for the TERMite server http (if required)
		:param string termite_pass: Password for the TERMite server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr
		if not termite_addr:
			termite_addr = self.termite_credentials['termite_addr']
			termite_user = self.termite_credentials['termite_user']
			termite_pass = self.termite_credentials['termite_pass']
		if not self.models:
			self.populate_models_dict()

		if self.models['relex'][model]['loaded'] == 'False':
			self.load_model('relex', model)

		if scibite_ai_addr.endswith('/api'):
			req = '/relex/predict_sentences'
		elif scibite_ai_addr.endswith('/relex'):
			req = '/predict_sentences'
		elif scibite_ai_addr.endswith('/predict_sentences'):
			req = ''
		else:
			req = '/api/relex/predict_sentences'

		data = {'model': model, 'sentences': sent, 'split_paragraphs' :split_paragraphs}

		if termite_addr:
			data['termite_url'] = termite_addr
		if termite_user:
			data['termite_http_user'] = termite_user
			data['termite_http_pass'] = termite_pass

		if not scibite_ai_user:
			r = requests.get('http://' + scibite_ai_addr + req, params=data)
		else:
			r = requests.get('https://' + scibite_ai_addr + req, params=data, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))
		j = json.loads(r.text)['results']
		j['sentence'] = sent

		return j


	def relex_from_doc(self, model, document, doctype=None, scibite_ai_addr=None, 
		scibite_ai_user=None, scibite_ai_pass=None, termite_addr=None, termite_user=None, 
		termite_pass=None, return_negatives=False):
		'''
		Pass a document within which you would like to identify sentences containing relationships 
		using a specific model.

		:param string model: The model trained to identify your relationship of interest
		:param string document: The filepath of the document you wish to search for your 
		relationship of interest
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		:param string termite_addr: Address for the TERMite server (e.g. 127.0.0.1:9090)
		:param string termite_user: Username for the TERMite server http (if required)
		:param string termite_pass: Password for the TERMite server http (if required)
		:param bool return_negatives: Set to True if you wish to have sentences with no
		relationship identified returned with your results
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr
		if not termite_addr:
			termite_addr = self.termite_credentials['termite_addr']
			termite_user = self.termite_credentials['termite_user']
			termite_pass = self.termite_credentials['termite_pass']
		if not self.models:
			self.populate_models_dict()

		if self.models['relex'][model]['loaded'] == 'False':
			self.load_model('relex', model)

		if scibite_ai_addr.endswith('/api'):
			req = '/relex/predict_file'
		elif scibite_ai_addr.endswith('/relex'):
			req = '/predict_file'
		elif scibite_ai_addr.endswith('/predict_file'):
			req = ''
		else:
			req = '/api/relex/predict_file'

		if not doctype:
			doctype = document[::-1][:document[::-1].find('.')][::-1]

		sents = []

		if termite_addr:
			#Call TERMite to split sentences...
			binary = open(os.path.join(document), 'rb').read()

			if termite_user:
				data = {'binary': binary, 'format': doctype, 'termite_user': termite_user,
				'termite_pass': termite_pass}
			else:
				data = {'binary': binary, 'format': doctype}
			
			r = requests.post(termite_addr+'/toolkit/docxsent.api', data=data)
			j = r.json()
			for sent in j['sentences'][0]:
				sents.append(sent['sentence'])
		else:
			if doctype == 'txt':
				sents = self.sent_detector.tokenize(open(document, 'r').read())
			else:
				raise Exception('TERMite is required to parse files that are not .txt format')

		results = []

		for sent in sents:
			pred = self.relex_from_sent(model, sent, scibite_ai_addr=scibite_ai_addr, 
				scibite_ai_user=scibite_ai_user, scibite_ai_pass=scibite_ai_pass, 
				termite_addr=termite_addr, termite_user=termite_user, termite_pass=termite_pass)

			if pred:
				results.append(pred)
			else:
				if return_negatives:
					results.append(pred)

		return results


	###
	#NER functionality
	###


	def ner_from_sent(self, models, sent, format_='scibite', hits_only=True, scibite_ai_addr=None,
		scibite_ai_user=None, scibite_ai_pass=None):
		'''
		Pass a sentence within which you would like to identify examples of entities of specific
		type(s).

		:param array(string) models: List of named entity recognition models to use
		:param string sent: The sentence in which you want to identify entities
		:param string format_: The formatting style for your results, defaults to 'scinapse'
		:param bool hits_only: Set to False to also return terms with no entity identified
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if not self.models:
			self.populate_models_dict()

		if type(models) == str:
			models = [models]

		for model in models:
			if self.models['ner'][model]['loaded'] == 'False':
				self.load_model('ner', model)

		models = ','.join(models)

		if scibite_ai_addr.endswith('/api'):
			req = '/ner/predict_sentences'
		elif scibite_ai_addr.endswith('/ner'):
			req = '/predict_sentences'
		elif scibite_ai_addr.endswith('/predict_sentences'):
			req = ''
		else:
			req = '/api/ner/predict_sentences'

		data = {'model': models, 'sentence': sent, 'hits_only': hits_only, 'format': format_}

		if not scibite_ai_user:
			r = requests.get('http://' + scibite_ai_addr + req, data=data)
		else:
			r = requests.get('https://' + scibite_ai_addr + req, data=data, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		j = json.loads(r.text)

		return j


	def ner_from_doc(self, models, document, format_='scibite', hits_only=True, 
		scibite_ai_addr=None, scibite_ai_user=None, scibite_ai_pass=None):
		'''
		Pass a document within which you would like to identify examples of entities of specific
		type(s).

		:param array(string) models: List of named entity recognition models to use
		:param string document: The filepath of the document in which you want to identify entities
		:param string format_: The formatting style for your results, defaults to 'scinapse'
		:param bool hits_only: Set to False to also return terms with no entity identified
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if not self.models:
			self.populate_models_dict()

		if type(models) == str:
			models = [models]

		for model in models:
			if self.models['ner'][model]['loaded'] == 'False':
				self.load_model('ner', model)

		if scibite_ai_addr.endswith('/api'):
			req = '/ner/predict_file'
		elif scibite_ai_addr.endswith('/ner'):
			req = '/predict_file'
		elif scibite_ai_addr.endswith('/predict_file'):
			req = ''
		else:
			req = '/api/ner/predict_file'

		if not doctype:
			doctype = document[::-1][:document[::-1].find('.')][::-1]

		sents = []

		if termite_addr:
			#Call TERMite to split sentences...
			binary = open(os.path.join(document), 'rb').read()

			if termite_user:
				data = {'binary': binary, 'format': doctype, 'termite_user': termite_user, 
				'termite_pass': termite_pass}
			else:
				data = {'binary': binary, 'format': doctype}

			r = requests.post(termite_addr+'/toolkit/docxsent.api', data=data)
			j = r.json()
			for sent in j['sentences'][0]:
				sents.append(sent['sentence'])
		else:
			if doctype == 'txt':
				sents = self.sent_detector.tokenize(open(document, 'r').read())
			else:
				raise Exception('TERMite is required to parse files that are not .txt format')

		results = {}
		for idx, sent in enumerate(sents):
			pred = ner_from_sent(models=models, sent=sent, format=format, hits_only=hits_only)

			results[idx] = pred

		return results


	###
	#QA functionality
	###


	def qa_from_json(self, model, filepath,	scibite_ai_addr=None, scibite_ai_user=None, 
		scibite_ai_pass=None):
		'''
		Pass a file containing SQuAD formatted json questions/contexts to answer said questions.

		:param string model: The model trained to identify your relationship of interest
		:param string filepath: The filepath of the document containing SQuAD formatted questions
		you wish to have answered
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if not self.models:
			self.populate_models_dict()

		if self.models['qa'][model]['loaded'] == 'False':
			self.load_model('qa', model)

		if scibite_ai_addr.endswith('/api'):
			req = '/qa/answer_json_questions'
		elif scibite_ai_addr.endswith('/qa'):
			req = '/answer_json_questions'
		elif scibite_ai_addr.endswith('/answer_json_questions'):
			req = ''
		else:
			req = '/api/ner/answer_json_questions'

		binary = open(filepath, 'rb')

		data = {'file': binary, 'model': model}

		if not scibite_ai_user:
			r = requests.get('http://' + scibite_ai_addr + req, data=data)
		else:
			r = requests.get('https://' + scibite_ai_addr + req, data=data, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		j = json.loads(r.text)

		return j


	def qa_from_text():
		raise NotImplementedError('To be implemented when methods are finalised')


	###
	#W2V functionality
	###


	def w2v_vector(self, model, word, scibite_ai_addr=None, scibite_ai_user=None, 
		scibite_ai_pass=None, termite_addr=None, termite_user=None, termite_pass=None):
		'''
		Convert a word into a semantic vector using a w2v model.

		:param string model: The w2v model you want to use to convert your word to a vector
		:param string word: The word you wish to convert to a vector
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if 'termite' in model.lower():
			if not termite_addr:
				termite_addr = self.termite_credentials['termite_addr']
				termite_user = self.termite_credentials['termite_user']
				termite_pass = self.termite_credentials['termite_pass']
			if not termite_addr:
				raise Exception('You must specify an address for a TERMite server to use TERMite models')
			else:
				self.termite_credentials['termite_addr'] = termite_addr

		if not self.models:
			self.populate_models_dict()

		if self.models['ontology'][model]['loaded'] == 'False':
			self.load_model('ontology', model)

		if scibite_ai_addr.endswith('/api'):
			req = '/ontology/vector'
		elif scibite_ai_addr.endswith('/ontology'):
			req = '/vector'
		elif scibite_ai_addr.endswith('/vector'):
			req = ''
		else:
			req = '/api/ontology/vector'

		data = {'model': model, 'word': word}
		if termite_addr:
			data['termite_url'] = termite_addr
		if termite_user:
			data['termite_http_user'] = termite_user
		if termite_pass:
			data['termite_http_pass'] = termite_pass
		
		if not scibite_ai_user:
			r = requests.get('http://' + scibite_ai_addr + req, data=data)
		else:
			r = requests.get('https://' + scibite_ai_addr + req, data=data, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		j = json.loads(r.text)

		return j


	def w2v_most_similar(self, model, word, limit=5, filters=None, scibite_ai_addr=None,
		scibite_ai_user=None, scibite_ai_pass=None, termite_addr=None, termite_user=None, 
		termite_pass=None):
		'''
		Identify the words most similar to your root term using semantic vectors.

		:param string model: The w2v model you want to use to convert your word to a vector
		:param string word: The word you wish to convert to a vector
		:param int limit: The number of similar words you would like to be returned
		:param string filters: Filters to improve precision of final results, comma separated list
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if 'termite' in model.lower():
			if not termite_addr:
				termite_addr = self.termite_credentials['termite_addr']
				termite_user = self.termite_credentials['termite_user']
				termite_pass = self.termite_credentials['termite_pass']
			if not termite_addr:
				raise Exception('You must specify an address for a TERMite server to use TERMite models')
			else:
				self.termite_credentials['termite_addr'] = termite_addr

		if not self.models:
			self.populate_models_dict()

		if self.models['ontology'][model]['loaded'] == 'False':
			self.load_model('ontology', model)

		if scibite_ai_addr.endswith('/api'):
			req = '/ontology/similar'
		elif scibite_ai_addr.endswith('/ontology'):
			req = '/similar'
		elif scibite_ai_addr.endswith('/similar'):
			req = ''
		else:
			req = '/api/ontology/similar'

		data = {'model': model, 'word': word, 'limit': limit}
		if termite_addr:
			data['termite_url'] = termite_addr
		if termite_user:
			data['termite_http_user'] = termite_user
		if termite_pass:
			data['termite_http_pass'] = termite_pass

		if filters:
			data['filters'] = filters

		if not scibite_ai_user:
			r = requests.get('http://' + scibite_ai_addr + req, data=data)
		else:
			r = requests.get('https://' + scibite_ai_addr + req, data=data, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		j = json.loads(r.text)

		return j


	def w2v_algebra(self, model, algebra, limit=1, scibite_ai_addr=None, scibite_ai_user=None, 
		scibite_ai_pass=None, termite_addr=None, termite_user=None, termite_pass=None):
		'''
		Use word vectors to perform additions and subtractions within a semantic embedding space.

		:param string model: The w2v model you want to use to convert words to vectors
		:param string algebra: The algebra string to calculate (e.g. 'london-england+france')
		:param int limit: How many results to return
		:param string scibite_ai_addr: Address for the SciBite AI server (e.g. 127.0.0.1:8000)
		:param string scibite_ai_user: Username for the SciBite AI server http (if required)
		:param string scibite_ai_pass: Password for the SciBite AI server http (if required)
		'''

		if not scibite_ai_addr:
			scibite_ai_addr = self.scibite_ai_credentials['scibite_ai_addr']
			scibite_ai_user = self.scibite_ai_credentials['scibite_ai_user']
			scibite_ai_pass = self.scibite_ai_credentials['scibite_ai_pass']
		if not scibite_ai_addr:
			raise Exception('You must specify an address for the SciBite.ai server')
		else:
			self.scibite_ai_credentials['scibite_ai_addr'] = scibite_ai_addr

		if 'termite' in model.lower():
			if not termite_addr:
				termite_addr = self.termite_credentials['termite_addr']
				termite_user = self.termite_credentials['termite_user']
				termite_pass = self.termite_credentials['termite_pass']
			if not termite_addr:
				raise Exception('You must specify an address for a TERMite server to use TERMite models')
			else:
				self.termite_credentials['termite_addr'] = termite_addr

		if not self.models:
			self.populate_models_dict()

		if self.models['ontology'][model]['loaded'] == 'False':
			self.load_model('ontology', model)

		if scibite_ai_addr.endswith('/api'):
			req = '/ontology/algebra'
		elif scibite_ai_addr.endswith('/ontology'):
			req = '/algebra'
		elif scibite_ai_addr.endswith('/algebra'):
			req = ''
		else:
			req = '/api/ontology/algebra'

		data = {'model': model, 'algebra': algebra, 'limit': limit}
		if termite_addr:
			data['termite_url'] = termite_addr
		if termite_user:
			data['termite_http_user'] = termite_user
		if termite_pass:
			data['termite_http_pass'] = termite_pass

		if not scibite_ai_user:
			r = requests.get('http://' + scibite_ai_addr + req, data=data)
		else:
			r = requests.get('https://' + scibite_ai_addr + req, data=data, 
				auth=HTTPBasicAuth(scibite_ai_user, scibite_ai_pass))

		j = json.loads(r.text)

		return j


def get_hits(termiteTags, hierarchy=None, vocabs=None):
	'''
	Helper function. Uses termiteTags and hierarchy to collect info on the highest priority hits.

	:param array termiteTags: Locations of TERMite hits found, extracted from the TERMite json
	:param dict hierarchy: Dictionary with a hierarchy of vocabs to prioritise in case of overlap
	:param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
	empty, all vocabs found will be used with random priority where overlaps are found.
	:return array(dict):
	'''
	hits = []
	for hit in termiteTags:
		if not vocabs:
			if hit['entityType'] not in hierarchy:
				hierarchy[hit['entityType']] = len(hierarchy)
		else:
			if hit['entityType'] not in vocabs:
				continue

		if 'fls' in hit['exact_array'][0]: #TERMite 6.3...
			hitLocs, subsumeStates = hit['exact_array'], hit['subsume']
		else: #TERMite 6.4...
			hitLocs = []
			subsumeStates = []
			for hit_array in hit['exact_array']:
				hitLocs.append({'fls': [hit_array['sentence'], hit_array['start'], hit_array['end']]})
				subsumeStates.append(hit_array['subsumed'])

		assert len(hitLocs) == len(subsumeStates)

		for idx, hitLoc in enumerate(hitLocs):
			if hitLoc['fls'][0] < 1:
				continue
			hitInfo = {}
			hitInfo['entityType'], hitInfo['entityID'], hitInfo['entityName'] = hit['entityType'], hit['hitID'], hit[
				'name']
			breakBool = False
			hitInfo['startLoc'], hitInfo['endLoc'] = hitLoc['fls'][1], hitLoc['fls'][2]
			if subsumeStates[idx] == False:  # If hit is not subsumed...
				for hitIdx, hit_ in enumerate(hits):
					# Compare to already found hits to check there's no conflict
					if ((hit_['endLoc'] >= hitInfo['startLoc'] and hit_['endLoc'] <= hitInfo['endLoc']) or
							(hit_['startLoc'] >= hitInfo['startLoc'] and hit_['startLoc'] <= hitInfo['endLoc'])):
						# If they overlap, check their position in the hierarchy
						if hierarchy[hit_['entityType']] >= hierarchy[hitInfo['entityType']]:
							del hits[hitIdx]
							break
						else:
							breakBool = True
							break
			if not breakBool:
				hits.append(hitInfo)
	return hits


def markup(docjsonx, normalisation='id', substitute=True, wrap=False,
		   wrapChars=('{!', '!}'), vocabs=None, labels=None, replacementDict=None):
	'''
	Receives TERMite docjsonx output. Processes the original text, normalising identified hits.

	:param str docjsonx: JSON string generated by TERMite. Must be docjsonx.
	:param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
	:param bool substitute: Whether to replace the found term (or add normalisation alongside)
	:param bool wrap: Whether to wrap found hits with 'bookends'
	:param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
	:param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
	empty, all vocabs found will be used with random priority where overlaps are found.
	:param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
	and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1.
	replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
	:return dict:
	'''

	results = {}

	validTypes = ['id', 'type', 'name', 'typeplusname', 'typeplusid']
	if normalisation not in validTypes:
		raise ValueError(
			'Invalid normalisation requested. Valid options are \'id\', \'name\', \'type\', \'typeplusname\' and \'tyeplusid\'.')
	if len(wrapChars) != 2 or not all(isinstance(wrapping, str) for wrapping in wrapChars):
		raise ValueError('wrapChars must be a tuple of length 2, containing strings.')
	if labels:
		if labels not in ['word', 'char']:
			raise ValueError('labels, if specified, must be either \'word\' or \'char\'')

	hierarchy = {}
	if vocabs:
		for idx, vocab in enumerate(vocabs):
			hierarchy[vocab] = idx

	if isinstance(docjsonx, str):
		j = json.loads(docjsonx)
	else:
		j = docjsonx

	for docIdx, doc in enumerate(j):
		text = doc['body']

		try:
			substitutions = get_hits(doc['termiteTags'], hierarchy=hierarchy, vocabs=vocabs)
		except KeyError:
			results[docIdx] = {'termited_text': text}
			continue

		if len(substitutions) > 0:
			substitutions.sort(key=lambda x: x['startLoc'])
			substitutions = reversed(substitutions)

		if wrap:
			prefix = wrapChars[0]
			postfix = wrapChars[1]
		else:
			prefix, postfix = '', ''

		for sub in substitutions:
			subText = ''
			if replacementDict:
				subText = replacementDict[sub['entityType']].replace(
					'~TYPE~', sub['entityType']).replace('~ID~', sub['entityID']).replace('~NAME~', sub['entityName'])
			elif normalisation == 'id':
				subText = '_'.join([sub['entityType'], sub['entityID']])
				if not substitute:
					subText += ' %s' % text[sub['startLoc']:sub['endLoc']]
			elif normalisation == 'type':
				subText = sub['entityType']
				if not substitute:
					subText += ' %s' % text[sub['startLoc']:sub['endLoc']]
			elif normalisation == 'name':
				subText = sub['entityName']
				if not substitute:
					subText += ' %s' % text[sub['startLoc']:sub['endLoc']]
			elif normalisation == 'typeplusname':
				subText = '%s %s' % (sub['entityType'], sub['entityName'])
				if not substitute:
					subText += ' %s' % text[sub['startLoc']:sub['endLoc']]
			elif normalisation == 'typeplusid':
				subText = '%s %s' % (sub['entityType'], '_'.join([sub['entityType'], sub['entityID']]))
				if not substitute:
					subText += ' %s' % text[sub['startLoc']:sub['endLoc']]
			text = text[:sub['startLoc']] + prefix + subText + postfix + text[sub['endLoc']:]

		results[docIdx] = {'termited_text': text}

	return results


def text_markup(text, termiteAddr='http://localhost:9090/termite', vocabs=['GENE', 'INDICATION', 'DRUG'],
				normalisation='id', wrap=False, wrapChars=('{!', '!}'), substitute=True, replacementDict=None,
				termite_http_user=None, termite_http_pass=None, include_json=False):
	'''
	Receives plain text, returns text with TERMited substitutions.

	:param str normalisation: Type of normalisation to substitute/add (must be 'id', 'type', 'name', 'typeplusname' or 'typeplusid')
	:param bool substitute: Whether to replace the found term (or add normalisation alongside)
	:param bool wrap: Whether to wrap found hits with 'bookends'
	:param tuple(str) wrapChars: Tuple of length 2, containing strings to insert at start/end of found hits
	:param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
	empty, all vocabs found will be used with random priority where overlaps are found.
	:param dict replacementDict: Dictionary with <VOCAB>:<string_to_replace_hits_in_vocab>. '~ID~' will be replaced with the entity id,
	and '~TYPE~' will be replaced with the vocab name. Example: {'GENE':'ENTITY_~TYPE~_~ID~'} would result in BRCA1 -> ENTITY_GENE_BRCA1
	replacementDict supercedes normalisation. ~NAME~ can also be used to get the preferred name.
	:return str:
	'''

	t = termite.TermiteRequestBuilder()
	t.set_url(termiteAddr)
	t.set_text(text)
	t.set_entities(','.join(vocabs))
	t.set_subsume(True)
	t.set_input_format("txt")
	t.set_output_format("doc.jsonx")
	if termite_http_pass:
		t.set_basic_auth(termite_http_user, termite_http_pass, verification=False)
	docjsonx = t.execute()

	if include_json:
		return markup(docjsonx, vocabs=vocabs, normalisation=normalisation, wrap=wrap,
					  wrapChars=wrapChars, substitute=substitute, 
					  replacementDict=replacementDict)[0]['termited_text'], docjsonx
	else:
		return markup(docjsonx, vocabs=vocabs, normalisation=normalisation, wrap=wrap,
					  wrapChars=wrapChars, substitute=substitute, 
					  replacementDict=replacementDict)[0]['termited_text']


def label(docjsonx, vocabs, labelLevel='word'):
	'''
	Receives TERMite output docjsonx and returns split text with labels as to what entities are found in that part of the text.

	:param str docjsonx: JSON string generated by TERMite. Must be docjsonx.
	:param str labelLevel: Labels for where hits are found in the text. Must be 'char' or 'word', word by default
	:param array(str) vocabs: List of vocabs to be substituted, ordered by priority. These vocabs MUST be in the TERMite results. If left
	empty, all vocabs found will be used with random priority where overlaps are found.
	:return dict:
	'''

	results = {}
	substitutions = []
	hierarchy = {}
	for idx, vocab in enumerate(vocabs):
		hierarchy[vocab] = idx

	if isinstance(docjsonx, str):
		j = json.loads(docjsonx)
	else:
		j = docjsonx

	for docIdx, doc in enumerate(j):
		text = doc['body']

		splitText, labels = None, None
		if labelLevel == 'word':
			splitText = text.split()
		elif labelLevel == 'char':
			splitText = list(text)
		labels = [0 for i in splitText]

		try:
			hits = get_hits(doc['termiteTags'], hierarchy=hierarchy, vocabs=vocabs)
		except KeyError:
			results[docIdx] = {'split_text': splitText, 'labels': labels}
			continue

		for hit in hits:
			if labelLevel == 'char':
				for i in range(hit['startLoc'], hit['endLoc']):
					labels[i] = hierarchy[hit['entityType']] + 1
			elif labelLevel == 'word':
				cursor = 0
				for wIdx, w in enumerate(splitText):
					if cursor >= hit['startLoc'] and cursor <= hit['endLoc']:
						labels[wIdx] = hierarchy[hit['entityType']] + 1
					cursor += len(w) + 1

		results[docIdx] = {'split_text': splitText, 'labels': labels}

	return results
