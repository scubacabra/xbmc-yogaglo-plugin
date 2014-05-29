## Categories for finding videos

Per the yg site, their are 4 categories on their homepage navigation banner.

* Teachers
* Style
* Duration
* Level

These 4 categories should be in the plugin index.  Each of these categories parses the homepage to find their respective entries and list them in the next view.  THeer are no videos to choose from until you further filter your selection inside the chosen categories contents (i.e. particular teacher, style, level or duration)

## Yoga of the day
A 5th category is some 'yoga of the day'.  The homepage lists 6 different videos every few days.  They always some theme/title and a description.  I call it 'yoga of the day'.  This entry should be displayed in the index menu in the plugin.  But unlike the other 4 categories that allow a further selection, this should take you straight to choosing the videos.

**Note: yoga of the day videos have no date associated with them, for whatever reason**

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
