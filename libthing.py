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

Usage: lt2bib.py <tab-delimited-file>

The <tab-delimited-file> is exported from LibraryThing.

"""

import re, urllib2

try:
    import utf8tobibtex as utbib
except ImportError:
    exit('This script requires that `utf8tobibtex` library'
         ' is installed: \n    pip install utf8tobibtex\n'
         'https://pypi.python.org/pypi/utf8tobibtex')


def downloadLTCSV(user='', passw='', path='LibThing.csv'):
    """
    Will make use of requests instead of mechanize. More future proof
    NB: little error checking for user/pass at present
    """
    try:
        import requests
    except ImportError:
        exit('This script needs requests')

    # Fill in your details here to be posted to the login form.
    payload = {
        'formusername': user,
        'formpassword': passw,
        'index_signin_already':'Sign+in'
    }

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        r = s.post('https://www.librarything.com/enter/start', data=payload)
        if 'LTUnifiedCookie' in r.cookies:
            if r.cookies['LTUnifiedCookie'] == '%7B%22areyouhuman%22%3A1%7D':
                #You aren't logged int
                return False

        # An authorised request.
        r = s.get('http://www.librarything.com/export-tab', stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return True


def getDictfromISBN(isbn,needItems):
    """ Sometimes the data in LibraryThing is a bit sparse. 
    This fills it out with more info. Uses worldcat. Mileage may vary. Slight concerned this may break if too many calls are made to WorldCat"""
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    from StringIO import StringIO as StringIO
    xml = urllib2.urlopen('http://xisbn.worldcat.org/webservices/xid/isbn/'+isbn+'?method=getMetadata&format=xml&fl=year,ed,title,author,publisher,city').read()
    tree = ET.parse(StringIO(xml))
    doc = tree.getroot()
    if doc.attrib['stat'] == 'ok':
        items = doc[0].attrib
        if 'ed' in items:
            items['edition'] = items.pop('ed')
        for item, value in items.iteritems():
            if item in needItems:
                items[item] = utbib.utf8_to_bibtex(value)
        return items
    else:
        # wasn't a valid ISBN
        return None

def formatBibTexLine(k, v):
    """
    Formats the BibTex line with the name of the key and value 
          - easier than writing if/else statements. 
    NB: For books, author/editor, publisher, title,  year are all a must
    """
    if v != '' or ( k =='author' or k == 'title' or k == 'publisher' or k == 'year'):
        return "\t%s = {%s},\n" % (k, v)
    else:
        return ''

def writeBibTex(dictdata, bibfile="LibraryThing.bib"):
    """
    Writes out the BibTex file when provided with a dictionary of keys, values
    """
    bibtex_file = file(bibfile, 'w')
    for n in dictdata:
        bibentry = '\n@book{%s,\n' % n
        for k in dictdata[n]:
            bibentry = bibentry + formatBibTexLine(k, dictdata[n][k])
        bibentry = bibentry +"\n}"

        bibtex_file.write(bibentry)

def writeLaTex(dictdata, texfile="LibraryThing.tex"):
    """
    Writes out latex. NB: Not tested. 
    """
    bibtex_file = file(texfile, 'w')
    for n in dictdata:
        latex_file.write("""\\documentclass{article}
\\usepackage{apacite}
\\usepackage{ucs}  % unicode support
\\title{Test of the \\texttt{LibraryThing.bib} file}
\\begin{document}
\\begin{itemize}
""")
        latex_file.write("\\item %s \\cite{%s}\n" % (title, key))
        latex_file.write("""
