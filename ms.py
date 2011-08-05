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
        log_handle = open('../r/log', 'a')
        log_handle.write(message + '\n')
    finally:
        log_handle.close()

form = cgi.FieldStorage()

if 'id' not in form or 'file' not in form:
    content = '<form enctype="multipart/form-data" method="post"><input type="text" name="id"><input type="file" name="file"><input type="submit"></form>'
else:
    # A nested FieldStorage instance holds the file
    fileitem = form['file']
    identitem = form['id']

    if identitem.value and fileitem.filename:
        ppath = ptree.id2ptree(identitem.value)
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
        log(datetime.now().isoformat() + ' POST ' + identitem.value + ' ' + name)
        content = '<p>The file "' + name + '" was uploaded successfully</p>'
    else:
        content = '<p>No file was uploaded</p>'
   
print """\
Content-Type: text/html\n
<!doctype html>
<html>
<head><title>up</title></head>
<body>
%s
</body>
</html>
""" % content
