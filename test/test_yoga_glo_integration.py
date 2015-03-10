'''
Created on Jan 2, 2014

@author: jacobono
'''
from yogaglo.yogaglo import YogaGlo
from mock import Mock, patch
import yogaglo.authentication

# Do a full test from the plugin code.  Runs through everything, stubbing out the xbmc stuff -- so nothing to actually test -- but the code is fully run through, gauranteeing no typos in the yogaglo and xbmc_util modules.  soup_crawler module is tested fully, but the yogaglo and xbm_util need to be run through and no way to test them
class TestYogaGloIntegration(object):

    def setUp(self):
	    self.patcher = patch('yogaglo.authentication.yg_authenticate')
	    self.authenticate = self.patcher.start()
	    self.authenticate.return_value = True

    def tearDown(self):
	    self.patcher.stop()

    def test_index(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {})
        results = yogaglo.index()

    def test_teacher_category(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "2"})
        resuls = yogaglo.category_menu()

    def test_style_category(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "3"})
        resuls = yogaglo.category_menu()

    def test_duration_category(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "4"})
        resuls = yogaglo.category_menu()

    def test_level_category(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "5"})
        resuls = yogaglo.category_menu()

    def test_teacher_select(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "2", 'yogagloUrl' : 'http://classic.yogaglo.com/teacher-37-Kathryn-Budig.html'})
        resuls = yogaglo.classes_menu()

    def test_style_select(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "2", 'yogagloUrl' : 'http://classic.yogaglo.com/video-Style-26-Ashtanga.html'})
        resuls = yogaglo.classes_menu()

    def test_level_select(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "2", 'yogagloUrl' : 'http://classic.yogaglo.com/video-Level-23-Level-2-3.html'})
        resuls = yogaglo.classes_menu()

    def test_duration_select(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "2", 'yogagloUrl' : 'http://classic.yogaglo.com/video-Duration-75-75-min.html'})
        resuls = yogaglo.classes_menu()

    def test_yoga_of_the_day_select(self):
        yogaglo = YogaGlo("plugin://yogaglo.py", 2, {'yogaCategory' : "2", 'yogagloUrl' : 'http://classic.yogaglo.com'})
        resuls = yogaglo.classes_menu()

    # def test_class_play(self):
