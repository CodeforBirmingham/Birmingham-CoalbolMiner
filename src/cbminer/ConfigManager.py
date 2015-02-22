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

'''
Same config file:

[CBMiner]
option = 1
[Database]
engine = postgres
host = localhost
name = cbminer
driver = psycopg2
'''
class ConfigManager(object):
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ConfigManager()
            cls._instance._load()
            
        return cls._instance

    def reload(self):
        _loaded = False

        self._load()
    
    def _load(self):
        if self._loaded:
            return
        
        self._cp = ConfigParser.ConfigParser()

        try:
            self._cp.read('cbminer.ini')
        except Exception, e:
            print 'exception', e
            pass

        self._loaded = True

    def save(self):
        with open('cbminer.ini', 'w') as f:
            self._cp.write(f)

    def clear_section(self, section):
        self._cp.remove_section(section)
        
    def get_options(self, section):
        print 'get options'
        self._load()
        print 'after load'

        options = {}
        print self._cp.items(section)
        for i in self._cp.items(section):
            print 'i=', i
            options[i[0]] = i[1]

        return options

    def set_option(self, section, name, value):
        if self._cp.has_section(section) == False:
            self._cp.add_section(section)

        self._cp.set(section, name, value)

    def get_option(self, section, name):
        if self._cp.has_option(section, name):
            return self._cp.get(section, name)
        return None
                
    def __init__(self):
        self._loaded = False
        self._cp = None

