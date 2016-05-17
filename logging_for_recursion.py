# -*- coding: utf-8 -*-

"""Logging utility with formatting based on recursion depth.
"""

import logging as pylogging

recursion_depth = 0

def increment_recursion_depth(increment=1):
    global recursion_depth
    recursion_depth += increment

def debug(msg):
    pylogging.debug("{0}{1}".format('   '*recursion_depth, msg))


