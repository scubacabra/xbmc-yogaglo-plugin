import urllib2
import gzip
import StringIO

import cookielib
import mechanize

import os, re

from BeautifulSoup import BeautifulSoup
from mechanize import HTTPCookieProcessor

def openUrl(url):
    #create an opener
    opener = urllib2.build_opener()

    #Add useragent, sites don't like to interact with scripts
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:24.0) Gecko/20100101 Firefox/24.0'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'en-gb,en;q=0.5'),
        ('Accept-Encoding', 'gzip,deflate'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
        ('Cache-Control', 'max-age=0'),
        ]
 
    resp = opener.open(url)
 
    # Compressed (gzip) response...
    if resp.headers.get( "content-encoding" ) == "gzip":
            htmlGzippedData = resp.read()
            stringIO        = StringIO.StringIO( htmlGzippedData )
            gzipper         = gzip.GzipFile( fileobj = stringIO )
            htmlData        = gzipper.read()
    else :
            htmlData = resp.read()
 
    resp.close()
     
    # Return html
    return htmlData

def openUrlWithCookie(url, cookie):
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    cj.load(cookie , ignore_discard=True, ignore_expires=True)
    response = br.open(url)
    html = response.read()
    return html

def login(cookiePath, username, password, signinUrl):
    print cookiePath

    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
        print cookiepath
    except:
        pass

    browser = mechanize.Browser()
    cookies = cookielib.LWPCookieJar()
    browser.set_cookiejar(cookies)
    browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
    opener = mechanize.build_opener(HTTPCookieProcessor(cookies))
    mechanize.install_opener(opener)
    browser.open(signinUrl)
    browser.select_form(name="do_User__eventCheckIdentification")
    browser['fields[password]'] = password
    browser['fields[email]'] = username
    print browser.form
    response2 = browser.submit()
    source = response2.read()
    login = check_login(source,username)
    #if login suceeded, save the cookiejar to disk
    if login == True:
        cookies.save(cookiePath , ignore_discard=True, ignore_expires=True)

    #return whether we are logged in or not
    return login

def check_login(source,username):

    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = 'Welcome Back'

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False

