#!/bin/env python

""" oxford diciontary api """

import os
import logging
import urllib.request
from http import cookiejar

import requests
from bs4 import BeautifulSoup as soup

logpath = os.path.join(os.environ['HOME'], '.cache', 'oxford_scraping.log')
logging.basicConfig(filename=logpath, level=logging.DEBUG)

class BlockAll(cookiejar.CookiePolicy):
	""" policy to block cookies """
	return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
	netscape = True
	rfc2965 = hide_cookie2 = False

class Word(object):
	""" retrive word info from oxford dictionary website """
	other_results_selector = '#rightcolumn #relatedentries'

	entry_selector = '#entryContent > .entry'

	br_pronounce_selector = '[class="pron-gs ei-g"] [geo=br] .phon'
	am_pronounce_selector = '[class="pron-gs ei-g"] [geo=n_am] .phon'
	br_pronounce_audio_selector = '[class="pron-gs ei-g"] [geo=br] [data-src-ogg]'
	am_pronounce_audio_selector = '[class="pron-gs ei-g"] [geo=n_am] [data-src-ogg]'

	wordform_selector = '.top-container .webtop-g .pos'
	amount_selector = '.top-container .gram-g'
	header_selector = '.top-container'

	namespaces_selector = '.h-g > .sn-gs'
	example_selector = '.h-g > .sn-gs > .sn-g > .x-gs .x'
	definition_selector = '.h-g > .sn-gs > .sn-g > .def'

	extra_examples_selector = '.res-g [title="Extra examples"] .x-gs .x'
	phrasal_verbs_selector = '.pv-gs a'
	idioms_selector = '.idm-gs > .idm-g'

	soup_data = None

	@classmethod
	def get_url(cls, word):
		""" get url of word definition """
		baseurl = 'https://www.oxfordlearnersdictionaries.com/definition/english/'
		return baseurl + word

	@classmethod
	def delete(cls, selector):
		""" remove tag with specified selector in cls.soup_data """
		try:
			for tag in cls.soup_data.select(selector):
				tag.decompose()
		except IndexError:
			pass

	@classmethod
	def get(cls, word):
		""" get html soup of word """
		req = requests.Session()
		req.cookies.set_policy(BlockAll())

		try:
			page_html = req.get(cls.get_url(word), timeout=5, headers={'User-agent': 'mother animal'})
			if page_html.status_code == 200:
				cls.soup_data = soup(page_html.content, 'html.parser')
			else:
				logging.debug('Requests failed. Status code: {}'.format(page_html.status_code))
		except requests.Timeout as error:
			logging.debug('Requests failed. Timeout: {}'.format(error))

		if cls.soup_data is None:
			return

		# remove the unnecessary because sometimes the selector will get false positive results
		cls.delete('[title="Oxford Collocations Dictionary"]')

	@classmethod
	def other_results(cls):
		""" get similar words, idioms, phrases...

		Sample html:
			<div id='relatedentries'>
				<dt>All matches</dt>
				<dd>
					<a href='link'>
						<span>word<pos>wordform</pos></span>
					</a>
					<a href='link'>...</a>
					<a href='link'>...</a>
				</dd>
				<dt>All matches</dt>
				<dd>..</dd>
				<dt>Phrasal verbs</dt>
				<dd>..</dd>
			</div>

		Return: {
				'All matches': [
					{'word1': word1, 'reference1': reference1, 'wordform1': wordform1},
					{'word2': word2, 'reference2': reference2, 'wordform2': wordform2}
					...
					]
				'Phrasal verbs': [
					{'word1': word1, 'reference1': reference1, 'wordform1': wordform1},
					{'word2': word2, 'reference2': reference2, 'wordform2': wordform2}
					...
					]
				...
				}
		"""
		info = []

		rightcolumn_tags = cls.soup_data.select(cls.other_results_selector)[0]

		# there can be multiple other results table like All matches, Phrasal verbs, Idioms,...
		header_tags = rightcolumn_tags.select('dt')
		other_results_tags = rightcolumn_tags.select('dd')

		# loop each other result table
		for header_tag, other_results_tag in zip(header_tags, other_results_tags):
			header = header_tag.text

			other_results = [tag.find_all(text=True) for tag in other_results_tag.select('span')]
			references = [cls.extract_keyword(tag.attrs['href'])
					for tag in other_results_tag.select('li a')]

			results = []
			for other_result, reference in zip(other_results, references):
				result = {}
				result['text'] = other_result[0].strip()
				result['reference'] = reference

				try:
					result['wordform'] = other_result[1].strip()
				except IndexError:
					pass

				results.append(result)

			info.append({header: results})

		return info

	@classmethod
	def other_wordform(cls):
		""" get other word form (verb, noun...) of a word """
		if cls.soup_data is None:
			return None
		pass

	@classmethod
	def keyword(cls):
		""" get keyword. if a word has definitions in 2 seperate pages (multiple wordform)
		it will return 'word_1' and 'word_2' depend on which page it's on """
		if cls.soup_data is None:
			return None
		return cls.soup_data.select(cls.entry_selector)[0].attrs['id']

	@classmethod
	def wordform(cls):
		""" return wordform of word (verb, noun, adj...) """
		if cls.soup_data is None:
			return None
		return cls.soup_data.select(cls.wordform_selector)[0].text

	@classmethod
	def amount(cls):
		""" return global amount (apply to all definitions) """
		if cls.soup_data is None:
			return None

		try:
			return cls.soup_data.select(cls.amount_selector)[0].text
		except IndexError:
			return None

	@classmethod
	def pronunciations(cls):
		""" get britain and america pronunciations """
		if cls.soup_data is None:
			return None

		britain = cls.soup_data.select(cls.br_pronounce_selector)[0].text.replace('/', ' ').split()
		america = cls.soup_data.select(cls.am_pronounce_selector)[0].text.replace('/', ' ').split()

		br_audio_url = cls.soup_data.select(cls.br_pronounce_audio_selector)[0].attrs['data-src-ogg']
		am_audio_url = cls.soup_data.select(cls.am_pronounce_audio_selector)[0].attrs['data-src-ogg']

		return {
				britain[0]: {
					'ipa': britain[1],
					'url': br_audio_url
				},
				america[0]: {
					'ipa': america[1],
					'url': am_audio_url
					}
				}

	@classmethod
	def download_pronunciation_audio(cls, path):
		""" download britain and american pron audio to path (dir) """
		br_audio_url = cls.soup_data.select(cls.br_pronounce_audio_selector)[0].attrs['data-src-ogg']
		am_audio_url = cls.soup_data.select(cls.am_pronounce_audio_selector)[0].attrs['data-src-ogg']

		urllib.request.urlretrieve(br_audio_url, os.path.join(path, cls.keyword()))
		urllib.request.urlretrieve(am_audio_url, os.path.join(path, cls.keyword()))

	@classmethod
	def extract_keyword(cls, link):
		""" get keyword from link
		Argument: https://abc/definition/keyword
		Return: keyword
		"""
		return link.split('/')[-1]

	@classmethod
	def get_references(cls, tags):
		""" get info about references to other page
		Argument: soup.select(<selector>)
		Return: {<keyword>: <word>, <keyword2>: <word2>, ...}
		"""
		if cls.soup_data is None:
			return None

		reference = {}
		for tag in tags.select('.xr-gs a'): # see also <external link>
			keyword = cls.extract_keyword(tag.attrs['href'])
			word = tag.text
			reference[keyword] = word

		return reference

	@classmethod
	def reference(cls):
		""" get global reference """
		if cls.soup_data is None:
			return None

		header_tag = cls.soup_data.select(cls.header_selector)[0]
		return cls.get_references(header_tag)

	@classmethod
	def definitions(cls):
		""" Return: list of definitions """
		if cls.soup_data is None:
			return None
		return [tag.text for tag in cls.soup_data.select(cls.definition_selector)]

	@classmethod
	def examples(cls):
		""" List of all examples (not categorized in seperate definitions) """
		if cls.soup_data is None:
			return None
		return [tag.text for tag in cls.soup_data.select(cls.example_selector)]

	@classmethod
	def extra_examples(cls):
		""" get extra examples """
		if cls.soup_data is None:
			return None
		return [tag.text for tag in cls.soup_data.select(cls.extra_examples_selector)]

	@classmethod
	def phrasal_verbs(cls):
		""" get phrasal verbs list (verb only) """
		if cls.soup_data is None:
			return None

		phrasal_verbs = []
		for tag in cls.soup_data.select(cls.phrasal_verbs_selector):
			phrasal_verb = tag.select('.xh')[0].text
			keyword = cls.extract_keyword(tag.attrs['href']) # https://abc/definition/keyword -> keyword

			phrasal_verbs.append({'name': phrasal_verb, 'keyword': keyword})

		return phrasal_verbs

	@classmethod
	def definitions_examples(cls):
		""" return word definition + corresponding examples

		A word can have a single (None) or multiple namespaces
		Each namespace can have one or many definitions
		Each definitions can have one, many or no examples

		A noun can have amount attribute (countable/uncountable/singular/plural)
		A verb can have phrasal verbs

		Sample html:
			<span class='sn-gs'>                       <!-- namespace + definitions + examples -->
				<span class='shcut'></span>            <!-- namespace -->
				<span class='sn-g'>                    <!-- definition + examples -->
					<span class='gram-g'>...</span>    <!-- amount (noun only) -->
					<span class='label-g'>...</span>   <!-- label (old-fashioned, informal, saying,...) -->
					<span class='def'>...</span>       <!-- definition -->
					<span class='x-gs'>                <!-- examples -->
						<span class='x'>               <!-- example -->
						<span class='x'>               <!-- example -->
					</span>
				</span>
				<span class='sn-g'></span>             <!-- definition + examples -->
				<span class='sn-g'></span>             <!-- definition + examples -->
			</span>
			<span class='sn-gs'></span>                <!-- namespace + definitions + examples -->
			<span class='sn-gs'></span>                <!-- namespace + definitions + examples -->
		"""
		if cls.soup_data is None:
			return None

		namespace_tags = cls.soup_data.select(cls.namespaces_selector) # sn-gs

		info = []
		for namespace_tag in namespace_tags:
			try:
				namespace = namespace_tag.select('.shcut')[0].text
			except IndexError:
				# some word have similar definitions grouped in a multiple namespaces (time)
				# some do not, and only have one namespace (woman)
				namespace = None

			definitions = []
			definition_example_tags = namespace_tag.select('.sn-g')

			for definition_example_tag in definition_example_tags:
				definition = {}

				try: # noun have amount attribute indicate countable/uncountable/singular/plural...
					definition['amount'] = definition_example_tag.select('.gram-g')[0].text
				except IndexError:
					definition.pop('amount', None)

				try: # label: (old-fashioned), (informal), (saying)...
					definition['label'] = definition_example_tag.select('.label-g')[0].text
				except IndexError:
					definition.pop('label', None)

				definition['reference'] = cls.get_references(definition_example_tag)
				if not definition['reference']:
					definition.pop('reference', None)

				definition['definition'] = definition_example_tag.select('.def')[0].text
				definition['examples'] = [example_tag.text
						for example_tag in definition_example_tag.select('.x-gs .x')]

				definitions.append(definition)

			info.append({'namespace': namespace, 'definitions': definitions})

		return info

	@classmethod
	def idioms(cls):
		""" get word idioms

		Idioms dont have namespace like regular definitions
		Each idioms have one or more definitions
		Each definitions can have one, many or no examples

		Sample html:
			<span class='idm-g'>                       <!-- idiom + definitions + examples -->
				<span class='idm-l'>                   <!-- idiom -->
					<span class='idm'>...</span>
					<span class='idm'>...</span>
				</span>
				<span class='sn-g'>                    <!-- definition + examples -->
					<span class='label-g'>...</span>   <!-- label (old-fashioned, informal, saying,...) -->
					<span class='def'>...</span>       <!-- definition -->
					<span class='x-gs'>                <!-- examples -->
						<span class='x'>               <!-- example -->
						<span class='x'>               <!-- example -->
					</span>
					<span class='xr-gs'>               <!-- external references -->
						<a href='../keyword'>...</a>   <!-- reference link -->
						<a href='../keyword'>...</a>   <!-- reference link -->
					</span>
				</span>
				<span class='sn-g'></span>             <!-- definition + examples -->
				<span class='sn-g'></span>             <!-- definition + examples -->
			</span>
			<span class='idm-g'></span>                <!-- idiom + definitions + examples -->
			<span class='idm-g'></span>                <!-- idiom + definitions + examples -->
		"""
		idiom_tags = cls.soup_data.select(cls.idioms_selector)

		idioms = []
		for idiom_tag in idiom_tags:

			try:
				# sometimes idiom is in multiple idm classes inside
				# one idm-l class instead of a single idm class
				idiom = idiom_tag.select('.idm-l')[0].text
			except IndexError:
				idiom = idiom_tag.select('.idm')[0].text

			definitions = []
			# one idiom can have multiple definitions, each can have multiple examples or no example
			for definition_tag in idiom_tag.select('.sn-gs .sn-g'):
				definition = {}

				try:
					definition['definition'] = definition_tag.select('.def')[0].text
				except IndexError:
					pass # sometimes, an idiom just reference to other page without having a definition

				try: # label: (old-fashioned), (informal), (saying)...
					definition['label'] = idiom_tag.select('.label-g')[0].text
				except IndexError:
					definition.pop('label', None)

				definition['reference'] = cls.get_references(definition_tag)
				if not definition['reference']:
					definition.pop('reference', None)

				definition['examples'] = [example_tag.text for example_tag in definition_tag.select('.x')]
				definitions.append(definition)

			idioms.append({'idiom': idiom, 'definitions': definitions})

		return idioms

	@classmethod
	def info(cls):
		""" return all info about a word """
		word = {
				'keyword': cls.keyword(),
				'wordform': cls.wordform(),
				'pronunciations': cls.pronunciations(),
				'reference': cls.reference(),
				'definitions': cls.definitions_examples(),
				'extra_examples': cls.extra_examples(),
				'idioms': cls.idioms(),
				'other_results': cls.other_results()
				}

		if word['reference'] is None:
			word.pop('reference', None)

		if word['wordform'] == 'noun':
			word['amount'] = cls.amount()

		if word['wordform'] == 'verb':
			word['phrasal_verbs'] = cls.phrasal_verbs()

		return word

if __name__ == '__main__':
	pass
	# Word.get('time')
	# Word.info()

# vim: nofoldenable

# TODO:
# external link proper handling
# synonym
# dis-g
# check amount if noun
# otherword()
