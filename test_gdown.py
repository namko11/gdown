#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for gdown."""

import unittest

import gdown


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
    #         self.assertRaises(gdown.ModuleError, gdown.getUrl, url, 'login', 'password')


if __name__ == '__main__':
    unittest.main()
