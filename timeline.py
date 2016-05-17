# -*- coding: utf-8 -*-

"""
Timeline class combines partial lists of ordered events into longest possible unambiguous sequences.
"""

import collections
import itertools

import logging_for_recursion as logging


class Timeline(object):
    def __init__(self, partial_timelines=None):
        """Initialize Timeline instance with provided partial timelines.

        Partial timelines can be added later using the add_partial_timeline method.

        :type partial_timelines: [[unicode]]
        :arg partial_timelines: list of ordered lists of strings that are events

        """
        # Map events to sets of subsequent events
        self._subsequent_events = collections.defaultdict(set)

        # Merge partial timelines
        for timeline in partial_timelines or []:
            self.add_partial_timeline(timeline)

    def add_partial_timeline(self, partial_timeline):
        """Add events from provided timeline to internal data.

        :type partial_timeline: [<unicode>
        :arg partial_timeline: ordered list of strings that are events

        """
        for i, event in enumerate(partial_timeline or []):
            if event not in self._subsequent_events:
                self._subsequent_events[event] = set()
            if i > 0:
                self._add_subsequent_event(partial_timeline[i-1], event)
            if i < len(partial_timeline)-1:
                self._add_subsequent_event(event, partial_timeline[i+1])

    def get_merged_timelines(self):
        """Merge partial timelines to generate longest possible unambiguous sequences of events.

        Multiple timelines will be returned if a single absolute ordering of events cannot
        be determined based on the partial timelines. For example, if one timeline specifes
        that event 'x' occurred after 'w' and before 'z', and another timeline specifies that
        event 'y' occurred after 'w' and before 'z', the absolute ordering of 'x' and 'y' 
        cannot be determined, and multiple timelines will be returned.

        :rtype: [[unicode]]
        :return: list of ordered lists of events

        """
        return self._get_merged_timelines__recurse()


    # private methods

    def _add_subsequent_event(self, event, subsequent_event):
        """Add specified subsequent_event to self._subsequent_events for event.

        :raise: ValueError if specified subsequent_event is already recorded as coming before event

        :type event: <unicode>
        :arg event: name of current event

        :type subsequent_event: <unicode>
        :arg subsequent_event: name of event succeeding current event

        """
        subsequent_events = self._get_all_subsequent_events(subsequent_event) 
        if subsequent_events and event in subsequent_events:
            raise ValueError(
                "Contradiction detected: event '{0}' comes before and after event '{1}'".format(
                    event, subsequent_event))
        self._subsequent_events[event].add(subsequent_event)

    def _dedupe_timelines(self, timelines):
        """Filter out timelines that are exactly contained by other timelines.

        :rtype: [[unicode]]
        :return: subset of timelines with unique event sequences

        :type timelines: [[unicode]]
        :arg timelines: list of ordered lists of events

        """
        if len(timelines) == 1:
            return [timelines[0]]

        logging.debug("Combining overlapping timelines {0}".format(timelines))

        # Since we trust the order of the events within each timeline, we can find
        # timelines that are included in another timeline by comparing sets of events.
        timeline_events = [set(events) for events in timelines]

        # Build list of booleans indicating if each timeline is unique or not.
        unique_timeline_selectors = [True for i in range(len(timelines))]

        for i in range(len(timelines)-1):
            i_events = timeline_events[i]
            for j in range(i+1, len(timelines)):
                j_events = timeline_events[j]
                if i_events.issubset(j_events):
                    unique_timeline_selectors[i] = False
                if j_events.issubset(i_events):
                    unique_timeline_selectors[j] = False

        return itertools.compress(timelines, unique_timeline_selectors)

    def _get_all_subsequent_events(self, event):
        direct_events = self._subsequent_events.get(event)
        if not direct_events:
            return None
        subsequent_events = set()
        for event in direct_events:
            subsequent_events.add(event)
            indirect_events = self._get_all_subsequent_events(event)
            if indirect_events:
                subsequent_events.update(indirect_events)
        return subsequent_events

    def _find_first_events(self):
        """Find events with no preceding events.

        :rtype: set(unicode)
        :return: set of events that have no preceding events

        """
        all_events = set(self._subsequent_events.keys())
        all_subsequent_events = set()
        for subsequent_events in self._subsequent_events.values():
            [all_subsequent_events.add(e) for e in subsequent_events]
        return all_events.difference(all_subsequent_events)

    def _get_next_events(self, from_event=None):
        """Find all events that succeed specified event.

        :rtype: set(unicode)
        :return: set of events that succeed specified event

        :type from_event: unicode
        :arg from_event: event for which subsequent events should be found

        """
        if not from_event:
            return self._find_first_events()
        return self._subsequent_events.get(from_event) or set()

    def _get_merged_timelines__recurse(self, from_event=None):
        """Internal recursive method for generating ordered timelines starting from specified event.

        :rtype: [[unicode]]
        :return: list of ordered lists of events

        :type from_event: unicode
        :arg from_event: optional name of starting event; None to begin

        """
        next_events = self._get_next_events(from_event=from_event)
        if not next_events:
            return [[]]

        # Generate timelines starting at each possible next event
        merged_timelines = []
        for next_event in next_events:
            logging.debug("from_event={0}".format(from_event))
            logging.debug("next_event={0}".format(next_event))
            logging.increment_recursion_depth()
            sub_timelines = self._get_merged_timelines__recurse(from_event=next_event)

            # Discard sub_timelines that are represented by other sub_timelines.
            # In practice, I think that duplicate timelines will match the end of another
            # timeline, but look for any overlap just in case.
            for timeline in self._dedupe_timelines(sub_timelines):
                merged_timelines.append([next_event] + timeline)
            logging.increment_recursion_depth(-1)
        logging.debug("Returning timelines {0}".format(merged_timelines))
        return merged_timelines


if __name__ == '__main__':
    """Command-line driver for merging arbitrary timeline data and displaying merged timelines.
    """
    import argparse
    import logging as pylogging
    import json
    import pprint

    parser = argparse.ArgumentParser(
        description='Combine partial timelines into longest possible sequences of events',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('infile',
                        help='input filename containing JSON list of ordered event sequences')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true', help='info-level output')
    group.add_argument('-V', '--very-verbose', action='store_true', help='debug-level output')
    args = parser.parse_args()
    
    # set logging to INFO or DEBUG based on command line arg
    log_level = pylogging.ERROR
    if args.verbose:
        log_level = pylogging.INFO
    elif args.very_verbose:
        log_level = pylogging.DEBUG
    pylogging.basicConfig(level=log_level)

    # read data from input file
    partial_timelines = None
    with open(args.infile) as infile:
        try:
            partial_timelines = json.loads(infile.read())
        except ValueError:
            raise

    if partial_timelines:
        pylogging.info('Input timelines: {0}'.format(partial_timelines))

        # Merge partial timelines
        timeline = Timeline(partial_timelines=partial_timelines)
        merged_timelines = timeline.get_merged_timelines()

        print('\nMerged timelines:')
        for t in merged_timelines:
            print(t)


