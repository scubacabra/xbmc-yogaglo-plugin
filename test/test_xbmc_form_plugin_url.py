'''
Created on Jan 27, 2014

@author: jacobono
'''

from nose.tools import assert_equals
from yogaglo.xbmc_util import form_plugin_url

class TestXBMCPluginURLFormation(object):

    def setUp(self):
        # default empty parameters
        self.xbmc_plugin_url = "plugin://yogaglo/default.py"

    def test_parameters_yoga_category(self):
        query = {'yoga_category': 2}
        result = form_plugin_url(self.xbmc_plugin_url, query)
        assert_equals(result, 'plugin://yogaglo/default.py?yoga_category=2')

    def test_parameters_yoga_category_and_url(self):
        query = {'yoga_category': 2, 'yoga_glo_url': 'http://www.yogaglo.com'}
        result = form_plugin_url(self.xbmc_plugin_url, query)
        assert_equals(result, 'plugin://yogaglo/default.py?yoga_glo_url=http%3A%2F%2Fwww.yogaglo.com&yoga_category=2')

    def test_parameters_yoga_category_url_play(self):
        query = {'yoga_category': 2, 'yoga_glo_url': 'http://www.yogaglo.com',
                 'play': 1}
        result = form_plugin_url(self.xbmc_plugin_url, query)
        assert_equals(result, 'plugin://yogaglo/default.py?play=1&yoga_glo_url=http%3A%2F%2Fwww.yogaglo.com&yoga_category=2')

    def test_parameters_yoga_category_url_utf8(self):
        yg_url = 'http://www.yogaglo.com/online-class-194-by-Noah-Maz%C3%A9-on-Anusara.html'
        query = {'yoga_category': 2, 'yoga_glo_url': yg_url, 'play': 1}
        result = form_plugin_url(self.xbmc_plugin_url, query)
        assert_equals(result, 'plugin://yogaglo/default.py?play=1&yoga_glo_url=http%3A%2F%2Fwww.yogaglo.com%2Fonline-class-194-by-Noah-Maz%25C3%25A9-on-Anusara.html&yoga_category=2')
