lt2bib
======

LibraryThing-to-BibTeX convertor

##lt2bib.py ##

A line command tool to access LibraryThing to BibTex. Will add some more flags as time goes on

##libthing.py ##

A poorly named (and written) library of the LibraryThingToBibtex tools. A quick aspect of functions

###downloadLTCSV(user,password,File) ###

Download the CSV file from LibraryThing for you. Just provide a valid username, password and file where you want it saved

###getDictfromISBN(isbn,needItems:{item1,item2})

Provide a ISBN code and a dict of items required (e.g. {author,editor,publisher,year}) and it will pass back a dict of information for that ISBN

###writeBibTex(dictData, bibFile) ###

Provide a dict structure and parse it to a BibTex file

###ltcsv_to_dictdata(csvdata, expandWCData=False) ###

Convert a CSV file from LibraryThing to dictdata required for the Conversion (writeBibTex())

##cgi/lt2bib.cgi ##

A little bit of code (and supporting php/style files) to make a web front end
