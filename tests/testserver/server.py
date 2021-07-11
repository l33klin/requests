#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Authors: klin
Email: l33klin@foxmail.com
Date: 2021/7/11
"""
import thread

from auth_server import auth_server_d
from upload_server import upload_server_d


class TestServer(object):

    def __init__(self, httpd):
        self.httpd = httpd
        self.thread = None
        self.host = None
    
    def run_background(self):
        sa = self.httpd.socket.getsockname()
        self.host = "http://localhost:{}".format(sa[1])
        self.thread = thread.start_new(self.httpd.serve_forever, ())
    
    def close(self):
        self.httpd.shutdown()
    

class AuthServer(TestServer):
    
    def __init__(self, auth=None):
        httpd = auth_server_d(user=auth[0], password=auth[1])
        super(AuthServer, self).__init__(httpd)


class UploadServer(TestServer):
    
    def __init__(self):
        httpd = upload_server_d()
        super(UploadServer, self).__init__(httpd)
    

def get_server(_type, **kwargs):
    
    servers = {
        "auth": AuthServer,
        "upload": UploadServer
    }
    
    return servers[_type](**kwargs)


if __name__ == '__main__':
    pass