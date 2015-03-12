import cookielib
import requests
import os
from xbmcswift2 import xbmc
import pickle


class YogaGloCore:
    """
    YogaGloCore handles cookies, sessions, and authentication tokens
    """

    def __init__(self, plugin):
        self.plugin = plugin
        self.plugin_profile_folder = self._make_addon_profile_folder()
        self.cookiejar = self._load_cookiejar()
        self.cookie_expired = self._cookie_expired()
        self.session = requests.session()
        self.session.cookies = self.cookiejar
        self.x_auth_token = self._load_x_authentication_token()

    def _make_addon_profile_folder(self):
        plugin_profile_folder = xbmc.translatePath(
            self.plugin._addon.getAddonInfo('profile'))

        if not os.path.exists(plugin_profile_folder):
            os.makedirs(plugin_profile_folder)

        return plugin_profile_folder

    def _load_x_authentication_token(self):
        x_auth_file = os.path.join(self.plugin_profile_folder,
                                   "yogaglo-x-auth.txt")
        if not os.path.exists(x_auth_file):
            return ''

        f = open(x_auth_file, 'r')
        return pickle.load(f)

    def _save_x_authenicaiton_token(self, new_x_auth_token):
        self.x_auth_token = new_x_auth_token
        x_auth_file = os.path.join(self.plugin_profile_folder,
                                   "yogaglo-x-auth.txt")
        f = open(x_auth_file, 'w')
        pickle.dump(self.x_auth_token, f)

    def _load_cookiejar(self):
        cookie_path = os.path.join(self.plugin_profile_folder,
                                   "yogaglo-cookie.txt")
        cookiejar = cookielib.LWPCookieJar(cookie_path)

        xbmc.log("yogaglo -> loading cookie at '%s'" %
                 cookie_path, xbmc.LOGDEBUG)

        try:
            cookiejar.load()  # if cookie is expired will not load anything
        except IOError:
            xbmc.log("yogaglo -> cookie doesn't exist at '%s'" %
                     cookie_path, xbmc.LOGDEBUG)
        except cookielib.LoadError:
            xbmc.log("yogaglo -> cookie is unreadable at '%s'!" %
                     cookie_path, xbmc.LOGDEBUG)

        return cookiejar

    def _cookie_expired(self):
        cookie = [c for c in self.cookiejar
                  if c.domain == self.yg_urls['domain']]
        if not cookie:
                return True

        # should only be one cookie loaded for this 1 files
        return cookie.pop().is_expired()
