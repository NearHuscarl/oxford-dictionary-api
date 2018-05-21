#!/bin/env python3

""" oxford dictionary api """

from http import cookiejar

import requests
from bs4 import BeautifulSoup as soup

class WordNotFound(Exception):
	""" word not found in dictionary (404 status code) """
	pass

class BlockAll(cookiejar.CookiePolicy):
	""" policy to block cookies """
	return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
	netscape = True
	rfc2965 = hide_cookie2 = False

class Word(object):
	""" retrive word info from oxford dictionary website """
	entry_selector = '#entryContent > .entry'
	header_selector = '.top-container'

	title_selector = header_selector + ' h2'
	wordform_selector = header_selector + ' .webtop-g .pos'
	property_global_selector = header_selector + ' .gram-g'

	br_pronounce_selector = '[class="pron-gs ei-g"] [geo=br] .phon'
	am_pronounce_selector = '[class="pron-gs ei-g"] [geo=n_am] .phon'
	br_pronounce_audio_selector = '[class="pron-gs ei-g"] [geo=br] [data-src-ogg]'
	am_pronounce_audio_selector = '[class="pron-gs ei-g"] [geo=n_am] [data-src-ogg]'

	namespaces_selector = '.h-g > .sn-gs'
	examples_selector = '.h-g > .sn-gs > .sn-g > .x-gs .x'
	definitions_selector = '.h-g > .sn-gs > .sn-g > .def'

	extra_examples_selector = '.res-g [title="Extra examples"] .x-gs .x'
	phrasal_verbs_selector = '.pv-gs a'
	idioms_selector = '.idm-gs > .idm-g'

	other_results_selector = '#rightcolumn #relatedentries'

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

		page_html = req.get(cls.get_url(word), timeout=5, headers={'User-agent': 'mother animal'})
		if page_html.status_code == 404:
			raise WordNotFound
		else:
			cls.soup_data = soup(page_html.content, 'html.parser')

		if cls.soup_data is not None:
			# remove some unnecessary tags to prevent false positive results
			cls.delete('[title="Oxford Collocations Dictionary"]')
			cls.delete('[title="British/American"]') # edge case: 'phone'
			cls.delete('[title="Express Yourself"]')
			cls.delete('[title="Collocations"]')
			cls.delete('[title="Word Origin"]')

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
					{'word1': word1, 'id1': id1, 'wordform1': wordform1},
					{'word2': word2, 'id2': id2, 'wordform2': wordform2}
					...
					]
				'Phrasal verbs': [
					{'word1': word1, 'id1': id1, 'wordform1': wordform1},
					{'word2': word2, 'id2': id2, 'wordform2': wordform2}
					...
					]
				...
				}
		"""
		info = []

		try:
			rightcolumn_tags = cls.soup_data.select(cls.other_results_selector)[0]
		except IndexError:
			return None

		# there can be multiple other results table like All matches, Phrasal verbs, Idioms,...
		header_tags = rightcolumn_tags.select('dt')
		other_results_tags = rightcolumn_tags.select('dd')

		# loop each other result table
		for header_tag, other_results_tag in zip(header_tags, other_results_tags):
			header = header_tag.text

			other_results = [tag.find_all(text=True) for tag in other_results_tag.select('span')]
			ids = [cls.extract_id(tag.attrs['href'])
					for tag in other_results_tag.select('li a')]

			results = []
			for other_result, id in zip(other_results, ids):
				result = {}
				result['name'] = other_result[0].strip()
				result['id'] = id

				try:
					result['wordform'] = other_result[1].strip()
				except IndexError:
					pass

				results.append(result)

			info.append({header: results})

		return info

	@classmethod
	def similars(cls):
		""" get other word form (verb, noun...) of a word
		Return: a list of ids in other form

		Example word: 'man'
		Return ['man_2', 'man_3']
		"""
		if cls.soup_data is None:
			return None

		name = cls.name()
		other_id = []

		try:
			rightcolumn_tags = cls.soup_data.select(cls.other_results_selector)[0]
		except IndexError: # dont have other match table
			return []

		allmatches_tags = rightcolumn_tags.select_one('dd') # get the first dd only

		for allmatches_tag in allmatches_tags.select('li'):
			other_name = allmatches_tag.select('span')[0].find(text=True).strip() # get first word only
			if name == other_name:
				id = cls.extract_id(allmatches_tag.select('a')[0].attrs['href'])
				other_id.append(id)

		return other_id

	@classmethod
	def name(cls):
		""" get word name """
		if cls.soup_data is None:
			return None
		return cls.soup_data.select(cls.title_selector)[0].text

	@classmethod
	def id(cls):
		""" get id of a word. if a word has definitions in 2 seperate pages
		(multiple wordform) it will return 'word_1' and 'word_2' depend on
		which page it's on """
		if cls.soup_data is None:
			return None
		return cls.soup_data.select(cls.entry_selector)[0].attrs['id']

	@classmethod
	def wordform(cls):
		""" return wordform of word (verb, noun, adj...) """
		if cls.soup_data is None:
			return None

		try:
			return cls.soup_data.select(cls.wordform_selector)[0].text
		except IndexError:
			return None

	@classmethod
	def property_global(cls):
		""" return global property (apply to all definitions) """
		if cls.soup_data is None:
			return None

		try:
			return cls.soup_data.select(cls.property_global_selector)[0].text
		except IndexError:
			return None

	@classmethod
	def get_prefix_from_filename(cls, filename):
		""" get prefix (NAmE or BrE) from audio name when prefix is null """
		if '_gb_' in filename:
			return 'BrE'

		elif '_us_' in filename:
			return 'NAmE'

		return None

	@classmethod
	def pronunciations(cls):
		""" get britain and america pronunciations """
		if cls.soup_data is None:
			return None

		britain = {'prefix': None, 'ipa': None, 'url': None}
		america = {'prefix': None, 'ipa': None, 'url': None}

		try:
			britain_pron_tag = cls.soup_data.select(cls.br_pronounce_selector)[0]
			america_pron_tag = cls.soup_data.select(cls.am_pronounce_selector)[0]

			britain['prefix'], britain['ipa'] = britain_pron_tag.text.split('//')[:-1]
			america['prefix'], america['ipa'] = america_pron_tag.text.split('//')[:-1]
		except IndexError:
			pass

		try:
			britain['url'] = cls.soup_data.select(cls.br_pronounce_audio_selector)[0].attrs['data-src-ogg']
			america['url'] = cls.soup_data.select(cls.am_pronounce_audio_selector)[0].attrs['data-src-ogg']
		except IndexError:
			pass

		if britain['prefix'] == None and britain['url'] is not None:
			britain['prefix'] = cls.get_prefix_from_filename(britain['url'])

		if america['prefix'] == None and america['url'] is not None:
			america['prefix'] = cls.get_prefix_from_filename(america['url'])

		return [britain, america]

	@classmethod
	def extract_id(cls, link):
		""" get word id from link
		Argument: https://abc/definition/id
		Return: id
		"""
		return link.split('/')[-1]

	@classmethod
	def get_references(cls, tags):
		""" get info about references to other page
		Argument: soup.select(<selector>)
		Return: [{'id': <id>, 'name': <word>}, {'id': <id2>, 'name': <word2>}, ...]
		"""
		if cls.soup_data is None:
			return None

		references = []
		for tag in tags.select('.xr-gs a'): # see also <external link>
			id = cls.extract_id(tag.attrs['href'])
			word = tag.text
			references.append({'id': id, 'name': word})

		return references

	@classmethod
	def references(cls):
		""" get global references """
		if cls.soup_data is None:
			return None

		header_tag = cls.soup_data.select(cls.header_selector)[0]
		return cls.get_references(header_tag)

	@classmethod
	def definitions(cls, full=False):
		""" Return: list of definitions """
		if cls.soup_data is None:
			return None

		if not full:
			return [tag.text for tag in cls.soup_data.select(cls.definitions_selector)]
		return cls.definition_full()

	@classmethod
	def examples(cls):
		""" List of all examples (not categorized in seperate definitions) """
		if cls.soup_data is None:
			return None
		return [tag.text for tag in cls.soup_data.select(cls.examples_selector)]

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
			id = cls.extract_id(tag.attrs['href']) # https://abc/definition/id -> id

			phrasal_verbs.append({'name': phrasal_verb, 'id': id})

		return phrasal_verbs

	@classmethod
	def definition_full(cls):
		""" return word definition + corresponding examples

		A word can have a single (None) or multiple namespaces
		Each namespace can have one or many definitions
		Each definitions can have one, many or no examples

		Some words can have specific property
		(transitive/intransitive/countable/uncountable/singular/plural...)
		A verb can have phrasal verbs

		Sample html:
			<span class='sn-gs'>                       <!-- namespace + definitions + examples -->
				<span class='shcut'></span>            <!-- namespace -->
				<span class='sn-g'>                    <!-- definition + examples -->
					<span class='gram-g'>...</span>    <!-- property (countable, transitive, plural,...) -->
					<span class='label-g'>...</span>   <!-- label (old-fashioned, informal, saying,...) -->
					<span class='dis-g'>...</span>     <!-- refer to something (of people, of thing,...) -->
					<span class='def'>...</span>       <!-- definition description -->
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
			definition_full_tags = namespace_tag.select('.sn-g')

			for definition_full_tag in definition_full_tags:
				definition = {}

				try: # property (countable, transitive, plural,...)
					definition['property'] = definition_full_tag.select('.gram-g')[0].text
				except IndexError:
					pass

				try: # label: (old-fashioned), (informal), (saying)...
					definition['label'] = definition_full_tag.select('.label-g')[0].text
				except IndexError:
					pass

				try: # refer to something (of people, of thing,...)
					definition['refer'] = definition_full_tag.select('.dis-g')[0].text
				except IndexError:
					pass

				definition['references'] = cls.get_references(definition_full_tag)
				if not definition['references']:
					definition.pop('references', None)

				try: # sometimes, it just refers to other page without having a definition
					definition['description'] = definition_full_tag.select('.def')[0].text
				except IndexError:
					pass

				definition['examples'] = [example_tag.text
						for example_tag in definition_full_tag.select('.x-gs .x')]

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
					<span class='dis-g'>...</span>     <!-- refer to something (of people, of thing,...) -->
					<span class='def'>...</span>       <!-- definition description -->
					<span class='x-gs'>                <!-- examples -->
						<span class='x'>               <!-- example -->
						<span class='x'>               <!-- example -->
					</span>
					<span class='xr-gs'>               <!-- external references -->
						<a href='../id'>...</a>   <!-- reference link -->
						<a href='../id'>...</a>   <!-- reference link -->
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

				try: # sometimes, it just refers to other page without having a definition
					definition['description'] = definition_tag.select('.def')[0].text
				except IndexError:
					pass

				try: # label: (old-fashioned), (informal), (saying)...
					definition['label'] = definition_tag.select('.label-g')[0].text
				except IndexError:
					pass

				try: # refer to something (of people, of thing,...)
					definition['refer'] = definition_tag.select('.dis-g')[0].text
				except IndexError:
					pass

				definition['references'] = cls.get_references(definition_tag)
				if not definition['references']:
					definition.pop('references', None)

				definition['examples'] = [example_tag.text for example_tag in definition_tag.select('.x')]
				definitions.append(definition)

			idioms.append({'name': idiom, 'definitions': definitions})

		return idioms

	@classmethod
	def info(cls):
		""" return all info about a word """
		if cls.soup_data is None:
			return None

		word = {
				'id': cls.id(),
				'similars': cls.similars(),
				'name': cls.name(),
				'wordform': cls.wordform(),
				'pronunciations': cls.pronunciations(),
				'references': cls.references(),
				'property': cls.property_global(),
				'definitions': cls.definitions(full=True),
				'extra_examples': cls.extra_examples(),
				'idioms': cls.idioms(),
				'other_results': cls.other_results()
				}

		if not word['references']:
			word.pop('references', None)

		if not word['property']:
			word.pop('property', None)

		if not word['other_results']:
			word.pop('other_results', None)

		if word['wordform'] == 'verb':
			word['phrasal_verbs'] = cls.phrasal_verbs()

		return word

# vim: nofoldenable
