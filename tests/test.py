import pytest
import requests
import time
from oxford import Word, WordNotFound

max_attempt = 10
connection_timeout = 10

with open("test_data.txt") as file:
    words = [line.rstrip() for line in file]


@pytest.mark.parametrize("word", words)
def test_get_word(word):
    attempt = 1
    connection_error = True
    while connection_error:
        assert attempt <= max_attempt
        connection_error = False
        try:
            Word.get(word)

            Word.info()
            Word.id()
            Word.name()
            Word.wordform()
            Word.pronunciations()
            Word.definitions()
            Word.examples()
            Word.definitions(full=True)
            Word.idioms()
            Word.other_results()
        except WordNotFound:
            pass
        except requests.exceptions.ConnectionError:
            connection_error = True
            attempt += 1
            time.sleep(connection_timeout)


