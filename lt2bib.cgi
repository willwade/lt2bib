#!/usr/bin/env python
# vim:shiftwidth=4:tabstop=4:expandtab:filetype=python

# Author:
#   Kevin Godby <godbyk@gmail.com>
#
# License:
#   Public domain.

"""
lt2bib.py is a script that parses the files exported by LibraryThing and
generates a BiBTeX file with the same information.

Usage: lt2bib.py <tab-delimited-file>

The <tab-delimited-file> is exported from LibraryThing.
"""

import sys, codecs, re, os
import datetime
import cgi
import libthing as lt2bib

import cgitb; cgitb.enable()    # XXX for debugging

def main():
    # Send http headers
    print "Content-Type: text/plain"

    # Process the form data
    form = cgi.FieldStorage()

    fileitem = form["lt_file"]
    print fileitem
    exit()
    
    if fileitem.filename:
        # strip leading path from file name to avoid directory traversal attacks
        timestamp = str(datetime.datetime.utcnow()).replace(" ", "_")
        #fn = os.path.basename(fileitem.filename) + "_" + timestamp
        fn = "LibraryThing_" + timestamp + ".xls"
        input_file = os.path.join('uploads', fn)
        open('uploads/' + fn, 'wb').write(fileitem.file.read())
        bookdata = codecs.open(input_file, 'rb', 'utf-16')
        bibtex_file = os.path.join("uploads", "LibraryThing_" + timestamp + ".bib")
        bib_dict = lt2bib.ltcsv_to_dictdata(bookdata, false)
        lt2bib.writeBibTex(bib_dict, bibtex_file)
    else:
        print "Error: File isn't valid."
        return

if __name__ == "__main__":
    main()

