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

