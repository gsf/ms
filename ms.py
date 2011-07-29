#!/usr/bin/python

import cgitb
cgitb.enable()

import cgi
import os
import simplejson as json

#print json.dumps({'Hello': 'world!'})
#for param in os.environ.keys():
#    print '%20s: %s' % (param, os.environ[param])
#print '\n' + os.environ['REQUEST_METHOD']

form = cgi.FieldStorage()

if 'file' in form:
    # Generator to buffer file chunks
    # from http://webpython.codepoint.net/cgi_big_file_upload
    def fbuffer(f, chunk_size=10000):
       while True:
          chunk = f.read(chunk_size)
          if not chunk: break
          yield chunk
          
    # A nested FieldStorage instance holds the file
    fileitem = form['file']

    # Test if the file was uploaded
    if fileitem.filename:

       # strip leading path from file name to avoid directory traversal attacks
       fn = os.path.basename(fileitem.filename)
       f = open('files/' + fn, 'wb', 10000)

       # Read the file in chunks
       for chunk in fbuffer(fileitem.file):
          f.write(chunk)
       f.close()
       content = '<p>The file "' + fn + '" was uploaded successfully</p>'
    else:
       content = '<p>No file was uploaded</p>'
else:
    content = '<form enctype="multipart/form-data" method="post"><input type="file" name="file"><input type="submit"></form>'
   
print """\
Content-Type: text/html\n
<!doctype html>
<html>
<head><title>up</title></head>
<body>
%s
</body>
</html>
""" % (content,)
