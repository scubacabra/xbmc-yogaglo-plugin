import urllib2
from urlparse import urljoin

import cookielib
import mechanize
from mechanize import HTTPCookieProcessor
from xbmc import log, LOGDEBUG
import os
import re

def openUrl(url, cookie=None, login=False):
    browser = mechanize.Browser()
    browser.addheaders = [
        ('User-Agent',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:24.0) Gecko/20100101 Firefox/24.0'),
        ('Accept',
         'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'en-gb,en;q=0.5'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
        ('Cache-Control', 'max-age=0'),
    ]

    #Experimental?
    # browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
    
    if not cookie is None:
	cj = cookielib.LWPCookieJar()
	browser.set_cookiejar(cj)
	opener = mechanize.build_opener(HTTPCookieProcessor(cj))
	mechanize.install_opener(opener)
	
	# trying to login, no cookie, must return browser so it can follow the
	# login url
	if login is True:
		browser.open(url)
		return browser
		
	# can't set to expire, can't read when this particular cookie expires
	cj.load(cookie , ignore_discard=True)

    return browser.open(url).read()


def login(cookiePath, username, password, signinUrl):
    #delete any old version of the cookie file
    if os.path.exists(cookiePath):
	log("cookie %s exists, deleting to aquire new cookie" % (cookiePath), LOGDEBUG)
        os.remove(cookiePath)

    browser = openUrl(signinUrl, cookiePath, True)
    browser.select_form(name="do_User__eventCheckIdentification")
    browser.form.set_all_readonly(False) # yg and mechanize not playing nice, need this
    browser['fields[password]'] = password
    browser['fields[email]'] = username
    browser['mydb_events[210]'] = 'do_User->eventSetSessionVariable' # not set right in post, forcing it now
    submit = browser.submit()
    homepage = submit.read()

    #if login suceeded, save the cookiejar to disk, no expiration to set
    if check_login(homepage) == True:
        browser._ua_handlers['_cookies'].cookiejar.save(cookiePath, ignore_discard=True)
        return True

    # failed login
    return False

def check_login(source):
    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = 'Welcome Back'

    #search for the string in the html, without caring about upper or lower case
    # if string is found, log in successful
    if re.search(logged_in_string, source, re.IGNORECASE):
	log("YogaGlo -- logged in to yogaglo!", LOGDEBUG)
	return True

    return False

def convert_relative_to_absolute_url(base_url, relative_url):
    # may be unicode, need utf8 encoding
    utf8_relative_url = relative_url.encode('utf-8')
    # percent encode relative url portion, it may have utf8 characters
    # open url can't read those
    url_encoded_relative_url = urllib2.quote(utf8_relative_url)
    return urljoin(base_url, url_encoded_relative_url)

