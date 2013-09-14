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
import libthing

import cgitb; cgitb.enable()    # XXX for debugging

def main():
    # Send http headers
    print "Content-Type: text/plain"
    print

    # Process the form data
    form = cgi.FieldStorage()

    latex = True
    #latex = form["generate_latex"] # FIXME how can we dump two files? (.bib and .tex)

    fileitem = form["lt_file"]
    if fileitem.filename:
        # strip leading path from file name to avoid directory traversal attacks
        timestamp = str(datetime.datetime.utcnow()).replace(" ", "_")
        #fn = os.path.basename(fileitem.filename) + "_" + timestamp
        fn = "LibraryThing_" + timestamp + ".xls"
        input_file = os.path.join('uploads', fn)
        open('uploads/' + fn, 'wb').write(fileitem.file.read())
        bookdata = codecs.open(input_file, 'rb', 'utf-16')
        lines = bookdata.readlines()
        bibtex_file = file(os.path.join("uploads", "LibraryThing_" + timestamp + ".bib"), 'w')
    else:
        print "Error: File isn't valid."
        return

    #bibtex_file = file("LibraryThing.bib", 'w')
    latex_file = file(os.path.join("uploads", "LibraryThing_" + timestamp + ".tex"), 'w')
    latex_file.write("""\\documentclass{article}
\\usepackage{apacite}
\\usepackage{ucs}  % unicode support
\\title{Test of the \\texttt{LibraryThing.bib} file}
\\begin{document}
\\begin{itemize}
""")
        latex_file.write("""
\\end{itemize}
\n\n
\\bibliographystyle{apacite}
\\bibliography{LibraryThing}
\\end{document}
""")
    latex_file.close()

    bib_dict = lt2bib.ltcsv_to_dictdata(bookdata, false)
    lt2bib.writeBibTex(bib_dict, 'LibThing.bib')
    #if latex:
    #    lt2bib.writeLaTex(bib_dict)
    #else:
    #    lt2bib.writeBibTex(bib_dict, 'LibThing.bib')


if __name__ == "__main__":
    main()

