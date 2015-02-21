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
This is the main importer of the old data.

This expects two input files:
 1) A Schema. This is a CSV file that specifies all the required attributes we will be converting data to.
 2) Data File. This is the actual CSV file with all the data we'll be converting
'''

import csv
import sqlalchemy
import sqlalchemy.orm

from ColumnFactory import ColumnFactory
from Utils import Utils

class Importer(object):
    #!mwd - These shouldn't be hardcoded
    # But without hardcoding, it's hard
    #  to automate this process
    # Hopefully the schema files are consistent!
    TABLE_NAME = 'table name'
    KEY_FIELD = 'Key Fields'
    COLUMN_NAME = 'sql field name'
    DATATYPE = 'Datatype'
    LENGTH = 'length'
    COLUMN_MAP = 'Worksheet Column'
    
    def __init__(self, db, schema):
        self._db = db
        self._schema = schema

        self._column_mapper = {}

        # go ahead an parse
        self.tables = self._parse_schema()

    def _parse_schema(self):
        '''
        Read the schema and build the required
        sql tables.

        This returns a dictionary of {'tableName': TableKlass},
        where TableKlass is the python object that can be instantiated.
        '''

        
        metadata = sqlalchemy.MetaData(self._db.engine)

        # hold the tables we will return
        tables = {}
        # hold the internal tables we've created,
        #  so we don't to it twice
        sqltables = {}

        f = open(self._schema, 'rb')
        c = csv.DictReader(f)
        
        for row in c:
            # See if this table has been created
            sqltable = sqltables.get(row[Importer.TABLE_NAME], None)
            if sqltable is None:
                # create this table
                sqltable = sqlalchemy.Table(row[Importer.TABLE_NAME], metadata)
                sqltables[row[Importer.TABLE_NAME]] = sqltable

            # We really only care about a few items in the schema:
            # 1) The column name
            # 2) The column data type
            # 3) The length of the data type
            # 4) Whether or not this is a primary key
            col_name = row[Importer.COLUMN_NAME].replace('-', '_')
            primary_key = True if row[Importer.KEY_FIELD] == 'Primary' else False
            col_type = ColumnFactory.build(row[Importer.DATATYPE], row[Importer.LENGTH])

            # Append a new sqlalchemy column with this information on the
            #  associated table
            
            # If this column is a primary key, and the data type is an Integer
            #  then we create a sequence object so that this will correctly
            #  auto increment
            if primary_key and isinstance(col_type, sqlalchemy.Integer):
                sqltable.append_column(sqlalchemy.Column(col_name, col_type, sqlalchemy.Sequence(col_name + "_seq"), primary_key = primary_key))
            else:
                if primary_key:
                    # This is a primary key, but the data type isn't an Integer
                    #  I don't think this is a good idea, but it's what the schema
                    #  called for. Print a warning to let the user know
                    print "Warning: Adding a primary key that isn't an Integer"
                    
                sqltable.append_column(sqlalchemy.Column(col_name, col_type, primary_key = primary_key))

            # The order of columns in the schema does not necessarily match
            #  the order of the columns in the actual data. The schema
            #  actually has a column that specifies its relationship to the data
            # We will store that so when we read in the data, we can map to the correct
            #  column.
            # However, instead of storing a column number, this stores
            #  an Excel style column, i.e. AA instead of 27
            # Convert the Excel style column into a number
            col_id = Utils.Base26ToBase10(row[Importer.COLUMN_MAP])
            # Now store it
            self._column_mapper[col_id] = (row[Importer.DATATYPE], col_name)

        # We have read the whole schema, and have created
        #  all the necessary sqlalchemy tables with their
        #  columns and attributes.
        # However, sqlalchemy requires that we map the
        #  sqlalchemy table definitions to actual Python
        #  classes.
        # Since we don't know what these are ahead of time
        #  we use python's metaprogramming to create
        #  classes on the fly and assign them a constructor
        #  that can handle all the properties.
        for key, value in sqltables.iteritems():
            # Use metaprogramming here to create
            #  a new class with the name of key
            #  that is a subclass of Python's base
            #  object class. Initially, this has
            #  no attributes or methods
            T = type(key, (object,), {})

            # To make this class easier to use,
            #  we create a new constructor for it
            #  that can take any arguments, and assigns
            #  them as attributes. If these argument names
            #  match the sqlalchemy names, they will
            #  be written to the database
            def init(self, **kwargs):
                for k, v in kwargs.iteritems():
                    self.__dict__[k] = v
            T.__init__ = init

            ## The above is metaprogramming that basically generates
            #  the following
            #
            # class TableName(object):
            #    def __init__(self, **kwargs):
            #        for k, v in kwargs.iteritems():
            #            self.__dict__[v] = k
            #

            # We now have to actually map this
            #  so that it will be active, and
            #  so sqlalchemy will be able to
            #  return instances on queries
            sqlalchemy.orm.mapper(T, value)

            # store this class object
            # so we can return it to our caller
            tables[key] = T

        # Have sqlalchemy create all
        #  the necessary sql tables
        metadata.create_all()
            
        return tables
    
    def parse_table_data(self, TableKlass, filename):
        '''
        After we've parsed the schema file,
        we can now parse the actual data.

        This file must be associated with a single table.
        You'll need to pass in a reference to the table class.
        
        This will parse everything, convert formats,
        and insert into the sql database.
        '''
        # parse the datafile
        f = open(filename, 'rb')
        c = csv.reader(f)

        # skip the header, it's frickin useless
        # we are going to use the mappings from
        #  the schema file anyway
        c.next()

        for row in c:
            # It is possible to to create a new
            #  instace of the table, and start
            #  assigning properties. But since
            #  we created that useful constructor
            #  in our metaclass, it's actually
            #  a lot easier to create a dictionary
            #  of all the column:value, and pass
            #  that in to create it in a single shot.
            d = {}
            for i, v in enumerate(row):
                # A lot of things have whitespace,
                #  strip it out
                val = v.strip()
                if len(val) == 0:
                    # This is a blank value. We can't
                    #  actually represent NULL in the CSV
                    #  file, so I'm making the assumption
                    #  that a line of 0 lenght should be
                    #  NULL
                    val = None

                # For some column data types, we can pass
                #  in a string representation and it will
                #  convert correctly (like a number). However
                #  some more advanced formats, specifically
                #  dates, cannot be auto determined.
                # We'll have to manually convert them into
                #  the correct type of object.
                # Fortunately, we kept track of what type
                #  of object everything column is supposed
                #  to be.
                # Get the column type and the matching row
                #  id location
                col_type, col_id = self._column_mapper[i]
                # Convert to the correct format, and store
                #  it based on the column name
                d[col_id] = ColumnFactory.convert(col_type, val)

            # We can now create a new instance
            #  and pass in the dictionary, which
            #  will assign all the columns values.
            t = TableKlass(**d)
            # Add this new object to the session
            #  to prep it for insertion
            self._db.session.add(t)

        # Commit everything. This will
        #  do all the changes at once
        self._db.session.commit()
    
