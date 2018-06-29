# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os
from distutils import dir_util
import tempfile


CACHE_DIR = os.environ.get("BROW_CACHE_DIR", "")
if not CACHE_DIR:
    CACHE_DIR = os.path.join(tempfile.gettempdir(), "brow")
else:
    CACHE_DIR = os.path.abspath(os.path.expanduser(CACHE_DIR))
if not os.path.isdir(CACHE_DIR):
    dir_util.mkpath(CACHE_DIR)


# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#parser-installation
HTML_PARSER = os.environ.get("BROW_HTML_PARSER", "")
if not HTML_PARSER:
    HTML_PARSER = "html.parser"
    try:
        import lxml
        HTML_PARSER = "lxml"
    except ImportError:
        try:
            import html5lib
            HTML_PARSER = "html5lib"
        except ImportError:
            pass


