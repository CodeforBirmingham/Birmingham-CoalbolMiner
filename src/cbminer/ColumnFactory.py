import datetime

import sqlalchemy

class ColumnFactoryException(Exception):
    pass

class ColumnFactory(object):
    @classmethod
    def build(cls, column_type, length):
        c = column_type.lower()
        
        if c == 'alphanumeric':
            return cls._build_string(length)
        elif c == 'money':
            return cls._build_money(length)
        elif c == 'numeric':
            return cls._build_numeric(length)
        elif c == 'percentage':
            return cls._build_percentage(length)
        elif c == 'date':
            return cls._build_date(length)
        else:
            print 'Unknown column type', column_type
            raise ColumnFactoryException("Unknown column tpe")

    @classmethod
    def convert(cls, column_type, value):
        if value is None:
            return None # can't convert this
        
        c = column_type.lower()

        try:
            if c == 'alphanumeric':
                return value
            elif c == 'money':
                try:
                    return float(value)
                except Exception, e:
                    raise ColumnFactoryException("Invalid value for money type: %s" % e)
            elif c == 'numeric':
                try:
                    # try an int first
                    return int(value)
                except ValueError, e:
                    try:
                        # try a float
                        return float(value)
                    except ValueError, e:
                        raise
                except Exception, e:
                    raise ColumnFactoryException("Invalid value for numeric type: %s" % e)
            elif c == 'percentage':
                try:
                    return float(value)
                except Exception, e:
                    raise ColumnFactoryException("Invalid value for percentage type: %s" % e)
            elif c == 'date':
                # ok, so it looks like dates are in the format of
                #  MDDYY or MMDDYY
                try:
                    return datetime.datetime.strptime(value, '%m%d%y').date()
                except Exception, e:
                    return None
            else:
                print 'Unknown column type', column_type
                raise ColumnFactoryException("Unknown column type")
        except Exception, e:
            print 'Error converting type:', value, e
            return value
        
    @classmethod
    def _build_string(cls, length):
        try:
            length = int(length)
            return sqlalchemy.String(length)
        except Exception, e:
            raise ColumnFactoryException("Invalid length: " + e)

    @classmethod
    def _build_money(cls, length):
        # just use a precision of 2
        return sqlalchemy.Numeric(2)

    @classmethod
    def _build_numeric(cls, length):
        try:
            length = int(length)
        except ValueError, e:
            try:
                length = float(length)

            except ValueError, e:
                raise ColumnFactoryException("Invalid length: " + e)

        return sqlalchemy.Float(length)

    @classmethod
    def _build_percentage(cls, length):
        return sqlalchemy.Float(2)

    @classmethod
    def _build_date(cls, length):
        return sqlalchemy.Date()
