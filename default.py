import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
 
HANDLE = int(sys.argv[1])

pluginName = "plugin.video.yogaglo"
__addon__       = xbmcaddon.Addon(id=pluginName)
__addonname__   = __addon__.getAddonInfo('name')

__icon__        = __addon__.getAddonInfo('icon')

 

title = "Hello World"

text = "This is some text"

time = 5000  # ms

line1 = "This is my first XBMC plugin"
line2 = "Going to do some YOGA with YogaGlo"
line3 = "showing this message in python modules"
 

dialog = xbmcgui.Dialog()
dialog.ok(__addonname__, line1, line2, line3) 
xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(title, text, time, __icon__))
def addDir(url, listItem, isFolder):
    return xbmcplugin.addDirectoryItem(HANDLE, url, listItem, isFolder)

def addDirs(linkList):
    print "Trying to add dirs %s, %s" % (HANDLE, len(linkList))
    return xbmcplugin.addDirectoryItems(HANDLE, linkList, len(linkList))


