#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import re
from html import unescape

from longest_common_subsequence import lcs

def strip_tags(markup):
    """
    Remove tags from the markup string
    >>> strip_tags('<a href="123">hell<b>o</b></a><br/>')
    hello
    """
    tag = r'</?\w+( .*?)?/?>'
    return re.sub(tag, '', markup)

def similarity(a, b):
    """
    Return the similarity of two strings based on longest_common_subsequence
    """
    return float(len(lcs(a, b))) / max(len(a), len(b))

def mutate(text):
    """
    Yield the text firstly, if the text has markup tags, then yield the strip_tags(text). If the text has html escape, yield the unescaped version of the text
    """
    yield text
    
    no_tags = strip_tags(text)
    if no_tags != text:
        yield no_tags
        
    no_escape = unescape(no_tags)
    if no_escape != no_tags:
        yield no_escape
        