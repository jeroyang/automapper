#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

"""
test_automapper
----------------------------------

Tests for `automapper` module.
"""

import unittest

from lxml import etree

from automapper import automapper

class TestAutomapper(unittest.TestCase):

    def test_strip_tags(self):
        markup = '<a href="123">hell<b>o</b></a><br/>'
        result = automapper.strip_tags(markup)
        wanted = 'hello'
        self.assertEqual(result, wanted)
    
    def test_peel(self):
        markup = '<div><b>good</b> word</div>'
        result = automapper.peel(markup)
        wanted = '<b>good</b> word'
        self.assertEqual(result, wanted)
        
    def test_similarity(self):
        a = '123'
        b = '2345'
        result = automapper.similarity(a, b)
        wanted = 2.0 / 4.0
        self.assertEqual(result, wanted)
    
    def test_score(self):
        a = '123'
        b = '2345'
        result = automapper.score(a, b)
        wanted = 2.0 / 4.0
        self.assertEqual(result, wanted)
        
class TestModel(unittest.TestCase):
        
    def setUp(self):
        text = """<html>
    <head>
    </head>
    <body>
        <h1>Title</h1>
        
        <p>hell<b>o</b></p>
        <p>hello</p>
        <p>w<b>o</b>rld</p>
        <br />
        <p>bob</p>
        tail
    </body>
</html>"""
        xml = etree.fromstring(text)
        model = automapper.Model.fromlxml(xml)
        self.model = model
        
    def test_fromlxml(self):
        model = self.model
        self.assertEqual(model['/html/body/p[1]'], 'hell<b>o</b>')
        self.assertEqual(model['/html/body/p[2]'], 'hello')
        
    def test_search(self):
        model = self.model
        result = model.search('hello', n=3, threshold=0.5)
        wanted = [(1.0, 0, '/html/body/p[2]'),
                 (1.0, 1, '/html/body/p[1]')]
        self.assertEqual(result, wanted)
        
        