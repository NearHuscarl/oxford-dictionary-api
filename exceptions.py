#!/bin/env python

""" Internet connection related exceptions """

# pylint: disable=unused-import
# pylint: disable=redefined-builtin
from requests import ConnectionError
from requests.exceptions import HTTPError, Timeout
