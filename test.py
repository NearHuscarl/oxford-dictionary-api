import pprint
from oxford import Word


def main():
    # run: multiple namespaces
    # loud: no namespace
    Word.get('run')

    pprint.pprint(Word.info())

    # pprint.pprint(Word.id())
    # pprint.pprint(Word.name())
    # pprint.pprint(Word.wordform())
    # pprint.pprint(Word.pronunciations())
    # pprint.pprint(Word.definitions())
    # pprint.pprint(Word.examples())
    # pprint.pprint(Word.definitions(full=True))
    # pprint.pprint(Word.idioms())
    # pprint.pprint(Word.other_results())


if __name__ == '__main__':
    main()
