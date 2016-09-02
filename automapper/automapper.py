#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import re

try:
    # python 3.4+
    from html import unescape
except:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
    h = HTMLParser()
    unescape = h.unescape
from collections import OrderedDict

from lxml import etree

from automapper.longest_common_subsequence import lcs

def strip_tags(markup):
    """
    Remove tags from the markup string
    >>> strip_tags('<a href="123">hell<b>o</b></a><br/>')
    hello
    """
    tag = r'</?\w+( .*?)?/?>'
    return re.sub(tag, '', markup)

def peel(markup):
    """
    Remove the outmost markup tags
    """
    tagpair =r'(?s)^\s*<(\w+)( .*)?>(.*)</\1>\s*$'
    content = re.sub(tagpair, r'\3', markup)
    return content.strip()

def similarity(a, b):
    """
    Return the similarity of two strings based on longest_common_subsequence
    """
    return float(len(lcs(a, b))) / max(len(a), len(b))

def score(a, b):
    """
    Return a herustic score of a and b
    """
    return similarity(a, b)
    
filters = OrderedDict((
            (0, lambda x: x),
            (1, strip_tags),
            (2, unescape)
            ))
class Model(dict):
    """
    The model is dict which holds a flat representation of xml or html tree, mapping from xpath to content
    """
    
    def search(self, query, n=None, threshold=None):
        """
        Given content, return the first n results ranked by their scores.
        If the threshold is set, only the results which score is greater than the threshold will be returned.
        """
        candidates = []
        for xpath, content in self.items():
            score2filter = dict()
            for name, filtfunc in list(filters.items())[::-1]:
                the_score = score(query, filtfunc(content))
                score2filter[the_score] = name
            best_result = sorted(list(score2filter.items()), key=lambda i: i[0], reverse=True)[0]
            best_score, best_filter = best_result
            candidates.append((best_score, best_filter, xpath))
        
        candidates.sort(key=lambda c: c[1])
        candidates.sort(key=lambda c: c[0], reverse=True)
        
        if threshold is not None:
            candidates = [c for c in candidates if c[0] >=threshold]
            
        if n is None:
            return candidates
        else:
            return candidates[:n]
            
        
    @classmethod
    def fromlxml(cls, xml):
        """
        A factory which returns a Model from an XML or HTML tree (from lxml)
        """
        model = cls()
        tree = etree.ElementTree(xml)
        for node in tree.iter():
            raw_content = etree.tostring(node, with_tail=False, encoding='unicode')
            xpath = tree.getpath(node)
            content = peel(raw_content)
            model[xpath] = content
            
        return model
        
        
        