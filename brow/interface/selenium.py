# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import logging
import tempfile
import os
import json
import random

from .base import Browser as BaseBrowser
from ..core import Cookies

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions # webdriver.FirefoxOptions in >=3.8

#from selenium.webdriver.common.keys import Keys
# https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/common/exceptions.py
from selenium.common.exceptions import \
    NoSuchElementException, \
    WebDriverException, \
    NoSuchWindowException

from ..exception import ParseError

logger = logging.getLogger(__name__)


class Selenium(BaseBrowser):
    """This is a wrapper around selenium to make browsering from the command line easier

    link -- Selinium source -- https://github.com/SeleniumHQ/selenium/tree/master/py
    link -- https://pypi.python.org/pypi/selenium
    """
    @property
    def body(self):
        """return the body of the current page"""
        # http://stackoverflow.com/a/7866938/5006
        # http://stackoverflow.com/a/16114362/5006
        return self.interface.page_source

    @property
    def url(self):
        """return the current url"""
        # http://stackoverflow.com/questions/15985339/how-do-i-get-current-url-in-selenium-webdriver-2-python
        return self.interface.current_url

    @property
    def cookies(self):
        ret = Cookies(self.domain)
        # http://selenium-python.readthedocs.io/navigating.html#cookies
        for cookie in self.interface.get_cookies():
            try:
                ret.append(cookie)
            except TypeError:
                pass

        return ret if len(ret) else None

    def dump(self, prefix="dump", directory=None, basename=None):
        ret = []
        inter = self.interface
        try:
            basepath = self.dump_basepath(prefix, directory, basename)
            path = "{}.png".format(basepath)
            inter.get_screenshot_as_file(path)
            logger.debug("Dumped screenshot to {}".format(path))
            ret.append(path)
        except Exception as e:
            logger.warn(e, exc_info=True)
            pass

        ret.extend(super(Selenium, self).dump(prefix, directory))
        return ret

    def _location(self, url, ignore_cookies):
        inter = self.interface
        inter.get(url)

        if not ignore_cookies:
            domain = self.domain
            cookies = Cookies(domain)
            cookies.load()
            count = 0
            for count, cookie in enumerate(cookies, 1):
                # TODO -- firefox sets this and it was causing it to not set cookies
                # but I don't know why, I think it's probably bad to just get rid of this
                # so I should look at why it was failing
                cookie.pop("expiry", None)
                inter.add_cookie(cookie)
            logger.debug("Loaded {} cookies for {}".format(count, domain))

            # you have to re-request the url in order to have the cookies be passed,
            # this is because you can only load cookies for the current url
            inter.get(url)

    def element(self, css_selector, timeout=0):
        """wrapper around Selenium's css selector

        http://selenium-python.readthedocs.io/locating-elements.html
        https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/remote/webelement.py

        :param css_selector: str, used to select elements on the page
        :returns: the elements or None if nothing was found
        """
        ret = None
        inter = self.interface
        inter.implicitly_wait(timeout) # http://selenium-python.readthedocs.io/waits.html#implicit-waits
        try:
            ret = inter.find_element_by_css_selector(css_selector)

        except NoSuchElementException as e:
            pass
            #logger.error("Could not find an element with css selector: {}".format(css_selector))
            #self.handle_error(e)
            #raise ParseError(body=self.body, error=e)
        return ret

    def has_element(self, css_selector):
        ret = True
        try:
            self.interface.find_element_by_css_selector(css_selector)
        except NoSuchElementException as e:
            ret = False
        return ret

    #def element_for(self, css
#     def wait_for_element(self, css_selector, seconds):
#         # ??? -- not sure this is needed or is better than builtin methods
#         # http://stackoverflow.com/questions/26566799/selenium-python-how-to-wait-until-the-page-is-loaded
#         # http://selenium-python.readthedocs.io/waits.html#explicit-waits
#         elem = None
#         driver = self.browser
#         for count in range(seconds):
#             elem = driver.find_element_by_css_selector(css_selector)
#             if elem:
#                 break
#             else:
#                 time.sleep(1)
# 
#         return elem
# 
    def close(self):
        """quit the browser and power down the virtual display"""
        logger.debug("Closing down browser")
        try:
            self.interface.close()
            del self.interface
        except AttributeError:
            pass
        except Exception as e:
            logger.warn("Browser close failed with {}".format(e.message))
            pass


