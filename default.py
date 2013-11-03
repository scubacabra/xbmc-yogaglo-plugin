import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import gzip
import StringIO
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
def openUrl(url):
    #create an opener
    opener = urllib2.build_opener()
    #Add useragent, sites don't like to interact with scripts
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:24.0) Gecko/20100101 Firefox/24.0'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'en-gb,en;q=0.5'),
        ('Accept-Encoding', 'gzip,deflate'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
        ('Cache-Control', 'max-age=0'),
        ]
 
    resp = opener.open(url)
 
    # Compressed (gzip) response...
    if resp.headers.get( "content-encoding" ) == "gzip":
            htmlGzippedData = resp.read()
            stringIO        = StringIO.StringIO( htmlGzippedData )
            gzipper         = gzip.GzipFile( fileobj = stringIO )
            htmlData        = gzipper.read()
    else :
            htmlData = resp.read()
 
    resp.close()
     
    # Return html
    return htmlData

dialog = xbmcgui.Dialog()
dialog.ok(__addonname__, line1, line2, line3) 
xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(title, text, time, __icon__))
def addDir(url, listItem, isFolder):
    return xbmcplugin.addDirectoryItem(HANDLE, url, listItem, isFolder)

def addDirs(linkList):
    print "Trying to add dirs %s, %s" % (HANDLE, len(linkList))
    return xbmcplugin.addDirectoryItems(HANDLE, linkList, len(linkList))


