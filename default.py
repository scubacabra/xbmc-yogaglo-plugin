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

 
    
def buildTopLevelMenu():
    itemList = []
    for category in ["Teacher", "Style", "Level", "Duration"]:
        label = "Select A " + category
        callbackParams = { 'yogaCategory' : getYogaGloCategory(category) }
        url = PLUGIN + "?" + urllib.urlencode(callbackParams)
        li = xbmcgui.ListItem(label=category, label2=label, iconImage="Default.png")
        itemList.append((url, li, True))
    addDirs(itemList)
    xbmcplugin.endOfDirectory(HANDLE)

def buildYogaCategoryMenu(params):
    itemList = []
    menu = getNavigationInformation(params['yogaCategory'])
    print menu
    for item in menu:
        try:
            title, ygUrl, imageUrl = item
        except ValueError:
            title, ygUrl = item
            imageUrl = None
        callbackParams = { 'yogaCategory' : params['yogaCategory'], 'yogagloUrl' : ygUrl }
        url = PLUGIN + "?" + urllib.urlencode(callbackParams)
        if imageUrl is not None:
            li = xbmcgui.ListItem(label=title, iconImage=imageUrl)
        else:
            li = xbmcgui.ListItem(label=title, iconImage="Default.png")
        itemList.append((url, li, True))
    addDirs(itemList)
    xbmcplugin.endOfDirectory(HANDLE)

def getNavigationInformation(category):
    menuList = []
    yogaglo = openUrl(BASEURL)
    soup = BeautifulSoup(''.join(yogaglo))
    navInfo = soup.find('li', id=category).findAll('a')
    for info in navInfo:
        infoTitle = info.contents[0]
        infoUrl = urllib.quote(info['href'].encode('utf-8'))
        menu = (infoTitle, infoUrl)
        if category == "2": #Looking at teachers, need images
           teacherImageUrl = getTeacherImageUrl(infoUrl)
           menu = menu + (teacherImageUrl, )
        menuList.append(menu)
    return menuList

def getTeacherImageUrl(teacherUrl):
    url = BASEURL + urllib.quote(teacherUrl.encode('utf-8'))
    teachercontent = openUrl(url)
    soup = BeautifulSoup(teachercontent)
    imgUrl = soup.find('section', attrs = {'class': 'cf'}).div.img
    return BASEURL + urllib.quote(imgUrl['src'].encode('utf-8'))

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


if not 'yogaCategory' in parameters:
    print "Building the Top Menu"
    buildTopLevelMenu()
else:
    if not 'yogagloUrl' in parameters:
        buildYogaCategoryMenu(parameters)
