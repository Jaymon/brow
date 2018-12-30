# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import


class ParseError(RuntimeError):
    """This gets raised any time Browser.element() fails to parse,
    it wraps NoSuchElementException"""
    def __init__(self, msg="", body="", error=None):
        if not msg:
            if error:
                msg = error.message

        self.body = body

        self.error = error
        super(ParseError, self).__init__(msg)


class RecoverableCrash(IOError):
    def __init__(self, e):
        self.error = e
        super(RecoverableCrash, self).__init__(e.message)

