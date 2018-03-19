# oxford-dictionary-api

## Installation
* `pip install requests`
* Download [oxford.py](https://github.com/NearHuscarl/oxford-dictionary-api/blob/master/oxford.py)

## Usage

**Note:** Some of the output will be reformatted for representation purpose

* In REPL
```$ python -i oxford.py```

* In source file
```import oxford```

### Retrieve word info

Get word information. Mimic `requests.get()` function

```python
Word.get('run')
```

### Keyword

Return word id

```python
Word.keyword()
```

```
'run_1'
```

### Wordform

Return wordform (verb, noun, adj,...)

```python
Word.wordform()
```

```
'verb'
```

### Pronunciation

Return pronunciation audio links and ipa in british and america voice

```python
Word.pronunciations()
```

```
{
  'BrE': {
    'ipa': 'rʌn',
    'url': 'https://www.oxfordlearnersdictionaries.com/media/english/uk_pron_ogg/r/run/run__/run__gb_1.ogg'
  },
   'NAmE': {
    'ipa': 'rʌn',
    'url': 'https://www.oxfordlearnersdictionaries.com/media/english/us_pron_ogg/r/run/run__/run__us_1.ogg'
  }
}
```

### Reference

Return a dictionary of references to other pages with key is word id and value is word or phrase to go to

```python
Word.reference()
```

```
{
  'run_1': 'Elections',
  'run_2': 'Committing crime',
  'run_3': 'Train and bus travel',
  'run_4': 'Exercise',
  'run_5': 'Driving',
  'run_6': 'How machines work'
}
```

### Definition

Return a list of all definitions (exclude idioms)

```python
Word.definitions()
```

```
[
  'to move using your legs, going faster than when you walk',
  'to travel a particular distance by running',
  'to run as a sport',
  'to take part in a race',
  'to make a race take place',
  'to hurry from one place to another',
  'to be in charge of a business, etc.',
  'to make a service, course of study, etc. available to people',
  'to own and use a vehicle or machine',
  'to operate or function; to make something do this',
  'to travel on a particular route',
  'to make buses, trains, etc. travel on a particular route',
  'to drive somebody to a place in a car',
  'to move, especially quickly, in a particular direction',
  'to move something in a particular direction',
  'to lead or stretch from one place to another; to make something do this',
  'to continue for a particular period of time without stopping',
  'to operate or be valid for a particular period of time',
  'to happen at the time mentioned',
  'to bring or take something into a country illegally and secretly',
  'to have particular words, contents, etc.',
  'to flow',
  'to make liquid flow',
  'to send out a liquid',
  'to be covered with a liquid',
  'if the colour runs in a piece of clothing when it gets wet, it dissolves and '
  'may come out of the clothing into other things',
  'to melt',
  'to become different in a particular way, especially a bad way',
  'to be at or near a particular level',
  'to print and publish an item or a story',
  'to do a test/check on something',
  'to be a candidate in an election for a political position, especially in the '
  'US',
  'if tights or stockings run, a long thin hole appears in them'
]
```

### Examples

Return a list of all examples (exclude idioms)

```python
Word.examples()
```

```
[
  'Can you run as fast as Mike?',
  'They turned and ran when they saw us coming.',
  'She came running to meet us.',
  'I had to run to catch the bus.',
  'The dogs ran off as soon as we appeared.',
  'He ran home in tears to his mother.',
  'Who was the first person to run a mile in under four minutes?',
  'She used to run when she was at college.',
  'I often go running before work.',
  'He will be running in the 100 metres tonight.',
  'There are only five horses running in the first race.',
  'to run the marathon',
  'Holmes ran a fine race to take the gold medal.',
  ...
]
```

### Definition + Examples

Return a list of definitions and corresponding examples + other extra info

```python
Word.definitions_examples()
```

```
[{'definitions': [{'amount': '[intransitive]',
                   'definition': 'to move using your legs, going faster than '
                                 'when you walk',
                   'examples': ['Can you run as fast as Mike?',
                                'They turned and ran when they saw us coming.',
                                'She came running to meet us.',
                                'I had to run to catch the bus.',
                                'The dogs ran off as soon as we appeared.',
                                'He ran home in tears to his mother.',
                                'Run and get your swimsuits, kids.',
                                'I ran and knocked on the nearest door.'],
                   'reference': {'run_4': 'Exercise'}},
                  {'amount': '[transitive]',
                   'definition': 'to travel a particular distance by running',
                   'examples': ['Who was the first person to run a mile in '
                                'under four minutes?'],
                   'reference': {'mile': 'mile'}},
                  {'amount': '[intransitive]',
                   'definition': 'to run as a sport',
                   'examples': ['She used to run when she was at college.',
                                'I often go running before work.']}],
                   'namespace': 'move fast on foot'},
 {'definitions': [{'amount': '[intransitive, transitive]',
                   'definition': 'to take part in a race',
                   'examples': ['He will be running in the 100 metres tonight.',
                                'There are only five horses running in the '
                                'first race.',
                                'to run the marathon',
                                'Holmes ran a fine race to take the gold '
                                'medal.'],
                   'reference': {'runner': 'runner (1)'}},
                  {'amount': '[transitive, often passive]',
                   'definition': 'to make a race take place',
                   'examples': ['The Derby will be run in spite of the bad '
                                'weather.']}],
                   'namespace': 'race'},
```

### Extra Examples

Return extra examples (not belong to any particular definitons)

```python
Word.extra_examples()
```

```
[
  'He hopes to run for president in 2016.',
  'He just wanted to run away and hide.',
  'He ran headlong into an enemy patrol.',
  'He ran out of the house.',
  'He ran unsuccessfully for the Senate in New York.',
  'He was given two twelve-month sentences to run concurrently.',
  'In many respects his poetical development had run parallel to Wordsworth’s.',
  'John can run very fast.',
  'Local buses run regularly to and from the school.',
  'Our car only runs on unleaded petrol.',
  'She ran quickly downstairs.',
  'She turned and ran blindly down the street.',
  ...
]
```

### Idiom

Return a list of idioms information like idiom names, definitions and examples usage

```python
Word.idioms()
```

```
[{'definitions': [{'definition': 'a situation in which somebody only just wins '
                   'or loses, for example in a competition or an '
                   'election',
                   'examples': ['Mr Taylor’s election defeat was a close-run '
                                'thing.',
                                'The invasion never happened but it was a '
                                'close-run thing.']}],
                   'idiom': 'a close-run thing'},
 {'definitions': [{'definition': 'to be pleased to do what somebody wants',
                   'examples': ['She knew she had only to call and he would '
                                'come running.']}],
                   'idiom': 'come running'},
 {'definitions': [{'definition': 'to start doing something and continue very '
                                 'quickly and successfully',
                   'examples': [],
                   'label': '(informal)'}],
                   'idiom': 'hit the ground running'},
 {'definitions': [{'definition': 'to run in order to escape from '
                                 'somebody/something',
                   'examples': []}],
                   'idiom': 'run for it'},
 {'definitions': [{'definition': 'working fully and correctly',
                   'examples': ['It will be a lot easier when we have the '
                                'database up and running.']}],
                   'idiom': 'up and running'}]
```

### Other results

Return other similar results

```python
Word.other_results()
```

```
[{'All matches': [{'reference': 'run_2', 'text': 'run', 'wordform': 'noun'},
                  {'reference': 'ladder_1#ladder_1__50',
                   'text': 'ladder',
                   'wordform': 'noun'},
                  {'reference': 'ski-run#ski-run__15',
                   'text': 'ski run',
                   'wordform': 'noun'},
                  {'reference': 'stand_1#stand_1__591',
                   'text': 'stand',
                   'wordform': 'verb'},
                   ...
 {'Phrasal verbs': [{'reference': 'run-at',
                     'text': 'run at',
                     'wordform': 'phrasal verb'},
                    {'reference': 'run-by',
                     'text': 'run by',
                     'wordform': 'phrasal verb'},
                    {'reference': 'run-in_2',
                     'text': 'run in',
                     'wordform': 'phrasal verb'},
                     ...
{'Idioms': [{'reference': 'amok#amok__17', 'text': 'run amok'},
             {'reference': 'dry_1#dry_1__344', 'text': 'run dry'},
             {'reference': 'free_3#free_3__60', 'text': 'run free'},
             {'reference': 'high_3#high_3__146', 'text': 'run high'},
             ...
```

### All in 1

Return all information above in one function call

```python
Word.info()
```

```python
# Display the following info:
# keyword
# wordform
# pronunciations
# reference
# definitions + examples
# extra_examples
# idioms
# other_results
```

## License
**[BSD 3-Clauses](https://github.com/NearHuscarl/oxford-dictionary-api/blob/master/LICENSE.md)**