\\end{itemize}
\n\n
\\bibliographystyle{apacite}
\\bibliography{LibraryThing}
\\end{document}
""")
    latex_file.close()

def cleankey(s):
    """
    Strips accents and special chars, leaving only A-Z, a-z, and 0-9
    """
    pattern = re.compile('[\W_]+', re.UNICODE)
    return pattern.sub('', s)

def valid_key(bib_dict, key):
    """
     if the bib_dict is empty, return the key
    """
    if bib_dict.keys() == []:
        return key

    # add all similar keys to the existing_keys list
    existing_keys = []
    for k in bib_dict.keys():
        if k is None:
            continue

        if k.lower().startswith(key.lower()):
            existing_keys.append(k)

    # find the latest key appendix
    max_postfix = ''
    for k in existing_keys:
        key_parts = re.split(r'[0-9]+', k)
        if len(key_parts[-1]) > len(max_postfix):
            max_postfix = key_parts[-1]
        elif len(key_parts[-1]) == len(max_postfix):
            if key_parts > max_postfix:
                max_postfix = key_parts[-1]

    # generate new key with incremented postfix
    key = key + nextpostfix(max_postfix)

    return key

def nextpostfix(x):
    """
    Returns the next alpha postfix in the sequence.
    """
    if x == '':
        return 'a'

    if ord(x[-1]) < ord('z'):
        x = x[0:-1] + chr(ord(x[-1])+1)
    else:
        if x[0] == 'z':
            x = 'a' + 'a' * len(x)
        else:
            x = chr(ord(x[0])+1) + x[1:]
            x = x[0:-1] + 'a'
    return x

def parseEdition(x):
    """
    Takes an integer and returns a ordinal word. 
    Amazing there isn't a simpler way of doing this
    """
    ordinal_dict = { 1 : 'First',  2 : 'Second',  3 : 'Third',
                    4 : 'Fourth',  5 : 'Fifth',  6 : 'Sixth',
                    7 : 'Seventh',  8 : 'Eighth',  9 : 'Ninth',
                   10 : 'Tenth',  11 : 'Eleventh',  12 : 'Twelfth',
                   13 : 'Thirteenth',  14 : 'Fourteenth',  15 : 'Fifteenth',
                   16 : 'Sixteenth',  17 : 'Seventeenth',  18 : 'Eighteenth',
                   19 : 'Nineteenth',  20 : 'Twentieth',  21 : 'Twenty-first',
                   22 : 'Twenty-second',  23 : 'Twenty-third',  24 : 'Twenty-fourth',
                   25 : 'Twenty-fifth',  26 : 'Twenty-sixth',  27 : 'Twenty-seventh',
                   28 : 'Twenty-eighth',  29 : 'Twenty-ninth',  30 : 'Thirtieth',
                   31 : 'Thirty-first',  32 : 'Thirty-second',  100 : 'Hundredth',
                   101 : 'Hundred and first',  112 : 'Hundred and twelfth',
                   1000 : 'Thousandth ',
    }

    if int(x) in ordinal_dict:
        return ordinal_dict[int(x)]
    else:
        print "didn't find ordinal:", x
        return x


def getauthorslist(author_fl, other_authors):
    """
    Get the list of authors
    """
    if other_authors == '':
        return author_fl
    else:
        authors_list = [author_fl]
        authors_list.extend(other_authors.split(", "))
        return " and ".join(authors_list)

def ltcsv_to_dictdata(csvdata, expandWCdata=False):
    lines = csvdata.readlines()
    bib_dict = { }
    linenum = -1
    for l in lines:
        linenum = linenum + 1
        if 0 == linenum:
            continue

        line = l.split('\t')

        book_id       = line[0]  # book id
        title         = utbib.utf8_to_bibtex(line[1])  # title
        author_fl     = utbib.utf8_to_bibtex(line[2])  # author, first-last
        author_lf     = utbib.utf8_to_bibtex(line[3])  # author, last-first
        other_authors = utbib.utf8_to_bibtex(line[4])  # other authers
        publication   = utbib.utf8_to_bibtex(line[5])  # publication
        date          = line[6]  # date
        isbn          = line[7]  # ISBN
        series        = line[8]  # series
        source        = line[9]  # source
        lang1         = line[10] # language 1
        lang2         = line[11] # language 2
        lang_orig     = line[12] # original language
        lc_call_num   = line[13] # LC call number
        dewey_decimal = line[14] # Dewey decimal number
        bcid          = line[15] # BCID
        date1         = line[16] # date entered
        date2         = line[17] # date entered
        date3         = line[18] # date entered
        date4         = line[19] # date entered
        rating        = line[20] # rating
        collections   = line[21] # rating
        tags          = utbib.utf8_to_bibtex(line[22]) # tags
        review        = line[23] # review
        summary       = utbib.utf8_to_bibtex(line[24]) # summary
        comments      = utbib.utf8_to_bibtex(line[25]) # comments
        privcomments  = utbib.utf8_to_bibtex(line[26]) # review
        copies        = line[27] # review
        encoding      = line[28] # encoding

        if isbn != '[]':
            url = 'http://www.amazon.com/exec/obidos/redirect?path=ASIN/'+isbn[1:-1]
            libthingurl = 'http://www.librarything.com/isbn/'+isbn[1:-1]
        else:
            encoded_title = urllib2.quote_plus(line[1])
            libthingurl = 'http://www.librarything.com/title/'+ encoded_title
            url = 'http://www.librarything.com/title/'+ encoded_title

        # Authors
        author = getauthorslist(author_fl, other_authors)

        # Name of editor, typed as indicated in the LaTeX book. If there is a
        # also an author field, then the editor field gives the editor of the book
        # or collection in which the reference appears.
        editor = ""

        # DEBUG
        # publication is like:
        #    McGraw-Hill (2003), Edition: 2, Paperback
        #    Penguin (Non-Classics) (2002), Edition: Reprint, Paperback
        publication_info = publication.split(",")

        # The publisher's name.
        publisher = publication_info[0].strip()[:-6].strip()

        # The year of publication or, for an unpublished work, the year it was
        # written. Generally it should consist of four numerals, such as 1984,
        # although the standard styles can handle any year whose last four
        # nonpunctuation characters are numerals, such as '(about 1984)'.
        year = date

        # Usually the address of the publisher or other type of institution.
        # For major publishing houses, van Leunen recommends omitting the
        # information entirely. For small publishers, on the other hand, you
        # can help the reader by giving the complete address.
        address = ""

        # In the format of 'First', 'Second', etc.  This should be an ordinal,
        # and should have the first letter capitalized, as shown here; the
        # standard styles convert to lower case when necessary.
        edition = ""
        if len(publication_info) > 1:
            if publication_info[1].strip().startswith('Edition:'):
                edition = publication_info[1].strip()[9:].strip().split(',')[0]
                m = re.compile("(\d+)", re.M).search(edition)
                if m is not None:
                    edition = parseEdition(m.group(1))

        # The volume of a journal or multivolume book.
        volume = ""

        # The number of a journal, magazine, technical report, or of a
        # work in a series. An issue of a journal or magazine is usually
        # identified by its volume and number; the organization that issues a
        # technical report usually gives it a number; and sometimes books are
        # given numbers in a named series.
        number = ""

        # The name of a series or set of books. When citing an entire book,
        # the the title field gives its title and an optional series field gives
        # the name of a series or multi-volume set in which the book is
        # published.
        series = ""

        # The month in which the work was published or, for an unpublished
        # work, in which it was written. You should use the standard three-letter
        # abbreviation, as described in Appendix B.1.3 of the LaTeX book.
        month = ""
        note = comments

        if isbn != '' and isbn != '[]':
            #otherinfo = "ISBN " + isbn[1:-1]
            isbn = isbn[1:-1]
        else:
            isbn = ""

        # Calculate the key (usually author's last name + 4-digit year)
        if author == '':
            if editor == '':
                #print "Warning: %s has no author or editor!" % (title)
                key = "UnknownAuthor" + date
            else:
                key = editor + date
        else:
            #key = author_lf.split(',')[0] + date
            key = cleankey((line[3].split(',')[0]) + date)

        key = valid_key(bib_dict, key)

        # add to bib_dict
        bib_dict[key] = {
            'author' : author,
            'editor' : editor,
            'title' : title,
            'publisher' : publisher,
            'year' : year,
            'address' : address,
            'edition' : edition,
            'volume' : volume,
            'number' : number,
            'series' : series,
            'month' : month,
            'note' : note,
            'isbn' : isbn,
            'tags' : tags,
            'libthingurl': libthingurl,
            'url' : url,
        }

        if expandWCdata:
            expandData = getDictfromISBN(isbn, {'edition','address','publisher'})
            bib_dict[key] = dict(bib_dict[key].items() + expandData.items())

    return bib_dict

