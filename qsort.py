#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Because everyone loves quicksort.
"""

import logging

num_tabs = 0

def quicksort(items, start_idx=None, end_idx=None):
    """
    :type items: list of comparable objects
    :arg items: items to be sorted

    :type start_idx: int
    :arg start_idx: optional index of first item to be sorted; defaults to 0

    :type end_idx: int
    :arg end_idx: optional index of last item to be sorted; defaults to len(items) -1

    """
    if start_idx is None:
        start_idx = 0
    if end_idx is None:
        end_idx = len(items)-1 if items else 0

    if start_idx < end_idx:
        log_debug("reordering items {0}-{1}: {2}".format(
                start_idx, end_idx, items[start_idx:end_idx-start_idx+1]))
        pivot_idx = partition(items, start_idx, end_idx)
        log_debug("splitting on item {0}; items={1}".format(pivot_idx, items))

        global num_tabs
        num_tabs += 1

        quicksort(items, start_idx=start_idx, end_idx=pivot_idx-1)
        quicksort(items, start_idx=pivot_idx+1, end_idx=end_idx)


def partition(items, start_idx, end_idx):
    """Reorder items around some pivot item.

    Items before the pivot are less than or equal to the pivot and items after the pivot 
    are greater than the pivot.

    :rtype: int
    :return: index of pivot item

    :type start_idx: int
    :arg start_idx: index of first item to be reordered

    :type end_idx: int
    :arg end_idx: index of last item to be reordered

    """
    pivot_idx = end_idx
    pivot_val = items[pivot_idx]

    placeholder_idx = start_idx
    i = placeholder_idx 

    log_debug('pivot_val={0}'.format(pivot_val))

    while i < end_idx:
        # if current item is less than or equal to the pivot value, swap it with placeholder item
        if items[i] <= pivot_val:
            log_debug('[{0}] {1} <= {2}; swapping {1} with {3}'.format(
                    i, items[i], pivot_val, items[placeholder_idx]))
            items[placeholder_idx], items[i] = items[i], items[placeholder_idx]
            placeholder_idx += 1
        else:
            log_debug('[{0}] {1} > {2}; do nothing'.format(i, items[i], pivot_val))
        i += 1
        
    # swap pivot value with placeholder value
    log_debug('swapping pivot {0} with placeholder {1}'.format(pivot_val, items[placeholder_idx]))
    items[placeholder_idx], items[pivot_idx] = items[pivot_idx], items[placeholder_idx]

    # return location of pivot
    return placeholder_idx
    

def log_debug(msg):
    logging.debug("{0}{1}".format('  '*num_tabs, msg))
    

        
if __name__ == '__main__':
    import unittest

    class TestQuicksort(unittest.TestCase):
        def test_sanity(self):
            """Test sanity
            """
            self.assertTrue(True)

        def test_short(self):
            """Verify sorting short list of items.
            """
            items = ['b', 'z', 'm', 'q', 'j', 'o']
            quicksort(items)
            self.assertEqual(sorted(items), items)
            
        def test_empty(self):
            """Verify sorting empty list.
            """
            items = []
            quicksort(items)
            self.assertEqual([], items)

        def test_one_item(self):
            """Verify sorting list of single item.
            """
            items = ['g']
            quicksort(items)
            self.assertEqual(['g'], items)

    # set logging to DEBUG
    logging.basicConfig(level=logging.DEBUG)

    # run tests
    unittest.main()
