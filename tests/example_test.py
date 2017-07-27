# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from vim_turing_machine import example


def test_hello():
    assert example.hello() == 'world'
