# -*- coding: UTF-8 -*-

"""
 weblogin
 by Anarchintosh @ xbmcforums
 Copyleft (GNU GPL v3) 2011 onwards

 this example is configured for Fantasti.cc login
 See for the full guide please visit:
 http://forum.xbmc.org/showthread.php?p=772597#post772597


 USAGE:
 in your default.py put:

 import weblogin
 logged_in = weblogin.doLogin('a-path-to-save-the-cookie-to','the-username','the-password')

 logged_in will then be either True or False depending on whether the login was successful.
"""
import logging
import mechanize
import cookielib
import os, sys
import re
import urllib,urllib2
import cookielib
from BeautifulSoup import BeautifulSoup
from mechanize import ParseResponse, urlopen, urljoin, CookieJar, build_opener, install_opener, HTTPCookieProcessor, LWPCookieJar

### TESTING SETTINGS (will only be used when running this file independent of your addon)
# Remember to clear these after you are finished testing,
# so that your sensitive details are not in your source code.
# These are only used in the:  if __name__ == "__main__"   thing at the bottom of this script.
myusername = 'daniel.j.mijares@gmail.com'
mypassword = 'seminoles35'
#note, the cookie will be saved to the same directory as weblogin.py when testing

logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

browser = mechanize.Browser()
browser.set_debug_http(True)
#browser.set_debug_responses(True)
browser.set_debug_redirects(True)

def check_login(source,username):
    
    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = 'Welcome Back'

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False
    
def doLogin(cookiepath, username, password):

    print cookiepath
    #check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        print cookiepath
        #if the user supplied only a folder path, append on to the end of the path a filename.
        cookiepath = os.path.join(cookiepath,'cookies.lwp')
        
    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
        print cookiepath
    except:
        pass

    if username and password:

        #the url you will request to.
        login_url = 'http://www.yogaglo.com/eventcontroler.php'

        #the header used to pretend you are a browser
        header_string = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:24.0) Gecko/20100101 Firefox/24.0'
        #browser.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:24.0) Gecko/20100101 Firefox/24.0'
#), ('Connection', 'keep-alive')]
        browser.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:24.0) Gecko/20100101 Firefox/24.0'),
                    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                    ('Accept-Language', 'en-gb,en;q=0.5'),
                    ('Accept-Encoding', 'gzip,deflate'),
                    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
                    ('Keep-Alive', '115'),
                    ('Connection', 'keep-alive'),
                    ('DNT', '1')]
        #initiate the cookielib class
        #cj = cookielib.LWPCookieJar()
        cookies = cookielib.LWPCookieJar()
        browser.set_cookiejar(cookies)
        print cookies
        browser.set_handle_gzip(True)
        browser.set_handle_redirect(True)
        browser.set_handle_referer(True)
        browser.set_handle_robots(False)
        browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
        opener = build_opener(HTTPCookieProcessor(cookies))
        install_opener(opener)
# 
#         #install cookielib into the url opener, so that cookies are handled
#         opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# 
#         #do the login and get the response
#         response = opener.open(req)
#         source = response.read()
#         response.close()
#         response = urlopen("http://www.yogaglo.com/signin.php")
#         forms = ParseResponse(response, backwards_compat=False)
#         form = forms[0]
        browser.open("http://www.yogaglo.com/signin.php")
        browser.select_form(name="do_User__eventCheckIdentification")
        browser['fields[password]'] = password
        browser['fields[email]'] = username
        print browser.form
        response2 = browser.submit()
        source = response2.read()
#         form['fields[password]'] = "seminoles35"
#         form['fields[email]'] = "daniel.j.mijares@gmail.com"
#         source = urlopen(form.click()).read()
        #check the received html for a string that will tell us if the user is logged in
        #pass the username, which can be used to do this.
        login = check_login(source,username)

        #if login suceeded, save the cookiejar to disk
        if login == True:
            cookies.save(cookiepath , ignore_discard=True, ignore_expires=True)

        #return whether we are logged in or not
        return login
    
    else:
        return False

#code to enable running the .py independent of addon for testing
if __name__ == "__main__":
    if myusername is '' or mypassword is '':
        print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
    else:
        logged_in = doLogin(os.getcwd(),myusername,mypassword)
        print 'LOGGED IN:',logged_in
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        cookiepath = os.path.join(os.getcwd(),'cookies.lwp')
        cj.load(cookiepath , ignore_discard=True, ignore_expires=True)
        response = br.open("http://www.yogaglo.com/online-class-3174-Kathryns-Home-Practice.html")
        print response.read()
        