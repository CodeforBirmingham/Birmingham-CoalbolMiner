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
Handle our web requests
'''

import SimpleHTTPServer
import urlparse
import json
import cgi

import src.cbminer as cbminer

# internal exceptions
class BadRequestException(Exception):
    pass
class UnAuthorizedException(Exception):
    pass
class ForbiddenException(Exception):
    pass
class NotFoundException(Exception):
    pass
class MethodNotAllowedException(Exception):
    pass

class Router(object):
    '''This holds all our routes'''
    METHOD_TYPE_POST = 0
    METHOD_TYPE_GET = 1
    HANDLERS = {}

'''
This is a decorator to setup routes
'''
class route:
    def __init__(self, path, method = Router.METHOD_TYPE_POST):
        self.path = path
        self.method = method
        
    def __call__(self, f):
        if self.path not in Router.HANDLERS:
            Router.HANDLERS[self.path] = {}
            Router.HANDLERS[self.path][self.method] = f
            return f

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urlparse.urlparse(self.path)
        path = p.path
        params = urlparse.parse_qs(p.query)
        for k, v in params.iteritems():
            if len(v) == 1:
                params[k] = v[0]
                
        resp = self._run(path, Router.METHOD_TYPE_GET, **params)
                                                        
        self.send_response(200)
        if 'headers' in resp:
            for k, v in resp['headers'].iteritems():
                self.send_header(k, v)
        self.end_headers()

        self.wfile.write(resp['body'])

    def do_POST(self):
        kwargs = {}

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        # we can either handle json directly in the body
        #  or we can take a form that has a single key
        #  called data, where the value is a json
        #  encoded dictionary
        if ctype == 'application/json':
            length = int(self.headers.getheader('content-length'))
            # read the body
            data = self.rfile.read(length)
            # convert to json
            kwargs = json.loads(data)
        elif ctype == 'application/x-www-form-urlencoded':       
            form = cgi.FieldStorage(
                fp = self.rfile,
                headers = self.headers,
                environ = {'REQUEST_METHOD': 'POST',
                           'CONTENT_TYPE': self.headers['Content-Type']}
            )


            # convert the form into a dictionary
            if 'data' in form:
                kwargs = json.loads(form.getvalue('data'))
                if not isinstance(kwargs, dict):
                    kwargs = {}
        else:
            raise BadRequestException("Invalid content type: %s" % ctype)

        resp = self._run(self.path, Router.METHOD_TYPE_POST, **kwargs)
                                                        
        self.send_response(200)
        if 'headers' in resp:
            for k, v in resp['headers'].iteritems():
                self.send_header(k, v)
        self.end_headers()

        self.wfile.write(resp['body'])


    def _run(self, path, method, *args, **kwargs):
        try:
            if path in Router.HANDLERS:
                if method in Router.HANDLERS[path]:
                    return Router.HANDLERS[path][method](self, *args, **kwargs)
                else:
                    raise MethodNotAllowedException()
            else:
                # 404
                raise NotFoundException()
        except BadRequestException, e:
            self.send_error(400, 'Bad Request to %s: %s' % (self.path, e))
        except UnAuthorizedException, e:
            self.send_error(401, 'Unauthroized Access to %s: %s' % (self.path, e))
        except ForbiddenException, e:
            self.send_error(403, 'Forbidden to Access to %s: %s' % (self.path, e))
        except NotFoundException, e:
            self.send_error(404, 'File not found: %s' % self.path)
        except MethodNotAllowedException, e:
            self.send_error(405, 'Metthod Not Allowed to %s: %s' % (self.path, e))
        except Exception, e:
            print 'Unhandled exception', e
            self.send_error(400, 'Bad Request to %s: %s' % (self.path, e))
            
    @route('/', Router.METHOD_TYPE_GET)
    def index(self):
        body = ''
        try:
            f = open('data/server/templates/index.tmpl.html')
            body = f.read()
            f.close()
        except Exception, e:
            print 'exception', e
            pass
        
        return {'headers': {'Content-type:': 'text/html'},
                'body': body}

    @route('/config/database')
    def update_database(self, dbtype, location, port = None, username = None, password = None):
        print 'update_database', dbtype, location, port, username, password
        
        cm = cbminer.ConfigManager.get_instance()
        cm.load()
        
        dbstring = ''
        
        if dbtype.lower() == 'sqlite':
            dbstring = "sqlite:///" + location
        else:
            raise Exception('unknown db type')

        cm.dbstring = dbstring

        cm.save()

        return {'headers': {'Content-type:': 'application/json'},
                'body': json.dumps({'result': 0})}
        
