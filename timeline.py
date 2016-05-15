#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Coding exercise that reconstructs event timeline based on partial eyewitness accounts.
"""

import collections
import logging

recursion_depth = 0
def log_debug(msg):
    logging.debug("{0}{1}".format('  '*recursion_depth, msg))

class Timeline(object):
    def __init__(self, partial_timelines=None):
        """Initialize instance with partial timelines if provided. 

        If no partial timelines are provided at instantiation, they can be added later
        using the merge_partial_timeline method.

        :type partial_timelines: [[unicode]]
        :arg partial_timelines: list of ordered lists of strings that are event names

        """
        # Map event names to sets of preceding events
        self._preceding_events = collections.defaultdict(set)

        # Merge partial timelines
        for timeline in partial_timelines or []:
            self.merge_partial_timeline(timeline)

    def merge_partial_timeline(self, partial_timeline):
        """
        :type partial_timeline: [<unicode>
        :arg partial_timeline: ordered list of strings that are event names
        """
        for i, event in enumerate(partial_timeline):
            if event not in self._preceding_events:
                self._preceding_events[event] = set()
            for preceding_event in partial_timeline[0:i]:
                self._add_preceding_event(event, preceding_event)
            for subsequent_event in partial_timeline[i+1:]:
                self._add_preceding_event(subsequent_event, event)

    def _add_preceding_event(self, event, preceding_event):
        """
        :type event: <unicode>
        :arg event: name of current event

        :type preceding_event: <unicode>
        :arg preceding_event: name of event preceding current event

        """
        self._preceding_events[event].add(preceding_event)

    def get_merged_timelines(self):
        log_debug("Merging timelines...")
        used_events = set()
        merged_timelines = self._get_merged_timelines__recurse(used_events)
        log_debug("Merged timelines: {0}".format(merged_timelines))
        return merged_timelines

    def _get_merged_timelines__recurse(self, used_events):
        if len(used_events) == len(self._preceding_events.keys()):
            return [[]]

        possible_timelines = []
        for next_event in self._get_next_unused_events(used_events):
            used_events.add(next_event)
            log_debug("Found next event: {0}".format(next_event))
            log_debug("Used events: {0}".format(sorted(list(used_events))))
            global recursion_depth
            recursion_depth += 1
            for possible_timeline in self._get_merged_timelines__recurse(used_events):
                possible_timelines.append([next_event] + possible_timeline)
            recursion_depth -= 1
            used_events.remove(next_event)
        return possible_timelines

    def _get_next_unused_events(self, used_events):
        """Find all events with no unused, preceding events.

        :rtype: [unicode]
        :return: names of unused events that have no preceding, unused events

        :type used_events: set
        :arg used_events: set of events that should not be considered

        """
        next_events = []
        for event in filter(lambda e: e not in used_events, self._preceding_events.keys()):
            preceding_events = self._preceding_events[event].difference(used_events)
            if len(preceding_events) == 0:
                next_events.append(event)
        return next_events
        


        
