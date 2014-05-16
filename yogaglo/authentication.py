import os
from xbmc import translatePath

from http import openUrl, login, check_login

yg_cookie = "yogaglo-cookie.lwp"
yg_login_url = "http://www.yogaglo.com/eventcontroler.php"
yg_signin_url = "http://www.yogaglo.com/signin.php"
yg_my_account_url = "http://www.yogaglo.com/myaccounttoday.php"

# return is logged on or not
def yg_authenticate(addon):
	yg_addon_profile_path = translatePath(addon.getAddonInfo('profile'))
	if not os.path.exists(yg_addon_profile_path):
		os.makedirs(yg_addon_profile_path)
		
	yg_cookie_path = os.path.join(yg_addon_profile_path, yg_cookie)
	if not os.path.isfile(yg_cookie_path):
		print "YogaGlo -- No cookie found for %s, attempting to log on to YogaGlo with credentials" % yg_cookie_path
		return yg_login(addon, yg_cookie_path)

	print "YogaGlo -- Found cookie... just trying to see if it is still a valid session"
	yg_my_account = openUrl(yg_my_account_url, yg_cookie_path)
	logged_in = check_login(yg_my_account) #RETURN
	if not logged_in:
		print "YogaGlo -- Cookie PHP session appears to be invalid...logging in again"
		return yg_login(addon, yg_cookie_path)

	return logged_in
		
# attempt to log on, return boolean for success/failure
def yg_login(addon, yg_cookie_path):
	username = addon.getSetting('username')
	password = addon.getSetting('password')
	if username and password:
		print "YogaGlo -- found credentials for username and password, attempting to logon"
		loggedOn = login(yg_cookie_path, username, password, yg_signin_url)
		print "YogaGlo -- logon was %s", "Successful" if loggedOn else "UnSuccessful"
		return loggedOn

        #TODO show error dialog
        print "YogaGlo -- One of either Username or Password is blank, cannot log on"
        return False
