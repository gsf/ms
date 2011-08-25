#!/usr/bin/python

import cgitb
cgitb.enable()

import cgi
from datetime import datetime
import os
import ptree
import simplejson as json


#print json.dumps({'Hello': 'world!'})
#for param in os.environ.keys():
#    print '%20s: %s' % (param, os.environ[param])
#print '\n' + os.environ['REQUEST_METHOD']

# Generator to buffer file chunks
# from http://webpython.codepoint.net/cgi_big_file_upload
def fbuffer(f, chunk_size=10000):
    while True:
        chunk = f.read(chunk_size)
        if not chunk: break
        yield chunk

def log(message):
    try:
        log_handle = open('../log', 'a')
        log_handle.write(message + '\n')
    finally:
        log_handle.close()

def html_response(content):
    return """\
Content-Type: text/html\n
<!doctype html>
<html>
  <head><title>up</title></head>
  <body>%s</body>
</html>
""" % content

def get_response():
    accept_formats = os.environ['HTTP_ACCEPT'].split(',')
    form = cgi.FieldStorage()
    #print 'Content-Type: text/plain\n'
    #print form
    #print 'Content-Type: text/html\n'
    #cgi.print_environ()

    #if os.environ['REQUEST_METHOD'] == 'GET':
            
    if os.environ['REQUEST_METHOD'] == 'POST':
        if 'id' in form and 'file' in form:
            identity = form['id'].value
            # A nested FieldStorage instance holds the file
            fileitem = form['file']

            if identity and fileitem.filename:
                ppath = ptree.id2ptree(identity)
                home = '../r%s' % ppath
                try:
                    os.makedirs(home)
                except OSError:
                    pass
                # strip leading path from file name to avoid directory traversal attacks
                name = os.path.basename(fileitem.filename)
                f = open('../r%s%s' % (ppath, name), 'wb', 10000)

                # Read the file in chunks
                for chunk in fbuffer(fileitem.file):
                   f.write(chunk)
                f.close()
                log(datetime.now().isoformat() + ' POST ' + identity + ' ' + name)
                message = "The file %s was uploaded successfully" % name
                if 'text/html' in accept_formats:
                    return html_response('<p>%s</p>' % message)
                else:
                    return 'Content-Type: text/plain\n\n%s' % message

    if os.environ['REQUEST_METHOD'] == 'DELETE':
        if 'id' in form and 'filename' in form:
            identity = form['id'].value
            filename = form['filename'].value
            if identity and filename:
                ppath = ptree.id2ptree(identity)
                dir = '../r%s' % ppath
                name = os.path.basename(filename)
                os.remove(dir + name)
                try:
                    os.removedirs(dir) # remove parent directories if empty
                except OSError:
                    pass
                log(datetime.now().isoformat() + ' DELETE ' + identity + ' ' + name)
                message = "The file %s was deleted successfully" % name
                if 'text/html' in accept_formats:
                    return html_response('<p></p>')
                else:
                    return 'Content-Type: text/plain\n\n%s' % message
                

    if 'text/html' in accept_formats:
        return html_response("""
<form enctype="multipart/form-data" method="post">
  <input type="text" name="id">
  <input type="file" name="file">
  <input type="submit">
</form>""")
    else:
        return 'Content-Type: text/plain\n\ndata.free103point9.org'
   
print get_response()
