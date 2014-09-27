#!/usr/bin/env python
import web
urls = ('/','root')
app = web.application(urls,globals())
 
class root:
 
    def __init__(self):
        self.hello = "hello world"
 
    def GET(self):
        return self.hello
 
if __name__ == "__main__":
        app.run()