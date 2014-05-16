''''
Created on May 14, 2014

@author: jacobono
'''
from mock import Mock, patch, MagicMock
from yogaglo.authentication import yg_authenticate
from nose.tools import assert_equals
from xbmcaddon import Addon
import os

# I don't really have two accounts and I don't want to put my credentials here, so
# i am mocking out the calls to yg_login.
# I use the plugin and the login works, so this shouldn't be a problem
class TestYogaGloAuthentication(object):

        def setUp(self):
	        self.addon = Addon()
	        self.addon.getAddonInfo = MagicMock(return_value="some-special-path")
	        self.patcher = patch('yogaglo.authentication.translatePath')
	        self.check_patcher = patch('yogaglo.authentication.check_login')
	        self.openurl_patcher = patch('yogaglo.authentication.openUrl')
	        self.translate_path = self.patcher.start()
	        self.check_login = self.check_patcher.start()
	        self.openurl = self.openurl_patcher.start()
	        self.openurl.return_value = ""
	
	def tearDown(self):
		self.patcher.stop()
		self.check_patcher.stop()

	@patch('yogaglo.authentication.login')
	def test_no_cookie_no_login_ever(self, mock_login):
		mock_login.return_value = False
		self.translate_path.return_value = os.getcwd()
		result = yg_authenticate(self.addon)
		assert_equals(result, False)
	
	def test_found_cookie_still_valid(self):
		self.check_login.return_value = True
		self.translate_path.return_value = os.path.join(
			os.getcwd(),"test/resources")
		result = yg_authenticate(self.addon)
		assert_equals(result, True)

	@patch('yogaglo.authentication.login')
	def test_found_cookie_not_valid(self, mock_login):
		mock_login.return_value = False
		self.check_login.return_value = False
		self.translate_path.return_value = os.path.join(
			os.getcwd(),"test/resources")
		result = yg_authenticate(self.addon)
		assert_equals(result, False)
		
		
