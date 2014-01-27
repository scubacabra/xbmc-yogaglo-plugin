import xbmc
import xbmcaddon
import xbmcgui

import os
import urllib
import re

from xbmc_util import addDir, addDirs, eod, listItemResolvedUrl
from http import openUrl, openUrlWithCookie, login, check_login
from soup_crawler import SoupCrawler

class YogaGlo:
    plugin_name = "plugin.video.yogaglo"
    yoga_glo_base_url = "http://www.yogaglo.com"
    cookie_file = "yogaGloCookie.lwp"
    yoga_glo_sign_in_url = "http://www.yogaglo.com/signin.php"
    yoga_glo_login_url = "http://www.yogaglo.com/eventcontroler.php"

    def __init__(self, plugin, handle, plugin_params):
        print "YogaGlo -- args are %s, %s, %s" % (plugin, handle, plugin_params)
        self.xbmc_plugin = plugin
        self.xbmc_handle = handle
        self.addon = xbmcaddon.Addon(id=self.plugin_name)
        self.yoga_glo_plugin_parameters = plugin_params
        self.crawler = SoupCrawler(self.yoga_glo_base_url)
        # Dir where plugin settings and cache will be stored
        self.yoga_glo_addon_profile_path = xbmc.translatePath(
            self.addon.getAddonInfo('profile')).decode('utf-8')

        if not os.path.exists(self.yoga_glo_addon_profile_path):
            os.makedirs(self.yoga_glo_addon_profile_path)

        self.yoga_glo_cookie_path = os.path.join(
            self.yoga_glo_addon_profile_path,
            self.cookie_file)
        if not os.path.isfile(self.yoga_glo_cookie_path):
            print "YogaGlo -- No cookie found for %s, attempting to log on to YogaGlo with credentials" % self.yoga_glo_cookie_path
            self.yoga_glo_logged_in = self.yogaGloLogin()
        else:
            print "YogaGlo -- Found cookie... just trying to see if it is still a valid session"
            myaccount = openUrlWithCookie(
                "http://www.yogaglo.com/myaccounttoday.php",
                self.yoga_glo_cookie_path)
            self.yoga_glo_logged_in = check_login(myaccount)
            if not self.yoga_glo_logged_in:
                print "YogaGlo -- Cookie PHP session seems invalid...logging in again"
                self.yoga_glo_logged_in = self.yogaGloLogin()

        print "YogaGlo -- DONE WITH INIT"

    def getYogaGloCategory(self, category):
        if category == "YOTD":
            return 1
        elif category == "Teacher":
            return 2
        elif category == "Style":
            return 3
        elif category == "Level":
            return 4
        elif category == "Duration":
            return 5


    def buildClassesMenu(self):
        #list of items for xbmc to handle (you get a progress bar with this!)
        itemList = []
        classesInformation = self.crawler.get_classes(
            self.yoga_glo_plugin_parameters['yogagloUrl'])
        for classInfo in classesInformation:
            li = xbmcgui.ListItem(label=classInfo['title'],
                                  label2=classInfo['secondLabel'],
                                  iconImage=classInfo['coverPicUrl'])
            li.setInfo('video', {'title': classInfo['title'],
                                 'plot': classInfo['plot'],
                                 'Duration': classInfo['duration'],
                                 'plotoutline': classInfo['secondLabel'],
                                 'tagline': classInfo['teacher'],
                                 'genre': "Yoga"})
            li.setProperty('IsPlayable', 'true')
            callbackParams = { 'yogaCategory' : 
                               self.yoga_glo_plugin_parameters['yogaCategory'],
                               'yogagloUrl' : classInfo['url'], 'play': 1}
            print classInfo['url']
            callBackUrl = self.xbmc_plugin + "?" + urllib.urlencode(callbackParams)
            print callBackUrl
            itemList.append((callBackUrl, li, False))

        addDirs(self.xbmc_handle, itemList)
        eod(self.xbmc_handle)


    def buildYogaCategoryMenu(self):
        print "YogaGlo -- Building category menu just selected"
        itemList = []
        menu = self.crawler.get_yoga_glo_navigation_information(
            self.yoga_glo_plugin_parameters['yogaCategory'])
        print menu

        for item in menu:
            try:
                title, ygUrl, imageUrl = item
            except ValueError:
                title, ygUrl = item
                imageUrl = None

            callbackParams = { 'yogaCategory' :
                               self.yoga_glo_plugin_parameters['yogaCategory'],
                               'yogagloUrl' : ygUrl }
            url = self.xbmc_plugin + "?" + urllib.urlencode(callbackParams)
            if imageUrl is not None:
                li = xbmcgui.ListItem(label=title, iconImage=imageUrl)
            else:
                li = xbmcgui.ListItem(label=title, iconImage="Default.png")

            itemList.append((url, li, True))

        addDirs(self.xbmc_handle, itemList)
        eod(self.xbmc_handle)
        print "YogaGlo -- category menu built"

    def buildTopLevelMenu(self):
        print "YogaGlo -- building initial Menu (teachers, style, level, duration) selection"
        itemList = []
        for category in ["Teacher", "Style", "Level", "Duration", "YOTD"]:
            title = category
            description = "Select A" + title
            callbackParams = { 'yogaCategory' : 
                               self.getYogaGloCategory(category) }
            if category == "YOTD": #special title and info for this!
                info = self.crawler.get_yoga_of_the_day_title_and_info()
                title = info['title']
                description = info['information']
                callbackParams['yogagloUrl'] = self.yoga_glo_base_url

            url = self.xbmc_plugin + "?" + urllib.urlencode(callbackParams)
            li = xbmcgui.ListItem(label=title, label2=description,
                                  iconImage="Default.png")
            itemList.append((url, li, True))

        addDirs(self.xbmc_handle, itemList)
        eod(self.xbmc_handle)
        print "YogaGlo -- initial Menu built"

    def playYogaGloVideo(self):
        print urllib.unquote(self.yoga_glo_addon_profile_path)
        vidPage = self.yoga_glo_plugin_parameters['yogagloUrl']
        #logged in, get full video at highest resolution
        if self.yoga_glo_logged_in:
            html = openUrlWithCookie(vidPage, self.yoga_glo_cookie_path)
            print re.compile(".*url: '([^']*)'").findall(html)
            swfUrl = re.compile(".*url: '([^']*)'").findall(html)[0]
            print re.compile('url: "([^"]*)"').findall(html)
            playpath = urllib.unquote(re.compile(
                'url: "([^"]*)"').findall(html)[0])
            print re.compile(
                "netConnectionUrl:\s+'([^']*)'").findall(html)[0]
            rtmpUrl = re.compile(
                "netConnectionUrl:\s+'([^']*)'").findall(html)[0]
        else: #not logged in, get preview clip instead
            html = openUrl(self.yoga_glo_base_url + vidPage)
            playpath = urllib.unquote(
                re.compile("url: '(mp4[^']*)'").findall(html)[0])
            swfUrl = re.compile("url:\s+'([^mp4]+[^']*)'").findall(html)[0]
            rtmpUrl = re.compile(
                "netConnectionUrl:\s+'([^']*)'").findall(html)[0]

        print (playpath, swfUrl, rtmpUrl)
        liz = xbmcgui.ListItem(label="DANIEL", path=rtmpUrl + "/" + playpath)
        liz.setProperty('PlayPath', playpath);
        liz.setProperty('SWFPlayer', swfUrl);
        listItemResolvedUrl(self.xbmc_handle, liz)

    def processParameters(self):
        print "YogaGlo parameters: '%s'", self.yoga_glo_plugin_parameters

        if 'play' in self.yoga_glo_plugin_parameters:
            self.playYogaGloVideo()
            return

        if 'yogagloUrl' in self.yoga_glo_plugin_parameters:
            self.buildClassesMenu()
            return

        if 'yogaCategory' in self.yoga_glo_plugin_parameters:
            self.buildYogaCategoryMenu()
            return

        print "Building the Top Menu"
        self.buildTopLevelMenu()

    def yogaGloLogin(self):
        username = self.addon.getSetting('username')
        password = self.addon.getSetting('password')
        if username != "" and password != "":
            print "YogaGlo -- found credentials for username and password, attempting to logon"
            loggedOn = login(self.yoga_glo_cookie_path, username, password,
                             self.yoga_glo_sign_in_url)
            print "YogaGlo -- logon was %s", "Successful" if loggedOn else "UnSuccessful"
            return loggedOn

        #TODO show error dialog
        print "YogaGlo -- One of either Username or Password is blank, cannot log on"
        return False
