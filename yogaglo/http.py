import urllib2
from urlparse import urljoin

import cookielib
import mechanize
from mechanize import HTTPCookieProcessor

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
    print cookiePath

    #delete any old version of the cookie file
    try:
        os.remove(cookiePath)
        print cookiePath
    except:
        pass

    browser = openUrl(signinUrl, cookiePath, True)
    browser.select_form(name="do_User__eventCheckIdentification")
    browser['fields[password]'] = password
    browser['fields[email]'] = username
    #print browser.form
    response2 = browser.submit()
    print response2.info()
    print response2.geturl()
    source = response2.read()
    login = check_login(source)
    #if login suceeded, save the cookiejar to disk, no expiration to set
    if login == True:
        cookies.save(cookiePath, ignore_discard=True)

    #return whether we are logged in or not
    return login

def check_login(source):

    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = 'Welcome Back'

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False

def convert_relative_to_absolute_url(base_url, relative_url):
    # may be unicode, need utf8 encoding
    utf8_relative_url = relative_url.encode('utf-8')
    # percent encode relative url portion, it may have utf8 characters
    # open url can't read those
    url_encoded_relative_url = urllib2.quote(utf8_relative_url)
    return urljoin(base_url, url_encoded_relative_url)

