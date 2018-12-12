# -*- coding: utf-8 -*-
"""
Fit Images plugin for Pelican
================================
Add Fit Images to section titles of the article
"""

from pelican import signals




def process_content(content):
    if content._content is None:
        return

    content._content = content._content.replace('<img', '<img style="max-width:96%;margin:5px 2% 5px 2%"')


def register():
    signals.content_object_init.connect(process_content)
