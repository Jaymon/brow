# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os

from . import MultiInterfaceTestCase, testdata


class InterfaceTest(MultiInterfaceTestCase):
    def test_location(self):
        with testdata.create_fileserver("foo") as server:
            browser = self.create_browser()
            browser.location(server)
            self.assertTrue("foo" in browser.body)
            browser.close()

    def test_element(self):
        body = '<html><head></head><body><p class="foo">text</p></body></html>'
        with testdata.create_fileserver(body) as server:
            with self.browser_cls.session() as b:
                b.location(server)

                self.assertTrue(b.has_element("p.foo"))
                elem = b.element("p.foo")
                self.assertIsNotNone(elem)

                self.assertFalse(b.has_element("p.bar"))
                elem = b.element("p.bar")
                self.assertIsNone(elem)

    def test_cookies(self):
        cookies = {
            "foo": testdata.get_ascii(),
            "bar": testdata.get_ascii(),
        }
        server = testdata.create_cookieserver(cookies)
        with server:
            with self.browser_cls.session() as b:
                b.location(server, ignore_cookies=True)
                #pout.v(b.response)
                bcookies = b.cookies
                self.assertEqual(len(cookies), len(bcookies))
                bcookies.dump()

            with self.browser_cls.session() as b:
                b.location(server)
                ret = b.json
                for name, val in cookies.items():
                    self.assertEqual(val, ret["read_cookies"][name]["value"])

    def test_session(self):
        with testdata.create_fileserver("foo") as server:
            with self.browser_cls.session() as browser:
                browser.location(server)
                self.assertTrue("foo" in browser.body)

    def test_session_error(self):
        with testdata.create_fileserver("foo") as server:
            try:
                with self.browser_cls.session() as b:
                    raise KeyError("blah")
            except KeyError:
                pass

            try:
                with self.browser_cls.session() as b:
                    b.location(server)
                    raise KeyError("blah")
            except KeyError:
                pass

    def test_dump(self):
        with testdata.create_fileserver(testdata.get_words()) as server:
            with self.browser_cls.session() as browser:
                browser.location(server)
                ret = browser.dump()
                for path in ret:
                    self.assertTrue(os.path.isfile(path))

