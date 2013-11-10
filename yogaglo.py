from BeautifulSoup import BeautifulSoup

import xbmc
import xbmcaddon

import urllib
import re

from xbmcUtil import addDir
from xbmcUtil import addDirs
from xbmcUtil import eod
from xbmcUtil import listItemResolvedUrl
from xbmcUtil import getXbmcInputParameters

import xbmcgui

from http import openUrl
from http import openUrlWithCookie
from http import login

from weblogin import doLogin

import os

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
            self.yogaGloLoggedIn = check_login(myaccount, "User") #TODO Take this second argument out, don't need it
            if not self.yogaGloLoggedIn:
                print "YogaGlo -- Cookie PHP session seems invalid...logging in again"
                self.yogaGloLoggedIn = self.yogaGloLogin()

        self.pluginParameters = getXbmcInputParameters(params)
        
        print "YogaGlo -- DONE WITH INIT"

    def getNavigationInformation(self, category):
        print "YogaGlo -- getting the navigation information for category: %s" % category
        menuList = []
        yogaglo = openUrl(self.baseUrl)
        soup = BeautifulSoup(''.join(yogaglo))
        navInfo = soup.find('li', id=category).findAll('a')
        print navInfo

        for info in navInfo:
            infoTitle = info.contents[0]
            infoUrl = urllib.quote(info['href'].encode('utf-8'))
            menu = (infoTitle, infoUrl)
            
            if category == "2":  # Looking at teachers, need images
                teacherImageUrl = self.getTeacherImageUrl(infoUrl)
                menu = menu + (teacherImageUrl,)
            
            menuList.append(menu)

        print "YogaGlo -- got all the navigation information for category: %s" % category
        return menuList

    def getYogaGloCategory(self, category):
        if category == "Teacher":
            return 2
        elif category == "Style":
            return 3
        elif category == "Level":
            return 4
        elif category == "Duration":
            return 5

    def getTeacherImageUrl(self, teacherUrl):
        url = self.baseUrl + urllib.quote(teacherUrl.encode('utf-8'))
        teachercontent = openUrl(url)
        soup = BeautifulSoup(teachercontent)
        imgUrl = soup.find('section', attrs={'class': 'cf'}).div.img
        return self.baseUrl + urllib.quote(imgUrl['src'].encode('utf-8'))
        
    def buildYogaCategoryMenu(self):
        print "YogaGlo -- Building category menu just selected"
        itemList = []
        ygCategory = self.pluginParameters['yogaCategory']
        menu = self.getNavigationInformation(ygCategory)
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
            
    def buildClassesMenu(self):
        itemList = []
        ygUrl = self.pluginParameters['yogagloUrl']
        url  = self.baseUrl + ygUrl
        page = openUrl(url)
        soup = BeautifulSoup(page)
        classes = soup.find('div', attrs={'class': re.compile("^main_layout")}).findAll('section')[-1].findAll('div', id=re.compile('^[0-9]+'))
        for yogaClass in classes:
            classUrl = yogaClass.a['href']
            classCoverPic = yogaClass.a.img['src'].encode('utf-8')
            classLength = yogaClass.findAll('div')[3].contents
            id = yogaClass['id']
            desc = self.getClassDescription(id)
            soup = BeautifulSoup(desc)
            style = soup.i.nextSibling
            try:
                title = soup.b.contents[0]
            except:
                title = style  # TODO something else here, like color it to make it different

            level = soup.findAll('i')[1].nextSibling
            teacher = soup.findAll('i')[2].nextSibling
            fullDesc = soup.findAll('br')[-1].nextSibling
            classInfo = (classUrl, classCoverPic, classLength, title, style, level, teacher, fullDesc)
            print classInfo
                
            li = xbmcgui.ListItem(label=title, label2=fullDesc, iconImage=classCoverPic)  # , path=streamurl)
            li.setInfo('video', {'title': title,
                                 'label': "Style: " + style + " Level: " + level,
                                 'plot': fullDesc})
            li.setProperty('IsPlayable', 'true')
            callbackParams = { 'yogaCategory' : self.pluginParameters['yogaCategory'], 'yogagloUrl' : classUrl, 'play': 1}
            callBackUrl = self.xbmcPlugin + "?" + urllib.urlencode(callbackParams)
            itemList.append((callBackUrl, li, False))

        addDirs(self.xbmcHandle, itemList)
        eod(self.xbmcHandle)
            
    def getClassDescription(self, classId):
        ajaxUrl = "/_ajax_get_class_description.php?"
        query = { 'id' : classId, 't': 0 }
        url = self.baseUrl + ajaxUrl + urllib.urlencode(query)
        desc = openUrl(url)
        return desc
        
    def playYogaGloVideo(self):
        print urllib.unquote(self.addonProfilePath)
        logged_in = False
        vidPage = self.pluginParameters['yogagloUrl']
        if not vidPage[0] == "/":
            vidPage = "/" + vidPage
            print self.yogaGloLoggedIn
            if self.yogaGloLoggedIn:
                html = openUrlWithCookie(self.baseUrl + vidPage, self.cookiePath)
                print re.compile(".*url: '([^']*)'").findall(html)
                swfUrl = re.compile(".*url: '([^']*)'").findall(html)[0]
                print re.compile('url: "([^"]*)"').findall(html)
                playpath = urllib.unquote(re.compile('url: "([^"]*)"').findall(html)[0])
                print re.compile("netConnectionUrl:\s+'([^']*)'").findall(html)[0]
                rtmpUrl = re.compile("netConnectionUrl:\s+'([^']*)'").findall(html)[0]
            else:
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
