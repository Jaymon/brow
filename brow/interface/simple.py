# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import logging
import random

import requests

from .base import Browser as BaseBrowser
from ..core import Cookies, Cookie


logger = logging.getLogger(__name__)


class SimpleBrowser(BaseBrowser):
    @property
    def body(self):
        body = self.response.content
        if body:
            encoding = self.response.encoding
            if not encoding:
                encoding = "utf-8"
            body = body.decode(encoding)
        return body

    @property
    def url(self):
        """return the current url"""
        # http://stackoverflow.com/questions/15985339/how-do-i-get-current-url-in-selenium-webdriver-2-python
        return self.response.url

    @property
    def cookies(self):
        """Return the cookies for the current domain"""
        cookies = Cookies(self.domain)
        for cookie in self.response.cookies:
            cookies.append(cookie)
        return cookies

    def _create_interface(self, options):
        # http://docs.python-requests.org/en/latest/user/advanced/#session-objects
        inter = requests.Session()
        inter.headers.update(self.get_headers())
        return inter

    def _location(self, url, ignore_cookies):
        inter = self.interface
        if not ignore_cookies:
            domain = self.domain
            cookies = Cookies(domain)
            cookies.load()
            inter.cookies = cookies.jar
            logger.debug("Loaded {} cookies for {}".format(len(cookies), domain))

        self.response = inter.get(url)

    def __init__(self, *args, **kwargs):
        self.domains = set()
        super(SimpleBrowser, self).__init__(*args, **kwargs)

    def element(self, css_selector):
        soup = self.soup
        return soup.select_one(css_selector)

    def has_element(self, css_selector):
        elem = self.element(css_selector)
        return True if elem else False

    def get_headers(self):
        """Return headers that will make this look like it is coming from the actual
        browser"""
        raise NotImplementedError()


class SimpleFirefoxBrowser(SimpleBrowser):
    def get_headers(self):
        # TODO -- figure out a better way to set the firefox version, I could run
        # `firefox --version` but I'm not sure that's ideal or works across everything,
        # so right now I'm just going to hard code it

        version = "57.0"
        oses = [
            "Windows NT 6.3", # Windows 8.1
            "Macintosh; Intel Mac OS X 10.12",
            "Macintosh; Intel Mac OS X 10.13",
            "Windows NT 6.3; Win64; x64", # Windows 8.1 x64
            "Windows NT 6.1; Win64; x64", # Windows 7 x64
            "Windows NT 10.0; Win64; x64", # Windows 10 x64
        ]
        user_agent = " ".join([
            "Mozilla/5.0", 
            "({}; rv:{})".format(random.choice(oses), version),
            "Gecko/20100101", 
            "Firefox/{}".format(version),
        ])

        return {
            "accept-language": "en-US,en;q=0.5",
            "accept-encoding": "gzip, deflate",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "user-agent": user_agent,
            "connection": "keep-alive",
            "upgrade-insecure-requests": "1",
        }


class SimpleChromeBrowser(SimpleBrowser):
    def get_headers(self):

        version = "62.0.3202.94"
        oses = [
            "Windows NT 6.3", # Windows 8.1
            "Macintosh; Intel Mac OS X 10_12_6",
            "Macintosh; Intel Mac OS X 10_13_1",
            "Windows NT 6.3; Win64; x64", # Windows 8.1 x64
            "Windows NT 6.1; Win64; x64", # Windows 7 x64
            "Windows NT 10.0; Win64; x64", # Windows 10 x64
        ]

        user_agent = " ".join([
            "Mozilla/5.0", 
            "({})".format(random.choice(oses)),
            "AppleWebKit/537.36", 
            "(KHTML, like Gecko)", 
            "Chrome/{}".format(version),
            "Safari/537.36"
        ])

        return {
            "accept-language": "en-US,en;q=0.8",
            "accept-encoding": "gzip, deflate, sdch, br",
            "connection": "keep-alive",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "upgrade-insecure-requests": "1",
            "user-agent": user_agent,
        }

