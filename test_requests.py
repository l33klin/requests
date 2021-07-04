#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests
import thread

from tests.testserver.test_server import run_server_with_auth


class RequestsTestSuite(unittest.TestCase):
	"""Requests test cases."""
	
	@classmethod
	def setUpClass(cls):
		cls.user = "user"
		cls.password = "password"
		cls.httpd = run_server_with_auth(user=cls.user, password=cls.password)
		sa = cls.httpd.socket.getsockname()
		cls.host = "http://localhost:{}".format(sa[1])
		cls.t = thread.start_new(cls.httpd.serve_forever, ())
	
	@classmethod
	def tearDownClass(cls):
		cls.httpd.shutdown()
	
	def setUp(self):
		pass

	def tearDown(self):
		"""Teardown."""
		pass
		
	def test_invalid_url(self):
		self.assertRaises(ValueError, requests.get, 'hiwpefhipowhefopw')

	def test_HTTP_200_OK_GET(self):
		r = requests.get('http://baidu.com')
		self.assertEqual(r.status_code, 200)

	def test_HTTPS_200_OK_GET(self):
		r = requests.get('https://baidu.com')
		self.assertEqual(r.status_code, 200)

	def test_HTTP_200_OK_HEAD(self):
		r = requests.head('http://baidu.com')
		self.assertEqual(r.status_code, 200)

	def test_HTTPS_200_OK_HEAD(self):
		r = requests.head('https://baidu.com')
		self.assertEqual(r.status_code, 200)

	def test_AUTH_HTTPS_200_OK_GET(self):
		auth = requests.AuthObject(self.user, self.password)
		url = self.host
		r = requests.get(url, auth=auth)

		self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
	unittest.main()
