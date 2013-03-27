#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for gdown."""

import unittest

import gdown


class GdownTestCase(unittest.TestCase):

    _multiprocess_can_split_ = True

    def setUp(self):
        """Create simple data set with headers."""
        pass

    def tearDown(self):
        """Teardown."""
        pass

    def test_entry_points(self):
        gdown.modules

    def testStatus(self):
        """Tests status function on free account."""
        for module in modules():
            if hasattr(module, 'status'):
                print module.__name__
                self.assertEqual(module.status('gdown', 'gdown'), 0)


def modules():
    modules_list = []
    for module_name in gdown.modules.__all__:
        modules_list.append(getattr(gdown, module_name))
    return modules_list

if __name__ == '__main__':
    unittest.main()
