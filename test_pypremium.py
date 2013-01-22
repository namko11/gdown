#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import pypremium

class RequestsTestCase(unittest.TestCase):
	
	#_multiprocess_can_split_ = True
	
	def setUp(self):
		"""Create simple data set with headers."""
		pass

	def tearDown(self):
		"""Teardown."""
		pass

	def test_assertion(self):
		assert 1

	def test_entry_points(self):
		pypremium.modules
	
	def test_bitshare(self):
		'''free account'''
		assert pypremium.bitshare.status('oczkers', 'mandrake') == 0

if __name__ == '__main__':
	unittest.main()
