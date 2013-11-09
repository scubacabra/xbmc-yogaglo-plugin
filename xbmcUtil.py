import xbmcplugin
import urllib

def addDir(handle, url, listItem, isFolder):
    return xbmcplugin.addDirectoryItem(handle, url, listItem, isFolder)

def addDirs(handle, linkList):
    print "Trying to add dirs %s, %s" % (handle, len(linkList))
    return xbmcplugin.addDirectoryItems(handle, linkList, len(linkList))

def eod(handle):
    return xbmcplugin.endOfDirectory(handle)

def listItemResolvedUrl(handle, listItem):
    return xbmcplugin.setResolvedUrl(handle,True, listItem) 

def getXbmcInputParameters(url):
    parameters = {}
    try:
        qm, params = url.split('?')
    except:
        params = None
        
    if not params is None:
        splitParameters = params.split('&')
        for pair in splitParameters:
            if len(pair) > 0:
                twoValues = pair.split('=')
                param = twoValues[0]
                value = urllib.unquote(urllib.unquote_plus(twoValues[1])).decode('utf-8')
                parameters[param] = value
    print "YogaGlo -- Parameters are %s" % parameters
    return parameters
