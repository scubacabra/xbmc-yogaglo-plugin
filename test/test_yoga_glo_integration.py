'''
Created on Jan 2, 2014

@author: jacobono
'''
from nose.tools import assert_equals
from yogaglo.soup_crawler import SoupCrawler

# Do a full test, from the website, no resources, mocks, and patches
class TestYogaGloIntegration(object):

    def setUp(self):
        self.crawler = SoupCrawler("http://www.yogaglo.com")

    def tearDown(self):
        self.crawler = None

    def test_class_description(self):
        results = self.crawler.get_yoga_class_description('2956')
        assert results is not None

    def test_noah_maze_parse_teacher_page(self):
        results = self.crawler.get_classes(
            'http://www.yogaglo.com/teacher-4-Noah-Maz%C3%A9.html')
        assert results is not None

    def test_kathryn_parse_teacher_page(self):
        results = self.crawler.get_classes(
            'http://www.yogaglo.com/teacher-37-Kathryn-Budig.html')
        assert results is not None
