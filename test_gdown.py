#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for gdown."""

import unittest

import gdown
from gdown import cli


class GdownTestCase(unittest.TestCase):

    #_multiprocess_can_split_ = True

    def setUp(self):
        """Setup."""
        self.modules = gdown.modules.__all__

    def tearDown(self):
        """Teardown."""
        pass

    # def testEntryPoints(self):
    #     gdown.getUrl
    #     gdown.getFile
    #     gdown.upload
    #     gdown.expireDate

    # def testInvalidHost(self):
    #     self.assertRaises(gdown.GdownError, gdown.core.getModule, 'sadasdasd')

    # def testInvalidAccount(self):
    #     for module in self.modules:
    #         self.assertRaises(gdown.exceptions.AccountError, gdown.expireDate, module, 'tadsasddsaasd', 'asdsadsads')

    # def testInvalidUrl(self):
    #     for module in self.modules:
    #         url = 'http://%s/testasdasdas' % (module)
    #         self.assertRaises(gdown.exceptions.ModuleError, gdown.getUrl, url, 'login', 'password')

    def testCli(self):
        self.assertEqual(gdown.__title__, cli.__title__)
        self.assertEqual(gdown.__version__, cli.__version__)
        self.assertEqual(gdown.__author__, cli.__author__)
        self.assertEqual(gdown.__license__, cli.__license__)
        self.assertEqual(gdown.__copyright__, cli.__copyright__)


if __name__ == '__main__':
    unittest.main()
