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

    title_selector = header_selector + ' .headword'
    wordform_selector = header_selector + ' .pos'
    property_global_selector = header_selector + ' .grammar'

    br_pronounce_selector = '[geo=br] .phon'
    am_pronounce_selector = '[geo=n_am] .phon'
    br_pronounce_audio_selector = '[geo=br] [data-src-ogg]'
    am_pronounce_audio_selector = '[geo=n_am] [data-src-ogg]'

    definition_body_selector = '.senses_multiple'
    namespaces_selector = '.senses_multiple > .shcut-g'
    examples_selector = '.senses_multiple .sense > .examples .x'
    definitions_selector = '.senses_multiple .sense > .def'

    extra_examples_selector = '.res-g [title="Extra examples"] .x-gs .x'
    phrasal_verbs_selector = '.phrasal_verb_links a'
    idioms_selector = '.idioms > .idm-g'

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
            cls.delete('[title="British/American"]')  # edge case: 'phone'
            cls.delete('[title="Express Yourself"]')
            cls.delete('[title="Collocations"]')
            cls.delete('[title="Word Origin"]')

    @classmethod
    def other_results(cls):
        """ get similar words, idioms, phrases...

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
            other_results = []

            for item_tag in other_results_tag.select('li'):
                names = item_tag.select('span')[0].find_all(text=True, recursive=False)
                wordform_tag = item_tag.select('pos')
                names.append(wordform_tag[0].text if len(wordform_tag) > 0 else '')
                other_results.append(names)

            other_results = list(filter(None, other_results))  # remove empty list
            ids = [cls.extract_id(tag.attrs['href'])
                   for tag in other_results_tag.select('li a')]

            results = []
            for other_result, id in zip(other_results, ids):
                result = {}
                result['name'] = ' '.join(list(map(lambda x: x.strip(), other_result[0:-1])))
                result['id'] = id

                try:
                    result['wordform'] = other_result[-1].strip()
                except IndexError:
                    pass

                results.append(result)

            info.append({header: results})

        return info

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

            britain['ipa'] = britain_pron_tag.text
            britain['prefix'] = 'BrE'
            america['ipa'] = america_pron_tag.text
            america['prefix'] = 'nAmE'
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
        for tag in tags.select('.xrefs a'):  # see also <external link>
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
    def phrasal_verbs(cls):
        """ get phrasal verbs list (verb only) """
        if cls.soup_data is None:
            return None

        phrasal_verbs = []
        for tag in cls.soup_data.select(cls.phrasal_verbs_selector):
            phrasal_verb = tag.select('.xh')[0].text
            id = cls.extract_id(tag.attrs['href'])  # https://abc/definition/id -> id

            phrasal_verbs.append({'name': phrasal_verb, 'id': id})

        return phrasal_verbs

    @classmethod
    def _parse_definition(cls, parent_tag):
        """ return word definition + corresponding examples

        A word can have a single (None) or multiple namespaces
        Each namespace can have one or many definitions
        Each definitions can have one, many or no examples

        Some words can have specific property
        (transitive/intransitive/countable/uncountable/singular/plural...)
        A verb can have phrasal verbs
        """
        if cls.soup_data is None:
            return None

        definition = {}

        try:  # property (countable, transitive, plural,...)
            definition['property'] = parent_tag.select('.grammar')[0].text
        except IndexError:
            pass

        try:  # label: (old-fashioned), (informal), (saying)...
            definition['label'] = parent_tag.select('.labels')[0].text
        except IndexError:
            pass

        try:  # refer to something (of people, of thing,...)
            definition['refer'] = parent_tag.select('.dis-g')[0].text
        except IndexError:
            pass

        definition['references'] = cls.get_references(parent_tag)
        if not definition['references']:
            definition.pop('references', None)

        try:  # sometimes, it just refers to other page without having a definition
            definition['description'] = parent_tag.select('.def')[0].text
        except IndexError:
            pass

        definition['examples'] = [example_tag.text
                                  for example_tag in parent_tag.select('.examples .x')]

        definition['extra_example'] = [
            example_tag.text
            for example_tag in parent_tag.select('[unbox=extra_examples] .examples .unx')
        ]

        return definition

    @classmethod
    def definition_full(cls):
        """ return word definition + corresponding examples

        A word can have a single (None) or multiple namespaces
        Each namespace can have one or many definitions
        Each definitions can have one, many or no examples

        Some words can have specific property
        (transitive/intransitive/countable/uncountable/singular/plural...)
        A verb can have phrasal verbs
        """
        if cls.soup_data is None:
            return None

        namespace_tags = cls.soup_data.select(cls.namespaces_selector)

        info = []
        for namespace_tag in namespace_tags:
            try:
                namespace = namespace_tag.select('h2.shcut')[0].text
            except IndexError:
                # some word have similar definitions grouped in a multiple namespaces (time)
                # some do not, and only have one namespace (woman)
                namespace = None

            definitions = []
            definition_full_tags = namespace_tag.select('.sense')

            for definition_full_tag in definition_full_tags:
                definition = cls._parse_definition(definition_full_tag)
                definitions.append(definition)

            info.append({'namespace': namespace, 'definitions': definitions})

        # no namespace. all definitions is global
        if len(info) == 0:
            info.append({'namespace': '__GLOBAL__', 'definitions': []})
            def_body_tags = cls.soup_data.select(cls.definition_body_selector)

            definitions = []
            definition_full_tags = def_body_tags[0].select('.sense')

            for definition_full_tag in definition_full_tags:
                definition = cls._parse_definition(definition_full_tag)
                definitions.append(definition)

            info[0]['definitions'] = definitions

        return info

    @classmethod
    def idioms(cls):
        """ get word idioms

        Idioms dont have namespace like regular definitions
        Each idioms have one or more definitions
        Each definitions can have one, many or no examples
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

            global_definition = {}

            try:  # label: (old-fashioned), (informal), (saying)...
                global_definition['label'] = idiom_tag.select('.labels')[0].text
            except IndexError:
                pass

            try:  # refer to something (of people, of thing,...)
                global_definition['refer'] = idiom_tag.select('.dis-g')[0].text
            except IndexError:
                pass

                global_definition['references'] = cls.get_references(idiom_tag)
            if not global_definition['references']:
                global_definition.pop('references', None)

            definitions = []
            # one idiom can have multiple definitions, each can have multiple examples or no example
            for definition_tag in idiom_tag.select('.sense'):
                definition = {}

                try:  # sometimes, it just refers to other page without having a definition
                    definition['description'] = definition_tag.select('.def')[0].text
                except IndexError:
                    pass

                try:  # label: (old-fashioned), (informal), (saying)...
                    definition['label'] = definition_tag.select('.labels')[0].text
                except IndexError:
                    pass

                try:  # refer to something (of people, of thing,...)
                    definition['refer'] = definition_tag.select('.dis-g')[0].text
                except IndexError:
                    pass

                definition['references'] = cls.get_references(definition_tag)
                if not definition['references']:
                    definition.pop('references', None)

                definition['examples'] = [example_tag.text for example_tag in definition_tag.select('.x')]
                definitions.append(definition)

            idioms.append({'name': idiom, 'summary': global_definition, 'definitions': definitions})

        return idioms

    @classmethod
    def info(cls):
        """ return all info about a word """
        if cls.soup_data is None:
            return None

        word = {
            'id': cls.id(),
            'name': cls.name(),
            'wordform': cls.wordform(),
            'pronunciations': cls.pronunciations(),
            'property': cls.property_global(),
            'definitions': cls.definitions(full=True),
            'idioms': cls.idioms(),
            'other_results': cls.other_results()
        }

        if not word['property']:
            word.pop('property', None)

        if not word['other_results']:
            word.pop('other_results', None)

        if word['wordform'] == 'verb':
            word['phrasal_verbs'] = cls.phrasal_verbs()

        return word
