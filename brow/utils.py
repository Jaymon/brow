# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import


from bs4 import BeautifulSoup

from . import environ


class Soup(BeautifulSoup):
    """Small wrapper around Beautiful Soup that uses an environment setting to pick
    the best parser"""
    # https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/bs4/__init__.py
    # https://www.crummy.com/software/BeautifulSoup/
    # docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    # bs4 codebase: http://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/files
    def __init__(self, markup="", features=None, *args, **kwargs):
        if not features:
            features = environ.HTML_PARSER
        super(Soup, self).__init__(markup, features, *args, **kwargs)

