# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os
import tempfile
import pickle
import logging

import requests

from . import environ
from .compat import *


logger = logging.getLogger(__name__)


class Cookie(dict):
    def __init__(self, cookie):
        if isinstance(cookie, cookiejar.Cookie):
            vals = {
                'domain': cookie.domain,
                'secure': cookie.secure,
                'value': cookie.value,
                'expiry': cookie.expires,
                'path': cookie.path,
                'httpOnly': False,
                'name': cookie.name,
            }

        else:
            vals = cookie

        super(Cookie, self).__init__(vals)


class Cookies(object):
    """This will write and read cookies for a Browser instance, calling Browser.location()
    will use this class to load cookies for the given domain if they are available

    https://www.quora.com/Is-there-a-way-to-keep-the-session-after-login-with-Selenium-Python
    http://stackoverflow.com/a/15058521/5006
    http://stackoverflow.com/questions/30791771/persistent-selenium-cookies-in-python
    https://groups.google.com/forum/#!topic/selenium-users/iHuoa5HTzzA

    alternative to cookies, creating a profile (Firefox specific which is why I didn't
    do it, so I could switch to chrome) http://stackoverflow.com/a/5595349/5006
    """
    @property
    def jar(self):
        """Returns all the cookies as a CookieJar file"""
        # https://github.com/kennethreitz/requests/blob/master/requests/packages/urllib3/response.py
        # http://docs.python-requests.org/en/latest/api/#api-cookies
        # http://docs.python-requests.org/en/master/_modules/requests/cookies/
        # http://docs.python-requests.org/en/master/user/quickstart/#cookies
        jar = requests.cookies.RequestsCookieJar()
        for c in self:
            name = c.pop("name")
            value = c.pop("value")
            c["rest"] = {"httpOnly": c.pop("httpOnly", None)}
            c["expires"] = c.pop("expiry", None)

            jar.set(name, value, **c)
        return jar

    @property
    def directory(self):
        return environ.CACHE_DIR

    @property
    def path(self):
        cookies_d = self.directory
        cookies_f = os.path.join(cookies_d, "cookies-{}.txt".format(self.domain))
        return cookies_f

    def __len__(self):
        return len(self.cookies)

    def __iter__(self):
        for cookie in self.cookies:
            yield cookie

    def append(self, cookie):
        c = Cookie(cookie)
        if self.is_valid(c):
            # NOTE -- so domain=.example.com fails when you try and set it back,
            # so override the domain
            c["domain"] = self.domain
            self.cookies.append(c)
        else:
            raise TypeError("Cookie domain {} does not match valid cookies domain {}".format(
                cookie["domain"],
                self.domain
            ))

    def is_valid(self, cookie):
        """Returns True if the cookie is valid for the current domain, false otherwise"""
        domain = self.domain
        cookie_domain = cookie["domain"]
        index = cookie_domain.rfind(domain)
        if index == 0:
            valid_cookie = True
        elif index == 1:
            valid_cookie = cookie_domain[index-1] == "."
        else:
            valid_cookie = False
            if cookie_domain[0] == ".":
                valid_cookie = domain.endswith(cookie_domain)
        return valid_cookie

    def load(self):
        cookies_f = self.path
        if os.path.isfile(cookies_f):
            #with codecs.open(cookies_f, encoding='utf-8', mode="rb") as f:
            logger.info("Loading cookies from: {}".format(cookies_f))
            with open(cookies_f, "rb") as f:
                self.cookies = pickle.load(f)

    def dump(self):
        """save the cookies in browser"""
        cookies_f = self.path
        logger.info("Dumping cookies to: {}".format(cookies_f))
        #with codecs.open(cookies_f, encoding='utf-8', mode="w+b") as f:
        with open(cookies_f, "w+b") as f:
            pickle.dump(self.cookies, f)

    def delete(self):
        """save the cookies in browser"""
        cookies_f = self.path
        logger.info("Deleting cookies: {}".format(cookies_f))
        os.unlink(cookies_f)

    def __init__(self, domain):
        self.domain = domain
        self.cookies = []


