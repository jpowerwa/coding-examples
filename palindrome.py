#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Determine if provided word is palindrome.
"""

import logging


def is_palindrome(in_string):
    if in_string is None:
        return False

    letters = list(in_string)
    i = 0
    j = len(letters) - 1

    while i<j:
        while _skip_char(letters[i]) and i<j:
            i += 1
        while _skip_char(letters[j]) and i<j:
            j -= 1
        if letters[i].lower() != letters[j].lower():
            return False
        i += 1
        j -= 1
    return True

def _skip_char(c):
    return not c.isalnum()


if __name__ == '__main__':
    import unittest

    class TestIsPalindrome(unittest.TestCase):
        def test_palindrome__odd(self):
            self.assertTrue(is_palindrome('aba'))

        def test_palindrome__ci(self):
            self.assertTrue(is_palindrome('abA'))

        def test_palindrome__even(self):
            self.assertTrue(is_palindrome('abba'))

        def test_palindrome__single_letter(self):
            self.assertTrue(is_palindrome('a'))

        def test_palindrome__odd__false(self):
            self.assertFalse(is_palindrome('abc'))

        def test_palindrome__even__false(self):
            self.assertFalse(is_palindrome('abca'))

        def test_palindrome__empty_string(self):
            self.assertTrue(is_palindrome(''))
            
        def test_palindrome__none(self):
            self.assertFalse(is_palindrome(None))

        def test_sentence(self):
            self.assertTrue(is_palindrome("A man, a plan, a canal... Panama!"))

        def test_all_punc(self):
            self.assertTrue(is_palindrome('......'))

    # run tests
    unittest.main()
