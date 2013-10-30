import xbmcaddon
import xbmcgui
 
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
 
line1 = "This is a simple example of OK dialog"
line2 = "Showing this message using"
line3 = "XBMC python modules"
 
xbmcgui.Dialog().ok(__addonname__, line1, line2, line3)
