# Some documentation

Just trying to get yogaglo videos on xbmc.

## Categories for findign videos

Per the yg site, their are 4 categories on their homepage.

* Teachers
* Style
* Duration
* Level

These 4 categories should be in the plugin index.  Each of these categories parses the homepage to find their respective entries and list them in the next view.  THeer are no videos to choose from until you further filter your selection inside the chosen categories contents (i.e. particular teacher, style, level or duration)

## Yoga of the day
A 5th category is some 'yoga of the day'.  The homepage lists 6 different videos every few days.  They always some theme/title and a description.  I call it 'yoga of the day'.  This entry should be displayed in the index menu in the plugin.  But unlike the other 4 categories that allow a further selection, this should take you straight to choosing the videos.

**Note: yoga of the day video have no date associated with them, for whatever reason**

## Total index categories (in order)

* Teachers
* Style
* Duration
* Level
* "Yoga of the Day" title, whatever that may be

# Yoga glo class information

All the classes items from the site carry thin information, return as a dictionary in the code.

* title --> *class name* **^**
* url --> *class url* **^**
* id --> *class id* **^**
* cover_picture_url --> *class url for cover picture menu*
* style --> *class style*
* duration --> *class length in min*
* level --> *class level*
* description --> *class description*
* teacher --> *class teacher*
* date --> *class release date* **NOT used yet**

*Note ^ items can be found from class containing div, all the rest is retrieved through an ajax called keyed by class id*

# XBMC plugin actions

* `index` --> list of menu choices (see above)
* `select_yogaglo_category` --> filters on one of the 4 choices for category filtering.
   No url to specify -- the url to crawl/scrape will be the homepage
* `get_classes_for_category(url)` --> gets the classes videos for this final category filtering
   displays them as list in xbmc

# Crawling/scraping actions

* `get_teacher_image_url(teacher_url)`
   Get this from teacher's own respective url page
* `get_yoga_class_description(class_id)`
   Every class has an ID that is associated with it.  The description of the class is retrieved through an ajax call returning some HTML (though not very well marked up)
* `get_video_details(crawled_class_div)` --> returns a dictionary
   takes the div with all the class information, gets the 4 items **denoted by ^ above** and sends the id to `get_class_description`.  returns a dictionary of the items described above
* `scrape_videos(url)` --> returns array of scraped div class div containers
   all videos can probably be scraped in the same manner, but there is going to be a difference scraping yoga of the day as opposed to the other ways.  Both methods just get the `section` enclosing parent tag that contains the video divs.  Once this is done all class div scraping is performed the same way.
* `get_classes(url)` --> returns array of dictionaries
   A page url needs to be parsed for classes -- could be many, so it returns an array of dicitonaries containing all the necessary information for each class.  Delegates to `scrape_videos` to get all the div containers, loops over them and delegates to `get_video_details` to the information dictionary.  returns an array of dictionaries for xbmc so `get_classes_for_category` can add to the gui.

# XBMC parameters in

* initially --> empty {}
* selecting a category --> 1 populated entry --> {'yoga_glo_category': '1-5'}
* retrieving classes for a category --> {'yoga_glo_category': '1-5', 'yoga_glo_url':'some_url'}
* playing a video
