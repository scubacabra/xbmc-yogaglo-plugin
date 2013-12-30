from BeautifulSoup import BeautifulSoup

from http import openUrl
import urllib
import re

class SoupCrawler(object):

    # Yoga Glo Base Url
    def __init__(self, yoga_glo_url):
        self.yogaGloUrl = yoga_glo_url
        self.classDescriptionAjaxUrl = self.yogaGloUrl + "/_ajax_get_class_description.php?"
    
    # Get basic navigation information, cueing off of Category -- String number [1-4]
    # inputs
    # category [1-4]
    # Teacher, Style, Level, Duration
    # Returns list of tuples (title, url, *imageUrl) 
    # *optional
    def getNavigationInformation(self, category):
        print "YogaGlo -- getting the navigation information for category: %s" % category
        menuList = [] # list of tuples to return
        yogaglo = openUrl(self.yogaGloUrl)
        soup = BeautifulSoup(''.join(yogaglo))
        navInfo = soup.find('li', id=category).findAll('a')
        print navInfo

        for info in navInfo:
            infoTitle = info.contents[0]
            infoUrl = urllib.quote(info['href'].encode('utf-8'))
            menu = (infoTitle, infoUrl)
            
            if category == "2":  # Looking at teachers, need images
                teacherImageUrl = self.getTeacherImageUrl(infoUrl)
                menu = menu + (teacherImageUrl,)
                
            menuList.append(menu)

        print "YogaGlo -- got all the navigation information for category: %s" % category
        return menuList


    # Get teacher Image Url -- only available on teachers page
    # need to encode url properly in case their are utf-8 characters -- there are some. Noah Maze!
    # returns full URL to teacher image
    def getTeacherImageUrl(self, teacherUrl):
        url = self.yogaGloUrl + urllib.quote(teacherUrl.encode('utf-8'))
        teachercontent = openUrl(url)
        soup = BeautifulSoup(teachercontent)
        imgUrl = soup.find('section', attrs={'class': 'cf'}).div.img
        return self.yogaGloUrl + urllib.quote(imgUrl['src'].encode('utf-8'))


    # Get Classes information -- for whatever category it's all the same
    # Input
    # Relative Page Url (parameter passed in)
    # Return
    # list of maps, containing params for xbmc information
    # classTitle, classSecondLabel, classCoverPictureUrl, classPlot, classLength (int), classStyle, classLevel, classTeacher, classUrl
    # all keys are without the "class" prefix and are string unless otherwise noted
    # title, secondLabel, coverPicUrl, plot, duration, style, level, teacher, url
    def getClassesInformation(self, relativePageUrl):
        classesInformation = [] # return this list
        pageContent = openUrl(self.yogaGloUrl + relativePageUrl)
        soup = BeautifulSoup(pageContent)
        classes = soup.find('div', attrs={'class': re.compile("^main_layout")}).findAll('section')[-1].findAll('div', id=re.compile('^[0-9]+'))
        for yogaClass in classes:
            classUrl = yogaClass.a['href']
            classCoverPicUrl = yogaClass.a.img['src'].encode('utf-8')
            classLength = yogaClass.findAll('div')[3].contents[0]
            classInformation = self.getClassDescription(yogaClass['id'])
            classInformation['url'] = classUrl
            classInformation['coverPicUrl'] = classCoverPicUrl
            classInformation['duration'] = int(classLength.split(" ")[0])
            classesInformation.append(classInformation)

        return classesInformation
            

    # Get the class description key information from the ajax request
    # not really formed well, but this is how they get it in their main pages -- I must comply
    # input -- the class ID from yogaGlo designation
    # return a dictionary of important fields
    # title, secondLabel, plot, style, level, teacher
    def getClassDescription(self, classId):
        query = { 'id' : classId, 't': 0 }
        classDescription = openUrl(self.classDescriptionAjaxUrl + urllib.urlencode(query))
        soup = BeautifulSoup(classDescription)

        style = soup.i.nextSibling
        # sometimes they are missing a title, in which case default to the style so you know when looking at that item
        try:
            title = soup.b.contents[0]
        except:
            title = style  # TODO something else here, like color it to make it different

        level = soup.findAll('i')[1].nextSibling
        teacher = soup.findAll('i')[2].nextSibling
        fullDesc = soup.findAll('br')[-1].nextSibling
        classInformation = { 'title' : title,
                             'secondLabel' : "Style: " + style + " Level: " + level,
                             'plot' : fullDesc,
                             'style' : style,
                             'level' : level,
                             'teacher' : teacher }
        print classInformation
        return classInformation
