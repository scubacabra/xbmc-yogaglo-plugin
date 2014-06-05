plugin.video.yogaglo
====================

[![Build Status](https://drone.io/github.com/jacobono/xbmc-yogaglo-plugin/status.png)]
(https://drone.io/github.com/jacobono/xbmc-yogaglo-plugin/latest)

[YogaGlo](http://www.yogaglo.com) plugin for XBMC -- just trying to
get yogaglo videos on xbmc.

Video Categories
================

Videos can be selected from 4 general categories.

* Teachers
* Style
* Duration
* Level

## Yoga Of The Day ##

A 5th Category is what I call 'yoga of the day', but it is really more
like week. [YogaGlo](http://www.yogaglo.com) has these selected videos
on their homepage, and they rotate them every few days I guess.

Logging In
==========

If you are logged in (set credentials in the configure dialog of
plugin) then the videos played are full length, HD.

If you aren't logged in, you get the 5-minute preview video.  Doesn't
do much good but let you know that you aren't logged in.

Logs in and grabs the cookie, that leaves you validated for a decent
bit of time.  Re-authenticates as needed.

Improvements
============

Fully functional right now, but lacking some features.

* No Video pagination
  - the site does some javascript once you past a certain scroll
    point, haven't delved into it yet.
* Even though logged on, can't get any videos you have saved for later
  to the site.  Only scrapes what is in their categories by crawling
  through the navigation bar and certain sub categories of those.

Hopefully, someone else who likes yoga will use this, and if you have
suggestions or want to fork it, that would be pretty cool too.