class ChromeBrowser(Selenium):
    @property
    def json(self):
        if self.has_element("pre"):
            element = self.element("pre")
            body = element.text
        else:
            body = self.body
        return json.loads(body)

    def _create_interface(self, options):
        # https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/remote/webdriver.py
        # http://www.guguncube.com/2983/python-testing-selenium-with-google-chrome
        # https://gist.github.com/addyosmani/5336747
        # http://blog.likewise.org/2015/01/setting-up-chromedriver-and-the-selenium-webdriver-python-bindings-on-ubuntu-14-dot-04/
        # https://sites.google.com/a/chromium.org/chromedriver/getting-started
        # http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium
        # https://intoli.com/blog/running-selenium-with-headless-chrome/

        # options: https://sites.google.com/a/chromium.org/chromedriver/capabilities
        # https://peter.sh/experiments/chromium-command-line-switches/
        options.setdefault("start-maximized", True)
        options.setdefault("disable-infobars", True)
        options.setdefault("--disable-extensions", True)
        options.setdefault("--headless", True)
        #options.setdefault("window-size", "1280x1024")

        opts = webdriver.ChromeOptions()
        for k, v in options.items():
            if v is True:
                opts.add_argument(k)
            elif v is False:
                pass # we ignore false options
            else:
                opts.add_argument("{}={}".format(k, v))


        # !!! this doesn't work in headless and it doesn't look like they are going
        # to fix that anytime soon
        # see: https://bugs.chromium.org/p/chromedriver/issues/detail?id=1925#c11
        #opts.add_experimental_option('prefs', {'intl.accept_languages': 'en-US,en'})
        # I might be able to get around this doing something like:
        # https://intoli.com/blog/making-chrome-headless-undetectable/
        # but not sure it's worth it

        inter = webdriver.Chrome(chrome_options=opts)
        # version: 

#         user_agent = " ".join([
#             "Mozilla/5.0", 
#             #"(X11; Linux x86_64)",
#             "(Macintosh; Intel Mac OS X 10_12_6)",
#             "AppleWebKit/537.36", 
#             "(KHTML, like Gecko)", 
#             "Chrome/{}".format(inter.capabilities['version']), # https://stackoverflow.com/a/12559477/5006
#             "Safari/537.36"
#         ])
#         opts.add_argument("user-agent={}".format(user_agent))
# 
#         # now get the driver again with a different useragent
#         inter = webdriver.Chrome(chrome_options=opts)


        #inter.implicitly_wait(10) # http://selenium-python.readthedocs.io/waits.html#implicit-waits
        return inter


class FirefoxBrowser(Selenium):
    @property
    def json(self):
        if self.has_element("pre"):
            element = self.element("pre")
            body = element.text

        elif self.has_element("plaintext"):
            element = self.element("plaintext")
            body = element.text

        else:
            body = self.body
        return json.loads(body)

    def _create_interface(self, options):

        options.setdefault("start-maximized", True)
        options.setdefault("disable-infobars", True)
        options.setdefault("--disable-extensions", True)

        opts = FirefoxOptions()
        #opts.set_headless() # in master but not in version on pypi
        # https://intoli.com/blog/running-selenium-with-headless-firefox/
        options["--headless"] = True
        os.environ['MOZ_HEADLESS'] = '1' # windows bug (just in case)

        for k, v in options.items():
            if v is True:
                opts.add_argument(k)
            elif v is False:
                pass # we ignore false options
            else:
                opts.add_argument("{}={}".format(k, v))

        #opts.add_experimental_option('prefs', {'intl.accept_languages': 'en-US,en'})

        # https://www.howtogeek.com/howto/internet/firefox/quick-tip-disable-favicons-in-firefox/
        opts.set_preference('browser.chrome.favicons', False)
        opts.set_preference('browser.chrome.site_icons', False)
        #opts.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0")

        inter = webdriver.Firefox(firefox_options=opts)

        # amazon will trigger a bot check if you request from Linux
        # https://myip.ms/browse/comp_browseragents/1/browserID/2962/browserID_A/1
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
            #"(X11; Linux x86_64)",
            "({}; rv:{})".format(random.choice(oses), inter.capabilities['browserVersion']),
            "Gecko/20100101", 
            "Firefox/{}".format(inter.capabilities['browserVersion']),
        ])
        # https://stackoverflow.com/questions/29916054/change-user-agent-for-selenium-driver
        opts.set_preference("general.useragent.override", user_agent)
        # now get the driver again with a different useragent
        inter.close()
        inter = webdriver.Firefox(firefox_options=opts)

        #inter.implicitly_wait(10) # http://selenium-python.readthedocs.io/waits.html#implicit-waits
        return inter

