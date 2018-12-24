#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = 'Brian'
SITENAME = 'KNOWN'
SITEURL = 'https://brianshen1990.github.io/'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

STATIC_PATHS = ['images']

LOAD_CONTENT_CACHE = False

THEME='./notmyideaBrian'

GOOGLE_ANALYTICS = 'UA-107750695-1'

DISQUS_SITENAME = "brianshen1990"

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['section_number']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# source venv/bin/activate
# make html && make serve
# make github