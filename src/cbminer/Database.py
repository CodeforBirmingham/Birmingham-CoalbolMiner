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
This is a simple class to hold our
basic database information
'''

import sqlalchemy
import sqlalchemy.orm

from ConfigManager import ConfigManager

class Database(object):
    def __init__(self):
        self._dbstring = None
        self._build_database_connection()
        
        if self._dbstring is None:
            raise Exception("Please configure the database first in the cbminer.ini")
        
        # This is a test, this should
        #  come from a configuration
        #self.engine = sqlalchemy.create_engine('sqlite:///test.sqlite3')
        self.engine = sqlalchemy.create_engine(self._dbstring)

        SessionKlass = sqlalchemy.orm.sessionmaker(bind = self.engine)
        self.session = SessionKlass()

    def _build_database_connection(self):
        cm = ConfigManager.get_instance()

        if cm.get_option('Database', 'name') is None or cm.get_option('Database', 'engine') is None:
            raise Exception("Please configure the database first in the cbminer.ini")
        
        dbstring = ''

        dbtype = cm.get_option('Database', 'engine').lower()
        if dbtype == 'sqlite':
            dbstring = "sqlite:///" + cm.get_option('Database', 'name')
        elif dbtype == 'postgres':
            dbstring = "postgresql"
            if cm.get_option('Database', 'driver'):
                if cm.get_option('Databse', 'driver').lower() == 'pg8000':
                    dbstring += "+pg8000://"
                else:
                    dbstring += "://"
            else:
                dbstring += "://"
                
            if cm.get_option('Database', 'username'):
                dbstring += cm.get_option('Database', 'username')
                if cm.get_option('Database', 'password'):
                    dbstring += ':' + cm.get_option('Database', 'password')
                dbstring += '@'

            if cm.get_option('Database', 'host'):
                dbstring += cm.get_option('Database', 'host') + '/'
            else:
                dbstring += 'localhost' + '/'

            dbstring += cm.get_option('Database', 'name')
                    
        elif dbtype == 'mysql':
            dbstring = "mysql"
            if cm.get_option('Database', 'driver'):
                if cm.get_option('Database', 'driver').lower() == 'connector':
                    dbstring += "+mysqlconnector://"
                elif cm.get_option('Database', 'driver') == 'oursql':
                    dbstring += '+oursql://'
                else:
                    dbstring += "://"
            else:
                dbstring += "://"
                
            if cm.get_option('Database', 'username'):
                dbstring += cm.get_option('Database', 'username')
                if cm.get_option('Database', 'password'):
                    dbstring += ':' + cm.get_option('Database', 'password')
                dbstring += '@'

            if cm.get_option('Database', 'host'):
                dbstring += cm.get_option('Database', 'host') + '/'
            else:
                dbstring += 'localhost' + '/'

            dbstring += cm.get_option('Database', 'name')
        elif dbtype == 'mssql':
            dbstring = "mssql"
            if cm.get_option('Database', 'driver'):
                if cm.get_option('Database', 'driver').lower() == 'pymssql':
                    dbstring += "+pymssql://"
                else:
                    dbstring += "+pyodbc://"
            else:
                dbstring += "+pyodbc://"
                
            if cm.get_option('Database', 'username'):
                dbstring += cm.get_option('Database', 'username')
                if cm.get_option('Database', 'password'):
                    dbstring += ':' + cm.get_option('Database', 'password')
                dbstring += '@'

            if cm.get_option('Database', 'host'):
                dbstring += cm.get_option('Database', 'host')
                if cm.get_option('Database', 'port'):
                    dbstring += ':' + cm.get_option('Database', 'port')
                dbstring += '/'

            dbstring += cm.get_option('Database', 'name')

        elif dbtype == 'oracle':
            dbstring = 'oracle'
            if cm.get_option('Database', 'driver'):
                if cm.get_option('Database', 'driver').lower() == 'cx':
                    dbstring += '+cx_oracle://'
                else:
                    dbstring += '://'
            else:
                dbstring += '://'

            if cm.get_option('Database', 'username'):
                dbstring += cm.get_option('Database', 'username')
                if cm.get_option('Database', 'password'):
                    dbstring += ':' + cm.get_option('Database', 'password')
                dbstring += '@'

            if cm.get_option('Database', 'host'):
                dbstring += cm.get_option('Database', 'host')
                if cm.get_option('Database', 'dbport'):
                    dbstring += ':' + cm.get_option('Database', 'port')
                dbstring += '/'


            dbstring += cm.get_option('Database', 'name')

        self._dbstring = dbstring
