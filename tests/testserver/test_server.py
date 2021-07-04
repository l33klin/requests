#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: klin
Email: l33klin@foxmail.com
Date: 2021/7/4
Refs: https://gist.github.com/fxsjy/5465353
"""

import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import thread
import base64

key = ""


class AuthHandler(SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    
    def do_HEAD(self):
        # print "send header"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_AUTHHEAD(self):
        # print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        global key
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif self.headers.getheader('Authorization') == 'Basic ' + key:
            SimpleHTTPRequestHandler.do_GET(self)
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass
    

def run_server_with_auth(port=0, user="user", password="password"):
    global key
    key = base64.b64encode("{}:{}".format(user, password))

    server_address = ('', port)       # 0 means random port
    protocol = "HTTP/1.0"
    
    AuthHandler.protocol_version = protocol
    httpd = BaseHTTPServer.HTTPServer(server_address, AuthHandler)

    return httpd


if __name__ == '__main__':
    httpd = run_server_with_auth(0, 'user', '123456')
    sa = httpd.socket.getsockname()
    print "serving on {}:{}".format(sa[0], sa[1])
    t = thread.start_new(httpd.serve_forever, ())
    import time
    for i in range(30):
        time.sleep(1)
        print (30 - i)
    httpd.server_close()

