#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate all possible words from provided set of letters.
"""

import logging
import math

def generate_combos(letters):
    if not letters:
        return letters
    if len(letters) == 1:
        return [letters[0]]

    combos = []
    for i in range(0, len(letters)):
        letter_i = letters[i]
        other_letters = letters[0:i] + letters[i+1:]
        for subcombo in generate_combos(other_letters):
            combos.append(letters[i] + subcombo)
    return combos
        
        
if __name__ == '__main__':
    import unittest

    class TestGenerateCombos(unittest.TestCase):
        def _run(self, letters):
            combos = generate_combos(list(letters))
            self.assertEqual(math.factorial(len(letters)), len(combos))

        def test_abc(self):
            self._run('abc')

        def test_fraggle(self):
            self._run("fraggle")
            
        def test_none(self):
            self.assertIsNone(generate_combos(None))

        def test_empty_list(self):
            self.assertEqual([], generate_combos([]))

        def test_single_letter(self):
            self.assertEqual(['a'], generate_combos(['a']))

    # run tests
    unittest.main()
