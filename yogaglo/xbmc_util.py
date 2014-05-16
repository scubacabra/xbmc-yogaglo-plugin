import xbmc
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, addDirectoryItems, endOfDirectory, setResolvedUrl, setContent
from urlparse import urlparse, parse_qsl, urlsplit
from urllib import urlencode
from string import join

def setViewMode(handle, addon, id):
    if xbmc.getSkinDir() == 'skin.confluence':
        setContent(handle, 'episodes')
        xbmc.executebuiltin('Container.SetViewMode(' + id + ')')

# Takes a class information dictionary and populates a list item from it
# returns list item
def yoga_class_list_item(class_info):
    li = ListItem(label=class_info['title'],
                          label2=class_info['secondLabel'],
                          iconImage=class_info['coverPicUrl'])
    li.setInfo('video', {'title': class_info['title'],
                         'plot': class_info['plot'],
                         'Duration': class_info['duration'],
                         'plotoutline': class_info['secondLabel'],
                         'tagline': class_info['teacher'],
                         'genre': "Yoga"
                     })
    li.setProperty('IsPlayable', 'true')
    return li

def yoga_category_menu_list_item(item_title, item_url, item_image_url):
    if item_image_url is not None:
        li = ListItem(label=item_title, iconImage=item_image_url)
        return li
    
    li = ListItem(label=item_title, iconImage="Default.png")
    return li
    
def yoga_glo_index_menu_item(title, description):
    li = ListItem(label=title, label2=description,
                          iconImage="Default.png")
    return li

def yoga_class_play_video(rtmp_url, play_path, swf_url, xbmc_handle):
    li = ListItem(path=rtmp_url)
    li.setProperty('PlayPath', play_path);
    li.setProperty('SWFPlayer', swf_url);
    setResolvedUrl(xbmc_handle, True, li)

def form_plugin_url(xbmc_plugin, query):
    query_string = urlencode(query)
    return join((xbmc_plugin, query_string), "?")

def addDirs(handle, linkList):
    return addDirectoryItems(handle, linkList, len(linkList))

def eod(handle):
    return endOfDirectory(handle)

def get_yoga_glo_input_parameters(xbmc_plugin_parameters):
    url_parts = urlsplit(xbmc_plugin_parameters)
    query_parameters = parse_qsl(url_parts.query)
    # [] tuple returns empty map
    yoga_glo_parameters = dict(query_parameters)
    return yoga_glo_parameters

