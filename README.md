# Oxford Dictionary API

## Requirements
* `python3`
* python modules:
  * `requests`
  * `beautifulsoup4`

## Installation
* `pip install requests`
* `pip install beautifulsoup4`
* Download [oxford.py](https://github.com/NearHuscarl/oxford-dictionary-api/blob/master/oxford.py)

## Usage

**Note:** Some of the output will be reformatted for representation purpose

* In REPL

```bash
$ python -i oxford.py
```

* In source file

```python
import oxford
```

### Retrieve info

Get word information. Mimic `requests.get()` function

```python
Word.get('run')
```

### Word ID

Return word id

```python
Word.id()
```

```python
'run_1'
```

### Name

Return name of word

```python
Word.name()
```

```python
'run'
```

### Wordform

Return wordform (verb, noun, adj,...)

```python
Word.wordform()
```

```python
'verb'
```

### Pronunciation

Return pronunciation audio links and ipa in british and america voice

```python
Word.pronunciations()
```

```python
[{'ipa': 'rʌn',
  'prefix': 'BrE',
  'url': 'https://www.oxfordlearnersdictionaries.com/media/english/uk_pron_ogg/r/run/run__/run__gb_1.ogg'},
 {'ipa': 'rʌn',
  'prefix': 'NAmE',
  'url': 'https://www.oxfordlearnersdictionaries.com/media/english/us_pron_ogg/r/run/run__/run__us_1.ogg'}]
```

### Definition

Return a list of all definitions (exclude idioms)

```python
Word.definitions()
```

```python
['to move using your legs, going faster than when you walk',
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
 'if tights or stockings run, a long thin hole appears in them']
```

### Examples

Return a list of all examples (exclude idioms)

```python
Word.examples()
```

```python
['Can you run as fast as Mike?',
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
 'The Derby will be run in spite of the bad weather.',
 "I've spent the whole day running around after the kids.",
 'to run a hotel/store/language school',
 'He has no idea how to run a business.',
 'Stop trying to run my life (= organize it) for me.',
 'The shareholders want more say in how the company is run.',
 'a badly run company',
 'state-run industries',
 'The college runs summer courses for foreign students.',
 "I can't afford to run a car on my salary.",
 'Stan had the chainsaw running.',
 'Her life had always run smoothly before.',
 'Our van runs on (= uses) diesel.',
 'Could you run the engine for a moment?',
 'Buses to Oxford run every half hour.',
 'Trains between London and Brighton run throughout the day.',
 'All the trains are running late (= are leaving later than planned).',
 'They run extra trains during the rush hour.',
 'Shall I run you home?',
 'The car ran off the road into a ditch.',
 'A shiver ran down my spine.',
 'The sledge ran smoothly over the frozen snow.',
 'The old tramlines are still there but now no trams run on them.',
 'She ran her fingers nervously through her hair.',
 'I ran my eyes over the page.',
 'He had a scar running down his left cheek.',
 'The road runs parallel to the river.',
 'We ran a cable from the lights to the stage.',
 'Her last musical ran for six months on Broadway.',
 'This debate will run and run!',
 'The permit runs for three months.',
 'The lease on my house only has a year left to run.',
 'Programmes are running a few minutes behind schedule this evening.',
 'The murderer was given three life sentences, to run concurrently.',
 'He used to run guns across the border.',
 'Their argument ran something like this…',
 '‘Ten shot dead by gunmen,’ ran the newspaper headline.',
 'The tears ran down her cheeks.',
 'Water was running all over the bathroom floor.',
 'She ran hot water into the bucket.',
 'to run the hot tap (= to turn it so that water flows from it)',
 "I'll run a bath for you.",
 "I'll run you a bath.",
 'Who left the tap running?',
 'Your nose is running (= mucus is flowing from it).',
 'The smoke makes my eyes run.',
 'His face was running with sweat.',
 'The bathroom floor was running with water.',
 'The colour ran and made all my underwear pink.',
 'The wax began to run.',
 'The river ran dry (= stopped flowing) during the drought.',
 'Supplies are running low.',
 "We've run short of milk.",
 "You've got your rivals running scared.",
 'Inflation was running at 26%.',
 'On advice from their lawyers they decided not to run the story.',
 'The doctors decided to run some more tests on the blood samples.',
 'Bush ran a second time in 2004.',
 'to run for president',
 'to run in the election']
```

### Full Definition

Return a list of definitions and corresponding examples + other extra info

```python
Word.definitions(full=True)
```

```python
[{'definitions': [{'description': 'to move using your legs, going faster than '
                                  'when you walk',
                   'examples': ['Can you run as fast as Mike?',
                                'They turned and ran when they saw us coming.',
                                'She came running to meet us.',
                                'I had to run to catch the bus.',
                                'The dogs ran off as soon as we appeared.',
                                'He ran home in tears to his mother.',
                                'Run and get your swimsuits, kids.',
                                'I ran and knocked on the nearest door.'],
                   'property': '[intransitive]',
                   'references': [{'id': 'run_4', 'name': 'Exercise'}]},
                  {'description': 'to travel a particular distance by running',
                   'examples': ['Who was the first person to run a mile in '
                                'under four minutes?'],
                   'property': '[transitive]',
                   'references': [{'id': 'mile', 'name': 'mile'}]},
                  {'description': 'to run as a sport',
                   'examples': ['She used to run when she was at college.',
                                'I often go running before work.'],
                   'property': '[intransitive]'}],
  'namespace': 'move fast on foot'},
 {'definitions': [{'description': 'to take part in a race',
                   'examples': ['He will be running in the 100 metres tonight.',
                                'There are only five horses running in the '
                                'first race.',
                                'to run the marathon',
                                'Holmes ran a fine race to take the gold '
                                'medal.'],
                   'property': '[intransitive, transitive]',
                   'references': [{'id': 'runner', 'name': 'runner (1)'}]},
                  {'description': 'to make a race take place',
                   'examples': ['The Derby will be run in spite of the bad '
                                'weather.'],
                   'property': '[transitive, often passive]'}],
  'namespace': 'race'},
 ...]
```


### Idiom

Return a list of idioms information like idiom names, definitions and examples usage

```python
Word.idioms()
```

```python
[{'definitions': [{'description': 'to be pleased to do what somebody wants',
                   'examples': ['She knew she had only to call and he would '
                                'come running.']}],
  'name': 'come running',
  'summary': {}},
 {'definitions': [{'description': 'to run in order to escape from '
                                  'somebody/something',
                   'examples': []}],
  'name': 'run for it',
  'summary': {}},
 {'definitions': [{'description': 'to treat somebody badly and not worry about '
                                  'their feelings',
                   'examples': []}],
  'name': 'run roughshod over somebody',
  'summary': {'label': '(US English usually)'}},
 {'definitions': [{'description': 'working fully and correctly',
                   'examples': ['It will be a lot easier when we have the '
                                'database up and running.',
                                'We soon had the sound system up and '
                                'running.']}],
  'name': 'up and running',
  'summary': {}}]
```

### Other results

Return other similar results

```python
Word.other_results()
```

```python
[{'All matches': [{'id': 'run_2', 'name': 'run', 'wordform': 'noun'},
                  {'id': 'ladder_1#ladder_1__50',
                   'name': 'ladder',
                   'wordform': 'noun'},
                  {'id': 'ski-run#ski-run__15',
                   'name': 'ski run',
                   'wordform': 'noun'},
                  {'id': 'stand_1#stand_1__591',
                   'name': 'stand',
                   'wordform': 'verb'},
                  ...]},
 {'Phrasal verbs': [{'id': 'run-at',
                     'name': 'run at',
                     'wordform': 'phrasal verb'},
                    {'id': 'run-by',
                     'name': 'run by',
                     'wordform': 'phrasal verb'},
                    {'id': 'run-in_2',
                     'name': 'run in',
                     'wordform': 'phrasal verb'},
                    {'id': 'run-on',
                     'name': 'run on',
                     'wordform': 'phrasal verb'},
                    ...]},
 {'Idioms': [{'id': 'amok#amok__17', 'name': 'run amok'},
             {'id': 'dry_1#dry_1__330', 'name': 'run dry'},
             {'id': 'free_3#free_3__60', 'name': 'run free'},
             {'id': 'high_3#high_3__146', 'name': 'run high'},
             ...]}]
```

### All in 1

Return all information above in one function call

```python
Word.info()
```

```python
# Display the following info:
# word id
# wordform
# pronunciations
# definitions + examples
# idioms
# other_results
```

## License
**[BSD 3-Clauses](https://github.com/NearHuscarl/oxford-dictionary-api/blob/master/LICENSE.md)**
