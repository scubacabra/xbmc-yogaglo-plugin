from xbmc import translatePath, log, LOGDEBUG, LOGNOTICE
from xbmcaddon import Addon
from xbmc_util import (addDirs, eod, yoga_class_list_item,
form_plugin_url, yoga_category_menu_list_item,
yoga_glo_index_menu_item, yoga_class_play_video)
import os

from http import openUrl, openUrlWithCookie, login, check_login
from soup_crawler import SoupCrawler

class YogaGlo:
    plugin_name = "plugin.video.yogaglo"
    yoga_glo_base_url = "http://www.yogaglo.com"
    cookie_file = "yogaGloCookie.lwp"
    yoga_glo_sign_in_url = "http://www.yogaglo.com/signin.php"
    yoga_glo_login_url = "http://www.yogaglo.com/eventcontroler.php"

    def __init__(self, plugin, handle, plugin_params):
        log("YogaGlo -- args are %s, %s, %s" %
            (plugin, handle, plugin_params), LOGDEBUG)
        self.xbmc_plugin = plugin
        self.xbmc_handle = handle
        self.addon = Addon(id=self.plugin_name)
        self.yoga_glo_plugin_parameters = plugin_params
        self.crawler = SoupCrawler(self.yoga_glo_base_url)

        # Dir where plugin settings and cache will be stored
        self.yoga_glo_addon_profile_path = translatePath(
            self.addon.getAddonInfo('profile')).decode('utf-8')

        # TODO same, no need for decode
        print translatePath(self.addon.getAddonInfo('profile'))
        print self.yoga_glo_addon_profile_path
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

    # Build plugins index page, with category selection and yoga of the day
    def index(self):
        yoga_glo_categories = {'Teacher': 2, 'Style': 3, 'Duration': 5,
                               'Level': 4, 'Yoga Of The Day': 1 }
        itemList = []
        for category in yoga_glo_categories:
            log("yogaglo -> building index for category '%s'" % (category), LOGDEBUG)
            # processing for yoga of the day!
            if yoga_glo_categories[category] == 1:
                yotd = self.crawler.get_yoga_of_the_day_title_and_info()
                title = yotd['title']
                description = yotd['information']
                plugin_query = {'yogaCategory' : yoga_glo_categories[category],
                                'yogagloUrl' : self.yoga_glo_base_url }
                li = yoga_glo_index_menu_item(title, description)
                plugin_url = form_plugin_url(self.xbmc_plugin, plugin_query)
                itemList.append((plugin_url, li, True))
                continue

            title = category
            description = "Select A" + title
            plugin_query = {'yogaCategory' : yoga_glo_categories[category]}
            li = yoga_glo_index_menu_item(title, description)
            plugin_url = form_plugin_url(self.xbmc_plugin, plugin_query)
            # list item is a folder, per se
            itemList.append((plugin_url, li, True))

        addDirs(self.xbmc_handle, itemList)
        eod(self.xbmc_handle)

    # downselect an upper category to a further filtered category, need to
    # select one level down from here to see videos
    def category_menu(self):
        log("yogaglo -> selecting category %s" %
            (self.yoga_glo_plugin_parameters['yogaCategory']), LOGDEBUG)
        itemList = []
        yoga_category = self.yoga_glo_plugin_parameters['yogaCategory']
        menu = self.crawler.get_yoga_glo_navigation_information(yoga_category)
        for item in menu:
            url = item['url']
            # using get() passes None instead of an error
            li = yoga_category_menu_list_item(item['title'], url,
                                              item.get('image_url'))
            plugin_query = { 'yogaCategory' : yoga_category,
                             'yogagloUrl' : url }
            plugin_url = form_plugin_url(self.xbmc_plugin, plugin_query)
            # list item is a folder, per se
            itemList.append((plugin_url, li, True))

        addDirs(self.xbmc_handle, itemList)
        eod(self.xbmc_handle)

    # list the items for the classes in a certain category, selecting plays the
    # video associated with the item
    def classes_menu(self):
        log("yogaglo -> getting classes for category '%s' at url '%s'" %
            (self.yoga_glo_plugin_parameters['yogaCategory'],
             self.yoga_glo_plugin_parameters['yogagloUrl']), LOGDEBUG)
        #list of items for xbmc to handle (you get a progress bar with this!)
        itemList = []
        yoga_category = self.yoga_glo_plugin_parameters['yogaCategory']
        classesInformation = self.crawler.get_classes(
            self.yoga_glo_plugin_parameters['yogagloUrl'])

        for classInformation in classesInformation:
            class_url = classInformation['url']
            li = yoga_class_list_item(classInformation)
            plugin_query = { 'yogaCategory' : yoga_category,
                             'yogagloUrl' : class_url, 'play': 1}
            plugin_url = form_plugin_url(self.xbmc_plugin, plugin_query)
            # list item is not a folder
            itemList.append((plugin_url, li, False))

        addDirs(self.xbmc_handle, itemList)
        eod(self.xbmc_handle)

    # selected a class item, stream the video for this class
    # preview of 5 minutes (usually), if not logged in to site
    # otherwise, full length, HD video streamed
    def play_class_video(self):
        log("yogaglo -> play class at url '%s'" %
            (self.yoga_glo_plugin_parameters['yogagloUrl']), LOGDEBUG)
        yogaglo_url = self.yoga_glo_plugin_parameters['yogagloUrl']

        #logged in, get full video at highest resolution
        if self.yoga_glo_logged_in:
            video_info = self.crawler.get_yogaglo_video_information(
                yogaglo_url, self.yoga_glo_cookie_path
            )
            yoga_class_play_video(video_info['rtmp_url'],
                                  video_info['play_path'],
                                  video_info['swf_url'], self.xbmc_handle)
            return
            
        #not logged in, 5-minute preview clip
        video_info = self.crawler.get_yogaglo_preview_video_information(
            yogaglo_url)
        yoga_class_play_video(video_info['rtmp_url'],
                              video_info['play_path'],
                              video_info['swf_url'], self.xbmc_handle)
        return

    def processParameters(self):
        if 'play' in self.yoga_glo_plugin_parameters:
            self.play_class_video()
            return

        if 'yogagloUrl' in self.yoga_glo_plugin_parameters:
            self.classes_menu()
            return

        if 'yogaCategory' in self.yoga_glo_plugin_parameters:
            self.category_menu()
            return

        self.index()

    def yogaGloLogin(self):
        username = self.addon.getSetting('username')
        password = self.addon.getSetting('password')
        if username and password:
            print "YogaGlo -- found credentials for username and password, attempting to logon"
            loggedOn = login(self.yoga_glo_cookie_path, username, password,
                             self.yoga_glo_sign_in_url)
            print "YogaGlo -- logon was %s", "Successful" if loggedOn else "UnSuccessful"
            return loggedOn

        #TODO show error dialog
        print "YogaGlo -- One of either Username or Password is blank, cannot log on"
        return False
