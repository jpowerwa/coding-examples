#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Determine if rectangles overlap.
"""

import collections

Point = collections.namedtuple('Point', 'x y')

class Rectangle(object):
    def __init__(self, min_x=None, max_x=None, min_y=None, max_y=None):
        for coord in (min_x, max_x, min_y, max_y):
            if coord is None:
                raise ValueError("All coordinates must be provided")
        if min_x >= max_x:
            raise ValueError("min_x must be < max_x")
        if min_y >= max_y:
            raise ValueError("min_y must be < max_y")
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def overlaps_rectangle(self, other):
        # check x-axis
        if other.max_x <= self.min_x or other.min_x >= self.max_x:
            return False
        # check y-axis
        if other.max_y <= self.min_y or other.min_y >= self.max_y:
            return False
        return True


if __name__ == '__main__':
    import unittest

    class TestRectanglesOverlap(unittest.TestCase):
        def setUp(self):
            self.rect = Rectangle(min_x=5, max_x=15, min_y=5, max_y=10)

        def test_overlap__top_left(self):
            """Verify that rectangle with top left corner overlapping is detected.
            """
            other_rect = Rectangle(min_x=7, max_x=20, min_y=1, max_y=7)
            self.assertTrue(self.rect.overlaps_rectangle(other_rect))
            self.assertTrue(other_rect.overlaps_rectangle(self.rect))

        def test_overlap__bottom_right(self):
            """Verify that rectangle with bottom right corner overlapping is detected.
            """
            other_rect = Rectangle(min_x=1, max_x=10, min_y=1, max_y=20)
            self.assertTrue(self.rect.overlaps_rectangle(other_rect))
            self.assertTrue(other_rect.overlaps_rectangle(self.rect))

        def test_overlap__to_the_left__false(self):
            """Verify that rectangle on the left is not detected as overlapping.
            """
            other_rect = Rectangle(min_x=1, max_x=4, min_y=7, max_y=15)
            self.assertFalse(self.rect.overlaps_rectangle(other_rect))
            self.assertFalse(other_rect.overlaps_rectangle(self.rect))

        def test_overlap__to_the_right__false(self):
            """Verify that rectangle on the right is not detected as overlapping.
            """
            other_rect = Rectangle(min_x=20, max_x=24, min_y=7, max_y=15)
            self.assertFalse(self.rect.overlaps_rectangle(other_rect))
            self.assertFalse(other_rect.overlaps_rectangle(self.rect))

        def test_overlap__above__false(self):
            """Verify that rectangle above is not detected as overlapping.
            """
            other_rect = Rectangle(min_x=7, max_x=10, min_y=11, max_y=15)
            self.assertFalse(self.rect.overlaps_rectangle(other_rect))
            self.assertFalse(other_rect.overlaps_rectangle(self.rect))

        def test_overlap__below__false(self):
            """Verify that rectangle below is not detected as overlapping.
            """
            other_rect = Rectangle(min_x=7, max_x=10, min_y=1, max_y=4)
            self.assertFalse(self.rect.overlaps_rectangle(other_rect))
            self.assertFalse(other_rect.overlaps_rectangle(self.rect))

        def test_overlap__contained(self):
            """Verify that interior rectangle is detected as overlapping.
            """
            other_rect = Rectangle(min_x=7, max_x=12, min_y=7, max_y=9)
            self.assertTrue(self.rect.overlaps_rectangle(other_rect))
            self.assertTrue(other_rect.overlaps_rectangle(self.rect))

        def test_overlap__containing(self):
            """Verify that framing rectangle is detected as overlapping.
            """
            other_rect = Rectangle(min_x=1, max_x=16, min_y=1, max_y=12)
            self.assertTrue(self.rect.overlaps_rectangle(other_rect))
            self.assertTrue(other_rect.overlaps_rectangle(self.rect))

    # run tests
    unittest.main()
