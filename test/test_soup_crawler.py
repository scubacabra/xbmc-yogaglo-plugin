''''
Created on Jan 2, 2014

@author: jacobono
'''
from mock import Mock, patch
from yogaglo.soup_crawler import SoupCrawler
from test import readTestInput
from nose.tools import assert_equals

class TestSoupCrawler(object):

    def setUp(self):
        self.crawler = SoupCrawler("http://www.yogaglo.com")
        self.patcher = patch('yogaglo.soup_crawler.openUrl')
        self.mock_open_url = self.patcher.start()

    def tearDown(self):
        self.crawler = None
        self.patcher.stop()

    def test_teacher_image_url_no_utf_8(self):
        self.mock_open_url.return_value = readTestInput("kathryn-page.html")
        result = self.crawler.get_teacher_image_url(
            "http://www.yogaglo.com/teacher-37-Kathryn-Budig.html")
        assert_equals(result,
                      "http://www.yogaglo.com/dbimage/Kathryn_Bio_Pic.jpg")

    def test_teacher_image_url_utf_8_Noah_Maze(self):
        self.mock_open_url.return_value = readTestInput("noah-page.html")
        result = self.crawler.get_teacher_image_url(
            "http://www.yogaglo.com/teacher-4-Noah-Maz%C3%A9.html")
        assert_equals(result,
                      "http://www.yogaglo.com/dbimage/Noah_bio.jpg")

    def test_get_teacher_name_and_url_no_utf_8(self):
        self.mock_open_url.return_value = readTestInput(
            "yghomepage-kathryn-only-teacher.html")
        self.crawler.get_teacher_image_url = Mock(return_value="something")
        title, ygUrl = self.crawler.get_yoga_glo_navigation_information(
            "2")[0][:2]
        assert_equals(title, "Kathryn Budig")
        assert_equals(ygUrl,
                      "http://www.yogaglo.com/teacher-37-Kathryn-Budig.html")

    def test_get_teacher_name_and_url_utf_8_Noah_Maze(self):
        self.mock_open_url.return_value = readTestInput(
            "yghomepage-noah-only-teacher.html")
        self.crawler.get_teacher_image_url = Mock(return_value="something")
        title, ygUrl = self.crawler.get_yoga_glo_navigation_information(
            "2")[0][:2]
        assert_equals(title, u"Noah Maz\xe9")
        assert_equals(ygUrl,
                      "http://www.yogaglo.com/teacher-4-Noah-Maz%C3%A9.html")

    def test_class_description_no_utf_8(self): 
        self.mock_open_url.return_value = readTestInput(
            "kathryn-class-3085.html")
        plot = ("Time for some deep hip love! This full flow class blends deep "
                "hip burning with hip stretching to create the perfect balance "
                "and freedom in the pelvis. ")
        result = self.crawler.get_yoga_class_description("3085")
        assert_equals(result['title'], "Deep Hip Love")
        assert_equals(result['secondLabel'], "Style: Vinyasa Flow Level: 2-3")
        assert_equals(type(result['plot']), type(u"d")) # return unicode
        assert_equals(result['plot'], plot)
        assert_equals(result['style'], "Vinyasa Flow")
        assert_equals(result['level'], "2-3")
        assert_equals(result['teacher'], "Kathryn Budig")

    def test_class_description_utf_8_Noah_Maze(self):   
        self.mock_open_url.return_value = readTestInput("noah-class-3088.html")
        plot = ("This vinyasa class begins with seated pranayama to "
                "establish the breath, sun salutation progressions to "
                "build heat and focus, into strong standing pose flows "
                "to work the legs and stretch the spine, hand "
                "balancings and core work for fierce fun, and backbends "
                "as the night cap. Enjoy!\n\nProps: 1 block ")
        result = self.crawler.get_yoga_class_description("3088")
        assert_equals(result['title'], "Fun Fierce Flow")
        assert_equals(result['secondLabel'], "Style: Vinyasa Flow Level: 2-3")
        assert_equals(type(result['plot']), type(u"d"))
        assert_equals(result['plot'], plot)
        assert_equals(result['style'], "Vinyasa Flow")
        assert_equals(result['level'], "2-3")
        assert_equals(result['teacher'], u"Noah Maz\xc3\xa9")

    def test_class_description_no_class_title(self): 
        self.mock_open_url.return_value = readTestInput(
            "no-class-title-class.html")
        result = self.crawler.get_yoga_class_description("3085")
        assert_equals(result['title'], "Vinyasa Flow")
        assert_equals(result['secondLabel'], "Style: Vinyasa Flow Level: 2-3")
        assert_equals(result['style'], "Vinyasa Flow")
        assert_equals(result['level'], "2-3")
        assert_equals(result['teacher'], "Kathryn Budig")

    def test_noah_maze_utf_8_video_url(self):
        self.mock_open_url.return_value = readTestInput(
            "noah-maze-utf-video-class.html")
        self.crawler.get_yoga_class_description = Mock(return_value={})
        result = self.crawler.get_classes("doesntmatter")[0]
        picUrl = "http://d3sywv2955jo7z.cloudfront.net/8_12_09_NM_thumb.jpg"
        classUrl = ("http://www.yogaglo.com/online-class-194-by-Noah-Maz%C3%A9"
                    "-on-Anusara.html")
        assert_equals(result['coverPicUrl'], picUrl)
        assert_equals(result['url'], classUrl)

    def test_yogaoftheday_holiday_detox(self):
        self.crawler.yoga_glo_category = "1"
        self.mock_open_url.return_value = readTestInput(
            "yg-yogaoftheday-holiday-recovery.html")
        #Mock return doesn't matter here
        self.crawler.get_yoga_class_description = Mock(return_value={})
        result = self.crawler.get_classes("http://www.yogaglo.com/")
        assert_equals(len(result), 6)

    def test_yogaoftheday(self):
        self.crawler.yoga_glo_category = "1"
        # has a different yoga of the day, just reusing
        self.mock_open_url.return_value = readTestInput(
            "yghomepage-noah-only-teacher.html")
        #Mock doesn't matter here
        self.crawler.get_yoga_class_description = Mock(return_value={})
        result = self.crawler.get_classes("http://www.yogaglo.com")
        assert_equals(len(result), 6)

    def test_yoga_of_the_day_title_info(self):
        self.crawler.yoga_glo_category = "6"
        self.mock_open_url.return_value = readTestInput(
            "yghomepage-noah-only-teacher.html")
        info = ("This week\xe2\x80\x99s featured classes will help you "
                "transition into the New Year with grace and ease.")
        result = self.crawler.get_yoga_of_the_day_title_and_info()
        assert_equals(result['information'], info)
        assert_equals(result['title'], 'Yoga for the New Year')

    def test_yoga_of_the_day_title_info_holiday_detox(self):
        self.mock_open_url.return_value = readTestInput(
            "yg-yogaoftheday-holiday-recovery.html")
        info = ("This week\xe2\x80\x99s featured classes will help to release "
                "the toxins and stress that build up in your body during the "
                "holiday season.")
        result = self.crawler.get_yoga_of_the_day_title_and_info()
        assert_equals(result['information'], info)
        assert_equals(result['title'], 'Yoga for Holiday Recovery & Detox')
