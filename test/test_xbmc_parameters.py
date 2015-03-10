'''
Created on Jan 27, 2014

@author: jacobono
'''

from nose.tools import assert_equals
from yogaglo.xbmc_util import get_yoga_glo_input_parameters
from urllib import urlencode

class TestXBMCParameters(object):

    def setUp(self):
        # default empty parameters
        self.plugin_url = "?"

    def test_parameters_empty(self):
        result = get_yoga_glo_input_parameters(self.plugin_url)
        assert_equals(result, {})

    def test_parameters_yoga_category(self):
        query = {'yoga_category': 2}
        url = self.plugin_url + urlencode(query)
        result = get_yoga_glo_input_parameters(url)
        assert_equals(result, {'yoga_category': '2'})

    def test_parameters_yoga_category_and_url(self):
        query = {'yoga_category': 2, 'yoga_glo_url': 'http://classic.yogaglo.com'}
        url = self.plugin_url + urlencode(query)
        result = get_yoga_glo_input_parameters(url)
        assert_equals(result, {'yoga_category': '2',
                               'yoga_glo_url': 'http://classic.yogaglo.com'})

    def test_parameters_yoga_category_url_play(self):
        query = {'yoga_category': 2, 'yoga_glo_url': 'http://classic.yogaglo.com',
                 'play': 1}
        url = self.plugin_url + urlencode(query)
        result = get_yoga_glo_input_parameters(url)
        assert_equals(result, {'yoga_category': '2', 'yoga_glo_url':
                               'http://classic.yogaglo.com','play': '1'})

    def test_parameters_yoga_category_url_utf8(self):
        yg_url = 'http://classic.yogaglo.com/online-class-194-by-Noah-Maz%C3%A9-on-Anusara.html'
        query = {'yoga_category': 2, 'yoga_glo_url': yg_url, 'play': 1}
        url = self.plugin_url + urlencode(query)
        result = get_yoga_glo_input_parameters(url)
        assert_equals(result, {'yoga_category': '2', 'yoga_glo_url': yg_url,
                               'play': '1'})
