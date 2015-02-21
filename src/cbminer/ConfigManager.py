'''
The MIT License (MIT)

Copyright (c) 2015 @ CodeForBirmingham (http://codeforbirmingham.org)
@Author: Marcus Dillavou <marcus.dillavou@codeforbirmingham.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

'''
This is a simple class for managing our
configuration
'''

import ConfigParser

class ConfigManager(object):
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ConfigManager()
            
        return cls._instance

    def load(self):
        cp = ConfigParser.ConfigParser()

        try:
            cp.read('cbminer.ini')
        except Exception, e:
            print 'exception', e
            pass

        print cp.sections()
        print cp.has_section("database")
        
        if cp.has_option("database", "connection_string"):
            print 'has option'
            self.dbstring = cp.get("database", "connection_string")
        print 'dbstring=', self.dbstring
        
    def save(self):
        cp = ConfigParser.ConfigParser()
        cp.add_section("database")
            
        if self.dbstring:
            cp.set("database", "connection_string", self.dbstring)

        with open('cbminer.ini', 'w') as f:
            cp.write(f)
            
    def __init__(self):
        self.dbstring = None

