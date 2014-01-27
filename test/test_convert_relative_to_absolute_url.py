'''
Created on Jan 27, 2014

@author: jacobono
'''

from nose.tools import assert_equals
from yogaglo.http import convert_relative_to_absolute_url

class TestConvertToAbsoluteUrl(object):

    def setUp(self):
        self.base_url = "http://www.yogaglo.com"

    def test_relative_path_with_slash(self):
        rel_uri = "/kathryn-budig.html"
        result = convert_relative_to_absolute_url(self.base_url, rel_uri)
        assert_equals(result, "http://www.yogaglo.com/kathryn-budig.html")

    def test_relative_path_no_slash(self):
        rel_uri = "kathryn-budig.html"
        result = convert_relative_to_absolute_url(self.base_url, rel_uri)
        assert_equals(result, "http://www.yogaglo.com/kathryn-budig.html")

    def test_relative_path_utf8_slash(self):
        rel_uri = u"/teacher-4-Noah-Maz\xe9.html"
        result = convert_relative_to_absolute_url(self.base_url, rel_uri)
        assert_equals(result, "http://www.yogaglo.com/teacher-4-Noah-Maz%C3%A9.html")

    def test_relative_path_utf8_no_slash(self):
        rel_uri = u"/teacher-4-Noah-Maz\xe9.html"
        result = convert_relative_to_absolute_url(self.base_url, rel_uri)
        assert_equals(result, "http://www.yogaglo.com/teacher-4-Noah-Maz%C3%A9.html")
