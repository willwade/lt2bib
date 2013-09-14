lt2bib
======

LibraryThing-to-BibTeX convertor

##lt2bib.py ##

A line command tool to access LibraryThing to BibTex. 

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

For example:
    lt2bib.py -l LibThing.csv 

Will output a formatted LibThing.bib file in the same folder.

    lt2bib.py -u username -p password -o MyLib.bib

Will login to LibraryThing, download the correct CSV file and convert it to MyLib.bib



##libthing.py ##

A poorly named (and written) library of the LibraryThingToBibtex tools. A quick aspect of functions:

###downloadLTCSV(user,password,File) ###

Download the CSV file from LibraryThing for you. Just provide a valid username, password and file where you want it saved

###getDictfromISBN(isbn,needItems:{item1,item2})

Provide a ISBN code and a dict of items required (e.g. {author,editor,publisher,year}) and it will pass back a dict of information for that ISBN

###writeBibTex(dictData, bibFile) ###

Provide a dict structure and parse it to a BibTex file

###ltcsv_to_dictdata(csvdata, expandWCData=False) ###

Convert a CSV file from LibraryThing to dictdata required for the Conversion (writeBibTex())

##index.html, lt2bib.cgi##

A little bit of code to make a web front end. Doesn't include a way of logging in to LibThing but just converts an already saved CSV file. 
