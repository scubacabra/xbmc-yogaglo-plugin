import cookielib
import requests
import os
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
            self.plugin.log.debug("yogaglo -> creating directory '%s'" %
                                  plugin_profile_folder)
            os.makedirs(plugin_profile_folder)

        return plugin_profile_folder

    def _load_x_authentication_token(self):
        x_auth_file = os.path.join(self.plugin_profile_folder,
                                   "yogaglo-x-auth.txt")
        if not os.path.exists(x_auth_file):
            self.plugin.log.debug("yogaglo -> x-auth file '%s' doesn't exist" %
                                  x_auth_file)
            return ''

        f = open(x_auth_file, 'r')
        return pickle.load(f)

    def _save_x_authenicaiton_token(self, new_x_auth_token):
        self.x_auth_token = new_x_auth_token
        x_auth_file = os.path.join(self.plugin_profile_folder,
                                   "yogaglo-x-auth.txt")
        self.plugin.log.debug("yogaglo -> saving new x-auth '%s'token to file '%s'" % (new_x_auth_token, x_auth_file))
        f = open(x_auth_file, 'w')
        pickle.dump(self.x_auth_token, f)

    def _load_cookiejar(self):
        cookie_path = os.path.join(self.plugin_profile_folder,
                                   "yogaglo-cookie.txt")
        cookiejar = cookielib.LWPCookieJar(cookie_path)

        self.plugin.log.debug("yogaglo -> loading cookie at '%s'" %
                              cookie_path)

        try:
            cookiejar.load()  # if cookie is expired will not load anything
        except IOError:
            self.plugin.log.debug("yogaglo -> cookie doesn't exist at '%s'" %
                                  cookie_path)
        except cookielib.LoadError:
            self.plugin.log.debug("yogaglo -> cookie is unreadable at '%s'!" %
                                  cookie_path)

        return cookiejar

    def _cookie_expired(self):
        cookie = [c for c in self.cookiejar
                  if c.domain == self.yg_urls['domain']]
        if not cookie:
                return True

        # should only be one cookie loaded for this 1 files
        return cookie.pop().is_expired()
