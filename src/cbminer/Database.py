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

        if not hasattr(cm, 'dbname'):
            raise Exception("Please configure the database first in the cbminer.ini")
        
        dbstring = ''

        dbtype = cm.dbengine.lower()
        if dbtype == 'sqlite':
            dbstring = "sqlite:///" + cm.dbname
        elif dbtype == 'postgres':
            dbstring = "postgresql"
            if hasattr(cm, 'dbdriver'):
                if cm.dbdriver.lower() == 'pg8000':
                    dbstring += "+pg8000://"
                else:
                    dbstring += "://"
            else:
                dbstring += "://"
                
            if hasattr(cm, 'dbusername'):
                dbstring += cm.dbusername
                if hasattr(cm, 'dbpassword'):
                    dbstring += ':' + cm.dbpassword
                dbstring += '@'

            if hasattr(cm, 'dbhost'):
                dbstring += cm.dbhost + '/'
            else:
                dbstring += 'localhost' + '/'

            dbstring += cm.dbname
                    
        elif dbtype == 'mysql':
            dbstring = "mysql"
            if hasattr(cm, 'dbdriver'):
                if cm.dbdriver.lower() == 'connector':
                    dbstring += "+mysqlconnector://"
                elif cm.dbdriver.lower() == 'oursql':
                    dbstring += '+oursql://'
                else:
                    dbstring += "://"
            else:
                dbstring += "://"
                
            if hasattr(cm, 'dbusername'):
                dbstring += cm.dbusername
                if hasattr(cm, 'dbpassword'):
                    dbstring += ':' + cm.dbpassword
                dbstring += '@'

            if hasattr(cm, 'dbhost'):
                dbstring += cm.dbhost + '/'
            else:
                dbstring += 'localhost' + '/'

            dbstring += cm.dbname
        elif dbtype == 'mssql':
            dbstring = "mssql"
            if hasattr(cm, 'dbdriver'):
                if cm.dbdriver.lower() == 'pymssql':
                    dbstring += "+pymssql://"
                else:
                    dbstring += "+pyodbc://"
            else:
                dbstring += "+pyodbc://"
                
            if hasattr(cm, 'dbusername'):
                dbstring += cm.dbusername
                if hasattr(cm, 'dbpassword'):
                    dbstring += ':' + cm.dbpassword
                dbstring += '@'

            if hasattr(cm, 'dbhost'):
                dbstring += cm.dbhost
                if hasattr(cm, 'dbport'):
                    dbstring += ':' + cm.dbport
                dbstring += '/'

            dbstring += cm.dbname

        elif dbtype == 'oracle':
            dbstring = 'oracle'
            if hasattr(cm, 'dbdriver'):
                if cm.dbdriver.lower() == 'cx':
                    dbstring += '+cx_oracle://'
                else:
                    dbstring += '://'
            else:
                dbstring += '://'

            if hasattr(cm, 'dbusername'):
                dbstring += cm.dbusername
                if hasattr(cm, 'dbpassword'):
                    dbstring += ':' + cm.dbpassword
                dbstring += '@'

            if hasattr(cm, 'dbhost'):
                dbstring += cm.dbhost
                if hasattr(cm, 'dbport'):
                    dbstring += ':' + cm.dbport
                dbstring += '/'


            dbstring += cm.dbname

        self._dbstring = dbstring
