#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import requests

from tests.testserver.server import get_server


class RequestsTestSuite(unittest.TestCase):
    """Requests test cases."""
    
    @classmethod
    def setUpClass(cls):
        cls.user = "user"
        cls.password = "password"
        cls.test_servers = []
        cls.auth_server = get_server("auth", auth=(cls.user, cls.password))
        cls.test_servers.append(cls.auth_server)
        cls.upload_server = get_server("upload")
        cls.test_servers.append(cls.upload_server)
        
        for server in cls.test_servers:
            server.run_background()
    
    @classmethod
    def tearDownClass(cls):
        for server in cls.test_servers:
            server.close()
    
    def setUp(self):
        pass
    
    def test_HTTP_200_OK_GET(self):
        r = requests.get('http://baidu.com')
        self.assertEqual(r.status_code, 200)
    
    def test_invalid_url(self):
        self.assertRaises(ValueError, requests.get, 'hiwpefhipowhefopw')
    
    def test_HTTPS_200_OK_GET(self):
        r = requests.get('https://baidu.com')
        self.assertEqual(r.status_code, 200)
    
    def test_HTTP_200_OK_HEAD(self):
        r = requests.head('http://baidu.com')
        self.assertEqual(r.status_code, 200)
    
    def test_HTTPS_200_OK_HEAD(self):
        r = requests.head('https://baidu.com')
        self.assertEqual(r.status_code, 200)
    
    def test_HTTP_200_OK_GET_WITH_PARAMS(self):
        heads = {'User-agent': 'Mozilla/5.0'}
        
        r = requests.get('http://www.baidu.com/s', params={'wd': 'test'}, headers=heads)
        self.assertEqual(r.status_code, 200)
    
    def test_HTTP_200_OK_GET_WITH_MIXED_PARAMS(self):
        heads = {'User-agent': 'Mozilla/5.0'}
        
        r = requests.get('http://baidu.com/s?test=true', params={'wd': 'test'}, headers=heads)
        self.assertEqual(r.status_code, 200)
    
    def test_AUTH_HTTPS_200_OK_GET(self):
        auth = (self.user, self.password)
        r = requests.get(self.auth_server.host, auth=auth)
        
        self.assertEqual(r.status_code, 200)
        
        r = requests.get(self.auth_server.host)
        self.assertEqual(r.status_code, 200)
        
        # reset auto authentication
        requests.auth_manager.empty()
    
    def test_POSTBIN_GET_POST_FILES(self):
        bin = requests.post(self.upload_server.host)
        print bin.url
        self.assertEqual(bin.status_code, 200)
        
        post = requests.post(bin.url, data={'some': 'data'})
        self.assertEqual(post.status_code, 200)
        
        post2 = requests.post(bin.url, files={'some': open('test_requests.py')})
        self.assertEqual(post2.status_code, 200)
    
    def test_POSTBIN_GET_POST_FILES_WITH_PARAMS(self):
        bin = requests.post(self.upload_server.host)
        
        self.assertEqual(bin.status_code, 200)
        
        post2 = requests.post(bin.url, files={'some': open('test_requests.py')}, data={'some': 'data'})
        self.assertEqual(post2.status_code, 200)
    
    def test_nonzero_evaluation(self):
        r = requests.get('http://douban.com/some-404-url')
        self.assertEqual(bool(r), False)
        
        r = requests.get('http://baidu.com/')
        self.assertEqual(bool(r), True)
    
    def test_request_ok_set(self):
        r = requests.get('http://douban.com/some-404-url')
        self.assertEqual(r.ok, False)
    
    def test_status_raising(self):
        r = requests.get('http://douban.com/some-404-url')
        self.assertRaises(requests.HTTPError, r.raise_for_status)
        
        r = requests.get('http://baidu.com/')
        self.assertFalse(r.error)
        r.raise_for_status()


if __name__ == '__main__':
    unittest.main()
