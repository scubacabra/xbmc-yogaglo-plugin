'''
Created on Jan 2, 2014

@author: jacobono
'''
import unittest
from SoupCrawler import SoupCrawler


class YogaGloTest(unittest.TestCase):


    def setUp(self):
        self.crawler = SoupCrawler("http://www.yogaglo.com")

    def tearDown(self):
        pass

    def test_noah_maze_parse_teacher_page(self):
        results = self.crawler.getClassesInformation(u'/teacher-4-Noah-Maz\xe9.html')
        assert results is not None

    def test_kathryn_parse_teacher_page(self):
        results = self.crawler.getClassesInformation(u'/teacher-37-Kathryn-Budig.html')
        assert results is not None
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()