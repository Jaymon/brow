# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os

from . import TestCase, testdata

from brow.core import Cookies, Cookie
from brow.compat import *


class CookiesTest(TestCase):
    def test_is_valid(self):
        b = Cookies("example.com")
        self.assertTrue(b.is_valid({"domain": ".example.com"}))
        self.assertFalse(b.is_valid({"domain": "foo.example.com"}))
        self.assertTrue(b.is_valid({"domain": "example.com"}))

        b = Cookies("foo.example.com")
        self.assertTrue(b.is_valid({"domain": ".example.com"}))
        self.assertFalse(b.is_valid({"domain": "example.com"}))
        self.assertTrue(b.is_valid({"domain": "foo.example.com"}))
        self.assertFalse(b.is_valid({"domain": "bar.example.com"}))


class CookieTest(TestCase):
    def test_cookiejar(self):
        #cd = cookies.SimpleCookie()
        #cd[b"foo"] = testdata.get_ascii()

        cj = cookiejar.CookieJar()
        tup = ("foo", testdata.get_ascii(), {}, {})
        class Request(object):
            def get_full_url(self):
                return "http://example.com/"
        c = cj._cookie_from_cookie_tuple(tup, Request())

        r = Cookie(c)
        self.assertEqual(tup[0], r["name"])
        self.assertEqual(tup[1], r["value"])
        self.assertEqual("example.com", r["domain"])

