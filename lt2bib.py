#!/usr/bin/python
# vim:shiftwidth=4:tabstop=4:expandtab:filetype=python

# Author:
#   Kevin Godby <godbyk@gmail.com>
#
# License:
#   Public domain.

"""
lt2bib.py is a script that parses the files exported by LibraryThing and
generates a BiBTeX file with the same information.

Usage: lt2bib.py [-hv (-w |--worldcatlookup) (-o FILE | --outputbib FILE)] [-l FILE | -u USER -p PASS]
       lt2bib.py -h | --help
       lt2bib.py -v | --version

Options:
        -l FILE, --libthingcsv=FILE  LibraryThing exported Tab-delimited CSV
        -u USER, --user=USER         Librarything Username
        -p PASS, --pass=PASS         Librarything Password
        -w, --worldcatlookup         Use worldcat to lookup and fill-in sparse LT data?
        -o FILE, --outputbib=FILE    Path/Name of the output file (default: LibThing.bib)
        -h, --help                   This help
        -v, --version                Show version info
"""
try:
    from docopt import docopt
except ImportError:
    exit('This example requires that `docopt` library'
         ' is installed: \n    pip install docopt\n'
         'https://github.com/docopt/docopt')

import libthing as lt2bib
import sys, os, codecs

# ==================== MAIN LOOP =========================================

if __name__ == '__main__':
    arguments = docopt(__doc__, version='lt2bib v1')
    
    # Open the bookdata.csv file
    """
    NB: Can now do a download of the data instead if thats useful
    """
    #lt2bib.downloadLTCSV('user','pass')
    if (arguments['--libthingcsv']):
        if os.path.isfile(arguments['--libthingcsv']): 
            try: 
                open(arguments['--libthingcsv'])
                bookdata = codecs.open(arguments['--libthingcsv'], 'rb', 'utf-16')
            except IOError:
                exit('Sorry.'+arguments['--libthingcsv']+' cannot be found')
    elif (arguments['--user'] and arguments['--pass']):    
        if (lt2bib.downloadLTCSV(arguments['--user'], arguments['--pass'],
                            path='LibThing.csv')):
            bookdata = codecs.open('LibThing.csv', 'rb', 'utf-16')
        else:
            exit('Sorry. We couldn\'t login with those details')
    else:
        exit('You need to provide either a CSV file or a user/pass')
            
    # False/True if you want to fill in missing info from Worldcat
    bib_dict = lt2bib.ltcsv_to_dictdata(bookdata, arguments['--worldcatlookup'])
    lt2bib.writeBibTex(bib_dict, 'LibThing.bib')

    """
    Just not sure about LaTex! Sorry!
    """
    #if latex:
    #    lt2bib.writeLaTex(bib_dict)
    #else:
    #    lt2bib.writeBibTex(bib_dict, 'LibThing.bib')
