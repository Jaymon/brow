# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
from unittest import TestCase

import testdata

from brow.interface.simple import SimpleBrowser
from brow.interface.selenium import FirefoxBrowser, ChromeBrowser
from brow.interface.simple import SimpleFirefoxBrowser, SimpleChromeBrowser


testdata.basic_logging()


class MultiInterfaceTestCase(TestCase):
    """This will run all the tests with multple environments (eg, both SQLite and Postgres)"""

    browser_cls = None
    browser_instances = []

#     @classmethod
#     def setUpClass(cls):
#         """make sure there is a default interface for any class"""
#         for i in cls.create_interfaces():
#             i.delete_tables(disable_protection=True)
#             prom.set_interface(i)
# 
#     @classmethod
#     def tearDownClass(cls):
#         for browser in cls.browser_instances:
#             browser.close()
#         cls.browser_instances = []

    def create_browser(self, options=None):
        instance = self.browser_cls(options=options)
        type(self).browser_instances.append(instance)
        return instance

    def run(self, *args, **kwargs):
        for bc in [ChromeBrowser, FirefoxBrowser, SimpleFirefoxBrowser, SimpleChromeBrowser]:
        #for bc in [ChromeBrowser]:
        #for bc in [FirefoxBrowser]:
        #for bc in [SimpleFirefoxBrowser]:
            self.browser_cls = bc
            super(MultiInterfaceTestCase, self).run(*args, **kwargs)

            # clean up any stray browsers, just in case
            for browser in type(self).browser_instances:
                browser.close()
            type(self).browser_instances = []

