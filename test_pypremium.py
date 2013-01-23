#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''tests for pypremium'''

import unittest

import pypremium

class PypremiumTestCase(unittest.TestCase):
	
	_multiprocess_can_split_ = True
	
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
	
	def testStatus(self):
		'''Tests status function on free account'''
		for module in modules():
			if hasattr(module, 'status'):
				self.assertEqual(module.status('pypremium', 'test'), 0)

def modules():
	modules_list = []
	for module_name in pypremium.modules.__all__:
		modules_list.append(getattr(pypremium, module_name))
	return modules_list

if __name__ == '__main__':
	unittest.main()
