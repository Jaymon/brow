# Brow

Control a browser using python.


## What do I need to use this?

Brow uses Selenium and headless Chrome or headless Firefox.

### Installing Selenium python bindings

```
pip install selenium
```


### Installing Firefox on Ubuntu using bash

These are the versions that I used:

    $ firefox --version
    Mozilla Firefox 57.0

    $ geckodriver --version
    geckodriver 0.19.1

First Install Firefox:

```bash
apt-get install --no-install-recommends firefox
```

Then you need the Gecko Driver:

```bash
LATEST=wget -O - https://github.com/mozilla/geckodriver/releases/latest 2>&1 | grep "Location:" | grep --only-match -e "v[0-9\.]\+"
wget "https://github.com/mozilla/geckodriver/releases/download/${LATEST}/geckodriver-${LATEST}-linux64.tar.gz"
tar -x geckodriver -zf geckodriver-${LATEST}-linux64.tar.gz -O > /usr/local/bin/geckodriver
chmod +x /usr/local/bin/geckodriver
```


### Installing Chrome on Ubuntu using bash

These are the versions I used:

    $ google-chrome --version
    Google Chrome 62.0.3202.94

    $ chromedriver --version
    ChromeDriver 2.33.506092 (733a02544d189eeb751fe0d7ddca79a0ee28cce4)

```bash
apt-get install --no-install-recommends libxss1 libappindicator1 libindicator7 
apt-get install --no-install-recommends gconf-service libasound2 libnspr4 libnss3-dev
apt-get install --no-install-recommends libpango1.0-0 xdg-utils fonts-liberation
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome*.deb
```

Now install the Chrome Driver:

```bash
apt-get install unzip
LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip
unzip chromedriver_linux64.zip && ln -s $PWD/chromedriver /usr/local/bin/chromedriver
```

You can verify Chrome headless works by running:

    $ google-chrome --headless "http://marcyes.com"

If you didn't get any errors then it is working.


## I've installed a browser, now what do I do?

Let's request something:

```python
from brow.interface.selenium import FirefoxBrowser as Browser
#from brow.interface.selenium import ChromeBrowser as Browser

with Browser.session() as b:
    b.load("http://marcyes.com")
    print(b.body)

    # follow a link
    css_selector = "a#some_id"
    elem = b.element(css_selector)
    elem.click()
    print(b.url) # will now be whatever elem had in href
```


### Handling Cookies

Cookies are loaded automatically if they have been dumped

```python
from brow.interface.selenium import FirefoxBrowser as Browser

with Browser.session() as b:
    b.load("http://google.com")

    # save the cookies
    b.cookies.dump()

with Browser.session() as b:
    # cookies will be automatically loaded
    b.load("http://google.com")

with Browser.session() as b:
    # cookies will be ignored
    b.load("http://google.com", ignore_cookies=True)
```

That's all there is to it.


## Installation

use pip:

    $ pip install brow

Or be bleeding edge:

    $ pip install --upgrade "git+https://github.com/Jaymon/brow#egg=brow"


