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
dbengine = postgres
dbhost = localhost
dbname = cbminer
dbdriver = psycopg2
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

        if not self._cp.has_section('CBMiner'):
            self._cp.add_section('CBMiner')

        try:
            self._cp.read('cbminer.ini')
        except Exception, e:
            print 'exception', e
            pass

        self._loaded = True
        
    def save(self):
        with open('cbminer.ini', 'w') as f:
            self._cp.write(f)

    def __getattr__(self, name):
        cp = self.__dict__.get('_cp')
        if cp:
            if cp.has_option('CBMiner', name):
                return cp.get('CBMiner', name)

        raise AttributeError("No attribute: " + name)

    def __setattr__(self, name, value):
        cp = self.__dict__.get('_cp')
        if cp:
            return cp.set('CBMiner', name, value)

        return object.__setattr__(self, name, value)
            
    def __init__(self):
        self._loaded = False
        self._cp = None

