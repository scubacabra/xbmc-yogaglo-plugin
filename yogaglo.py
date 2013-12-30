import xbmc
import xbmcaddon
import xbmcgui

from xbmcUtil import addDir
from xbmcUtil import addDirs
from xbmcUtil import eod
from xbmcUtil import listItemResolvedUrl
from xbmcUtil import getXbmcInputParameters

from http import openUrl
from http import openUrlWithCookie
from http import login
from http import check_login

from SoupCrawler import SoupCrawler
import os
import urllib
import re

class YogaGlo:
    pluginName = "plugin.video.yogaglo"
    baseUrl = "http://www.yogaglo.com"
    cookieFile = "yogaGloCookie.lwp"
    yogaGloSignInUrl = "http://www.yogaglo.com/signin.php"
    yogaGloLoginUrl = "http://www.yogaglo.com/eventcontroler.php"

    def __init__(self, plugin, handle, params):
        print "YogaGlo -- args are %s, %s, %s" % (plugin, handle, params)
        self.xbmcPlugin = plugin
        self.xbmcHandle = handle
        self.addon = xbmcaddon.Addon(id=self.pluginName)
        self.crawler = SoupCrawler(self.baseUrl) # Soup Crawler to get info

        # Dir where plugin settings and cache will be stored
        self.addonProfilePath = xbmc.translatePath(self.addon.getAddonInfo('profile')).decode('utf-8')
        if not os.path.exists(self.addonProfilePath):
            os.makedirs(self.addonProfilePath)

        self.cookiePath = os.path.join(self.addonProfilePath, self.cookieFile)
        if not os.path.isfile(self.cookiePath):
            print "YogaGlo -- No cookie found for %s, attempting to log on to YogaGlo with credentials" % self.cookiePath
            self.yogaGloLoggedIn = self.yogaGloLogin()
        else:
            print "YogaGlo -- Found cookie... just trying to see if it is still a valid session"
            myaccount = openUrlWithCookie("http://www.yogaglo.com/myaccounttoday.php", self.cookiePath)
            self.yogaGloLoggedIn = check_login(myaccount)
            if not self.yogaGloLoggedIn:
                print "YogaGlo -- Cookie PHP session seems invalid...logging in again"
                self.yogaGloLoggedIn = self.yogaGloLogin()

        self.pluginParameters = getXbmcInputParameters(params)
        
        print "YogaGlo -- DONE WITH INIT"



    def getYogaGloCategory(self, category):
        if category == "Teacher":
            return 2
        elif category == "Style":
            return 3
        elif category == "Level":
            return 4
        elif category == "Duration":
            return 5


    def buildClassesMenu(self):
        itemList = [] #list of items for xbmc to handle (you get a progress bar with this!)
        classesInformation = self.crawler.getClassesInformation(self.pluginParameters['yogagloUrl'])
        for classInfo in classesInformation:
            li = xbmcgui.ListItem(label=classInfo['title'], label2=classInfo['secondLabel'], iconImage=classInfo['coverPicUrl'])
            li.setInfo('video', {'title': classInfo['title'],
                                 'plot': classInfo['plot'],
                                 'Duration': classInfo['duration'],
                                 'plotoutline': classInfo['secondLabel'],
                                 'tagline': classInfo['teacher'],
                                 'genre': "Yoga"})
            li.setProperty('IsPlayable', 'true')
            callbackParams = { 'yogaCategory' : self.pluginParameters['yogaCategory'], 'yogagloUrl' : classInfo['url'], 'play': 1}
            callBackUrl = self.xbmcPlugin + "?" + urllib.urlencode(callbackParams)
            itemList.append((callBackUrl, li, False))

        addDirs(self.xbmcHandle, itemList)
        eod(self.xbmcHandle)


    def buildYogaCategoryMenu(self):
        print "YogaGlo -- Building category menu just selected"
        itemList = []
        ygCategory = self.pluginParameters['yogaCategory']
        menu = crawler.getNavigationInformation(ygCategory)
        print menu

        for item in menu:
            try:
                title, ygUrl, imageUrl = item
            except ValueError:
                title, ygUrl = item
                imageUrl = None

            callbackParams = { 'yogaCategory' : ygCategory, 'yogagloUrl' : ygUrl }
            url = self.xbmcPlugin + "?" + urllib.urlencode(callbackParams)
            if imageUrl is not None:
                li = xbmcgui.ListItem(label=title, iconImage=imageUrl)
            else:
                li = xbmcgui.ListItem(label=title, iconImage="Default.png")
                
            itemList.append((url, li, True))
            
        addDirs(self.xbmcHandle, itemList)
        eod(self.xbmcHandle)
        print "YogaGlo -- category menu built"
        
    def buildTopLevelMenu(self):
        print "YogaGlo -- building initial Menu (teachers, style, level, duration) selection"
        itemList = []
        for category in ["Teacher", "Style", "Level", "Duration"]:
            label = "Select A " + category
            print label
            callbackParams = { 'yogaCategory' : self.getYogaGloCategory(category) }
            print callbackParams
            url = self.xbmcPlugin + "?" + urllib.urlencode(callbackParams)
            li = xbmcgui.ListItem(label=category, label2=label, iconImage="Default.png")
            itemList.append((url, li, True))

        addDirs(self.xbmcHandle, itemList)
        eod(self.xbmcHandle)
        print "YogaGlo -- initial Menu built"
            
                                 
    def playYogaGloVideo(self):
        print urllib.unquote(self.addonProfilePath)
        logged_in = False
        vidPage = self.pluginParameters['yogagloUrl']
        if not vidPage[0] == "/":
            vidPage = "/" + vidPage
            print self.yogaGloLoggedIn
            if self.yogaGloLoggedIn: #logged in, get full video at highest resolution
                html = openUrlWithCookie(self.baseUrl + vidPage, self.cookiePath)
                print re.compile(".*url: '([^']*)'").findall(html)
                swfUrl = re.compile(".*url: '([^']*)'").findall(html)[0]
                print re.compile('url: "([^"]*)"').findall(html)
                playpath = urllib.unquote(re.compile('url: "([^"]*)"').findall(html)[0])
                print re.compile("netConnectionUrl:\s+'([^']*)'").findall(html)[0]
                rtmpUrl = re.compile("netConnectionUrl:\s+'([^']*)'").findall(html)[0]
            else: #not logged in, get preview clip instead
                html = openUrl(self.baseUrl + vidPage)
                playpath = urllib.unquote(re.compile("url: '(mp4[^']*)'").findall(html)[0])
                swfUrl = re.compile("url:\s+'([^mp4]+[^']*)'").findall(html)[0]
                rtmpUrl = re.compile("netConnectionUrl:\s+'([^']*)'").findall(html)[0]
                
        print (playpath, swfUrl, rtmpUrl)
        liz = xbmcgui.ListItem(label="DANIEL", path=rtmpUrl + "/" + playpath)
        liz.setProperty('PlayPath', playpath);
        liz.setProperty('SWFPlayer', swfUrl);
        listItemResolvedUrl(self.xbmcHandle, liz)

    def processParameters(self):
        print "YogaGlo -- Processing Parameters %s", self.pluginParameters
        if not 'yogaCategory' in self.pluginParameters:
            print "Building the Top Menu"
            self.buildTopLevelMenu()
        else:
            if not 'yogagloUrl' in self.pluginParameters:
                self.buildYogaCategoryMenu()
            else:
                if not 'play' in self.pluginParameters:
                    self.buildClassesMenu()
                else:
                    self.playYogaGloVideo()

    def yogaGloLogin(self):
        username = self.addon.getSetting('username')
        password = self.addon.getSetting('password')
        if username != "" and password != "":
            print "YogaGlo -- found credentials for username and password, attempting to logon"
            loggedOn = login(self.cookiePath, username, password, self.yogaGloSignInUrl)
            print "YogaGlo -- logon was %s", "Successful" if loggedOn else "UnSuccessful"
            return loggedOn

        print "YogaGlo -- One of either Username or Password is blank, cannot log on" #TODO show error dialog
        return False
