# -*- coding: utf-8 -*-

"""Tests for timeline functionality.

If not python 3, pip install mock.
"""

from __future__ import print_function, unicode_literals

import logging
import mock
import unittest

from timeline import Timeline

from pprint import pprint

class TimelineTests(unittest.TestCase):
    """Exercise Timeline class logic.
    """

    def test_init(self):
        """Verify init with no args.
        """
        timeline = Timeline()
        self.assertEqual({}, timeline._subsequent_events)

    @mock.patch.object(Timeline, 'add_partial_timeline')
    def test_init(self, mock_merge_timeline):
        """Verify init with partial timelines calls add_partial_timelines.
        """
        partial_timelines = [mock.Mock(name='partial_timeline_1'),
                             mock.Mock(name='partial_timeline_2')]
        timeline = Timeline(partial_timelines=partial_timelines)

        # Verify mocks
        self.assertEqual([mock.call(t) for t in partial_timelines],
                         mock_merge_timeline.call_args_list)

    def test_add_partial_timeline__simple(self):
        """Verify side-effects of single call to add_partial_timeline.
        """
        partial_timeline = ['one', 'two', 'three', 'four']
        timeline = Timeline()
        timeline.add_partial_timeline(partial_timeline)

        # Verify internal timeline data
        expected_subsequent_events = {'one': set(['two']),
                                      'two': set(['three']),
                                      'three': set(['four']),
                                      'four': set()}
        self.assertEqual(expected_subsequent_events, timeline._subsequent_events)

    def test_add_partial_timeline__overlapping(self):
        """Verify side-effects of calling add_partial_timeline with overlapping timelines.
        """
        partial_timelines = [['two', 'three', 'six'],
                             ['three', 'four', 'five', 'six', 'seven'],
                             ['one', 'two']]
        timeline = Timeline(partial_timelines=partial_timelines)

        # Verify internal timeline data
        expected_subsequent_events = {'one': set(['two']),
                                      'two': set(['three']),
                                      'three': set(['six', 'four']),
                                      'four': set(['five']),
                                      'five': set(['six']),
                                      'six': set(['seven']),
                                      'seven': set()}
        self.assertEqual(expected_subsequent_events, timeline._subsequent_events)

    def test_add_partial_timeline__contradiction(self):
        """Verify that order contradiction is detected and avoided.
        """
        partial_timelines = [
            ['one', 'two', 'three'],
            ['three', 'two']]
        timeline = Timeline()
        timeline.add_partial_timeline(partial_timelines[0])
        self.assertRaisesRegexp(
            ValueError,
            "Contradiction detected: event 'three' comes before and after event 'two'",
            timeline.add_partial_timeline,
            partial_timelines[1])

    def test_get_all_subsequent_events__simple(self):
        """Verify behavior of _get_all_subsequent_events.
        """
        timeline = Timeline()
        timeline._subsequent_events = {'one': set(['two']),
                                      'two': set(['three']),
                                      'three': set(['four']),
                                      'four': set()}
        subsequent_events = timeline._get_all_subsequent_events('one')
        self.assertEqual(set(['two', 'three', 'four']), subsequent_events)

    def test_get_all_subsequent_events__branching(self):
        """Verify behavior of _get_all_subsequent_events when events overlap.
        """
        timeline = Timeline()
        timeline._subsequent_events = {'one': set(['two']),
                                       'two': set(['three']),
                                       'three': set(['six', 'four']),
                                       'four': set(['five']),
                                       'five': set(['six']),
                                       'six': set(['seven']),
                                       'seven': set()}
        subsequent_events = timeline._get_all_subsequent_events('one')
        self.assertEqual(set(['two', 'three', 'four', 'five', 'six', 'seven']), subsequent_events)

    def test_get_merged_timeline__none(self):
        """Verify merged timeline of nothing.
        """
        timeline = Timeline()
        self.assertEqual([[]], timeline.get_merged_timelines())

    def test_get_merged_timeline__single_timeline(self):
        """Verify merged timeline of exactly one partial timeline.
        """
        partial_timeline = ['one', 'two', 'three', 'four']
        timeline = Timeline(partial_timelines=[partial_timeline])

        # Verify get_merged_timelines return value
        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual([partial_timeline], merged_timelines)

    def test_get_merged_timelines__full_merge__start_and_end_overlap(self):
        """Verify that unambiguous overlapping timelines merge correctly.
        """
        partial_timelines = [['two', 'three', 'six'],
                             ['six', 'seven'],
                             ['one', 'two']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual([['one', 'two', 'three', 'six', 'seven']],
                         merged_timelines)

    def test_get_merged_timelines__full_merge__interleaved(self):
        """Verify that unambiguous interleaved timelines merge correctly.
        """
        partial_timelines = [['two', 'three', 'seven'],
                             ['three', 'four', 'five', 'seven']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual([['two', 'three', 'four', 'five', 'seven']],
                         merged_timelines)

    def test_get_merged_timelines__full_merge__longer(self):
        """Verify that unambiguous partial timelines merge correctly.
        """
        partial_timelines = [['two', 'three', 'six'],
                             ['three', 'four', 'five', 'six', 'seven'],
                             ['one', 'two']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual([['one', 'two', 'three', 'four', 'five', 'six', 'seven']],
                         merged_timelines)

    def test_get_merged_timelines__partial_merge(self):
        """Verify that ambiguous partial timelines are merged as far as possible.
        """
        partial_timelines = [['two', 'three', 'four', 'six'],
                             ['one', 'two', 'five', 'six', 'seven']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        expected_timelines = [
            ['one', 'two', 'three', 'four', 'six', 'seven'],
            ['one', 'two', 'five', 'six', 'seven']]
        self.assertEqual(len(expected_timelines), len(merged_timelines))
        for merged_timeline in merged_timelines:
            self.assertTrue(merged_timeline in expected_timelines)

    def test_get_merged_timelines__full_merge__shooting_example(self):
        """Verify that full merge is possible for shooting example.
        """
        partial_timelines = [
            ['shouting', 'fight', 'fleeing'],
            ['fight', 'gunshot', 'panic', 'fleeing'],
            ['anger', 'shouting']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        self.assertEqual([['anger', 'shouting', 'fight', 'gunshot', 'panic', 'fleeing']],
                         merged_timelines)

    def test_get_merged_timelines__partial_merge__arson_example(self):
        """Verify that partial merge is possible for arson example.
        """
        partial_timelines = [
            ['pouring gas', 'laughing', 'lighting match', 'fire'],
            ['buying gas', 'pouring gas', 'crying', 'fire', 'smoke']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        expected_timelines = [
            ['buying gas', 'pouring gas', 'crying', 'fire', 'smoke'],
            ['buying gas', 'pouring gas', 'laughing', 'lighting match', 'fire', 'smoke']]
        self.assertEqual(len(expected_timelines), len(merged_timelines))
        for merged_timeline in merged_timelines:
            self.assertTrue(merged_timeline in expected_timelines)

    def test_get_merged_timelines__partial_merge__foiled_mugging_example(self):
        """Verify that partial merge is possible for foiled_mugging example.
        """
        partial_timelines = [
            ['shadowy figure', 'demands', 'scream', 'siren'],
            ['shadowy figure', 'pointed gun', 'scream']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        expected_timelines = [
            ['shadowy figure', 'demands', 'scream', 'siren'],
            ['shadowy figure', 'pointed gun', 'scream', 'siren']]
        self.assertEqual(len(expected_timelines), len(merged_timelines))
        for merged_timeline in merged_timelines:
            self.assertTrue(merged_timeline in expected_timelines)

    def test_get_merged_timelines__no_merge__scandal_example(self):
        """Verify that no merge is possible for scandal example.
        """
        partial_timelines = [
            ['argument', 'coverup', 'pointing'],
            ['press brief', 'scandal', 'pointing'],
            ['argument', 'bribe']]
        timeline = Timeline(partial_timelines=partial_timelines)

        merged_timelines = timeline.get_merged_timelines()
        expected_timelines = partial_timelines
        self.assertEqual(len(expected_timelines), len(merged_timelines))
        for merged_timeline in merged_timelines:
            self.assertTrue(merged_timeline in expected_timelines)


if __name__ == '__main__':
    import sys
          
    # set logging to DEBUG based on command line arg
    log_level = logging.DEBUG if '-v' in sys.argv else logging.ERROR
    logging.basicConfig(level=log_level)

    # run tests
    unittest.main()

