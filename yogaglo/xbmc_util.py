import xbmcplugin
from urlparse import urlparse, parse_qsl, urlsplit

def addDir(handle, url, listItem, isFolder):
    return xbmcplugin.addDirectoryItem(handle, url, listItem, isFolder)

def addDirs(handle, linkList):
    print "Trying to add dirs %s, %s" % (handle, len(linkList))
    return xbmcplugin.addDirectoryItems(handle, linkList, len(linkList))

def eod(handle):
    return xbmcplugin.endOfDirectory(handle)

def listItemResolvedUrl(handle, listItem):
    return xbmcplugin.setResolvedUrl(handle,True, listItem) 

def get_yoga_glo_input_parameters(xbmc_plugin_parameters):
    url_parts = urlsplit(xbmc_plugin_parameters)
    query_parameters = parse_qsl(url_parts.query)
    # [] tuple returns empty map
    yoga_glo_parameters = dict(query_parameters)
    return yoga_glo_parameters

