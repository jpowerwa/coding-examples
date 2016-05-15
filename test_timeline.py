#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for timeline functionality.
"""

from __future__ import print_function, unicode_literals

import logging
import unittest

from timeline import Timeline


class TimelineTests(unittest.TestCase):
    """Exercise Timeline class logic.
    """

    def test_init(self):
        """Verify init with no args.
        """
        timeline = Timeline()
        self.assertEqual({}, timeline._preceding_events)

    def test_get_merged_timelines__empty(self):
        """Verify that get_merged_timelines returns list of empty list when there is no data.
        """
        timeline = Timeline()
        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual([[]], merged_timelines)

    def test_merge_timelines__unambiguous(self):
        """Verify that unambiguous partial timelines are correctly merged.
        """
        partial_timelines = [
            ['shouting', 'fight', 'fleeing'],
            ['fight', 'gunshot', 'panic', 'fleeing'],
            ['anger', 'shouting']]
        timeline = Timeline()
        for t in partial_timelines:
            timeline.merge_partial_timeline(t)

        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual([['anger', 'shouting', 'fight', 'gunshot', 'panic', 'fleeing']],
                         merged_timelines)

    def test_merge_timelines__two_possibilities(self):
        """Verify that ambiguous partial timelines are correctly merged into two possibilities.
        """
        partial_timelines = [
            ['shouting', 'fight', 'fleeing'],
            ['fight', 'gunshot', 'fleeing'],
            ['fight', 'screaming', 'fleeing']]
        expected_timelines = [
            ['shouting', 'fight', 'gunshot', 'screaming', 'fleeing'],
            ['shouting', 'fight', 'screaming', 'gunshot', 'fleeing']]

        timeline = Timeline()
        for t in partial_timelines:
            timeline.merge_partial_timeline(t)

        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual(len(expected_timelines), len(merged_timelines))
        for merged_timeline in merged_timelines:
            self.assertTrue(merged_timeline in expected_timelines)

    def test_merge_timelines__three_possibilities(self):
        """Verify that ambiguous partial timelines are correctly merged into three possibilities.
        """
        partial_timelines = [
            ['pouring gas', 'laughing', 'lighting match', 'fire'],
            ['buying gas', 'pouring gas', 'crying', 'fire', 'smoke']]
        expected_timelines = [
            ['buying gas', 'pouring gas', 'laughing', 'lighting match', 'crying', 'fire', 'smoke'],
            ['buying gas', 'pouring gas', 'crying', 'laughing', 'lighting match', 'fire', 'smoke'],
            ['buying gas', 'pouring gas', 'laughing', 'crying', 'lighting match', 'fire', 'smoke']]

        timeline = Timeline()
        for t in partial_timelines:
            timeline.merge_partial_timeline(t)

        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual(len(expected_timelines), len(merged_timelines))
        for merged_timeline in merged_timelines:
            self.assertTrue(merged_timeline in expected_timelines)


if __name__ == '__main__':

    # set logging to DEBUG if desired
    logging.basicConfig(level=logging.DEBUG)

    # run tests
    unittest.main()

