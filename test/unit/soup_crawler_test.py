'''
Created on Jan 2, 2014

@author: jacobono
'''
import unittest, io, urllib
from mock import Mock
from mock import patch

from SoupCrawler import SoupCrawler
    
class SoupCrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = SoupCrawler("http://www.yogaglo.com")

    def tearDown(self):
        self.crawler = None

    @patch('SoupCrawler.openUrl')
    def test_teacher_image_url_no_utf_8(self, mock_open_url):
        mock_open_url.return_value = self.readTestInput("kathryn-page.html")
        result = self.crawler.getTeacherImageUrl("http://www.yogaglo.com/teacher-37-Kathryn-Budig.html")
        assert result == "http://www.yogaglo.com/dbimage/Kathryn_Bio_Pic.jpg"
        
    @patch('SoupCrawler.openUrl')
    def test_teacher_image_url_utf_8_Noah_Maze(self, mock_open_url):
        mock_open_url.return_value = self.readTestInput("noah-page.html")
        result = self.crawler.getTeacherImageUrl("http://www.yogaglo.com/teacher-4-Noah-Maz%C3%A9.html")
        assert result == "http://www.yogaglo.com/dbimage/Noah_bio.jpg"
        
    @patch('SoupCrawler.openUrl')
    def test_get_teacher_name_and_url_no_utf_8(self, mock_open_url):
        mock_open_url.return_value = self.readTestInput("yghomepage-kathryn-only-teacher.html")
        self.crawler.getTeacherImageUrl = Mock(return_value="something")
        title, ygUrl = self.crawler.getNavigationInformation("2")[0][:2]
        assert title == "Kathryn Budig"
        assert ygUrl == "/teacher-37-Kathryn-Budig.html"
     
    @patch('SoupCrawler.openUrl')   
    def test_get_teacher_name_and_url_utf_8_Noah_Maze(self, mock_open_url):
        mock_open_url.return_value = self.readTestInput("yghomepage-noah-only-teacher.html")
        self.crawler.getTeacherImageUrl = Mock(return_value="something")
        title, ygUrl = self.crawler.getNavigationInformation("2")[0][:2]
        self.assertEqual(title, u"Noah Maz\xe9")
        self.assertEqual(ygUrl, "/teacher-4-Noah-Maz%C3%A9.html")
    
    @patch('SoupCrawler.openUrl') 
    def test_class_description_no_utf_8(self, mock_open_url): 
        mock_open_url.return_value = self.readTestInput("kathryn-class-3085.html")
        result = self.crawler.getClassDescription("3085")
        self.assertEqual(result['title'], "Deep Hip Love")
        self.assertEqual(result['secondLabel'], "Style: Vinyasa Flow Level: 2-3")
        self.assertEqual(result['plot'], ("Time for some deep hip love! This full flow class blends deep hip "
                                            "burning with hip stretching to create the perfect balance and freedom in the pelvis. "))
        self.assertEqual(result['style'], "Vinyasa Flow")
        self.assertEqual(result['level'], "2-3")
        self.assertEqual(result['teacher'], "Kathryn Budig")
        
    @patch('SoupCrawler.openUrl') 
    def test_class_description_utf_8_Noah_Maze(self, mock_open_url):   
        mock_open_url.return_value = self.readTestInput("noah-class-3088.html")
        result = self.crawler.getClassDescription("3088")
        self.assertEqual(result['title'], "Fun Fierce Flow")
        self.assertEqual(result['secondLabel'], "Style: Vinyasa Flow Level: 2-3")
        self.assertEqual(result['plot'], ("This vinyasa class begins with seated pranayama to establish the breath, sun salutation "
                                          "progressions to build heat and focus, into strong standing pose flows to work the legs and stretch the spine, hand balancings "
                                          "and core work for fierce fun, and backbends as the night cap. Enjoy!\n\nProps: 1 block "))
        self.assertEqual(result['style'], "Vinyasa Flow")
        self.assertEqual(result['level'], "2-3")
        self.assertEqual(result['teacher'], u"Noah Maz\xc3\xa9")

    @patch('SoupCrawler.openUrl') 
    def test_class_description_no_class_title(self, mock_open_url): 
        mock_open_url.return_value = self.readTestInput("no-class-title-class.html")
        result = self.crawler.getClassDescription("3085")
        self.assertEqual(result['title'], "Vinyasa Flow")
        self.assertEqual(result['secondLabel'], "Style: Vinyasa Flow Level: 2-3")
        self.assertEqual(result['style'], "Vinyasa Flow")
        self.assertEqual(result['level'], "2-3")
        self.assertEqual(result['teacher'], "Kathryn Budig")
  
    @patch('SoupCrawler.openUrl')          
    def test_noah_maze_utf_8_video_url(self, mock_open_url):
        mock_open_url.return_value = self.readTestInput("noah-maze-utf-video-class.html")
        self.crawler.getClassDescription = Mock(return_value={})
        result = self.crawler.getClassesInformation("doesntmatter")[0]
        self.assertEqual(result['coverPicUrl'], "http://d3sywv2955jo7z.cloudfront.net/8_12_09_NM_thumb.jpg")
        self.assertEqual(result['url'], "online-class-194-by-Noah-Maz\xc3\xa9-on-Anusara.html")
        
    def readTestInput(self, filename):
        try:
            testinput = open("resources/" + filename)
            inputdata = testinput.read()
        except:
            testinput = io.open("resources/" + filename)
            inputdata = testinput.read()

        return inputdata 
               
if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
