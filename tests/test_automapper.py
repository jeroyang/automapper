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

from automapper import automapper


class TestAutomapper(unittest.TestCase):

    def test_strip_tags(self):
        markup = '<a href="123">hell<b>o</b></a><br/>'
        result = automapper.strip_tags(markup)
        wanted = 'hello'
        self.assertEqual(result, wanted)
        
    def test_similarity(self):
        a = '123'
        b = '2345'
        result = automapper.similarity(a, b)
        wanted = 2.0 / 4.0
        self.assertEqual(result, wanted)
        
    def test_mutate(self):
        text = 'hello'
        result = list(automapper.mutate(text))
        wanted = ['hello']
        self.assertEqual(result, wanted)
        
        text = '<b>hello</b>'
        result = list(automapper.mutate(text))
        wanted = ['<b>hello</b>', 'hello']
        self.assertEqual(result, wanted)
        
        text = '<b>hello&gt;</b>'
        result = list(automapper.mutate(text))
        wanted = ['<b>hello&gt;</b>', 'hello&gt;', 'hello>']
        self.assertEqual(result, wanted)
    
        