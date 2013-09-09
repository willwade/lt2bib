# ==================== MAIN LOOP =========================================
import libthing as lt2bib
import sys, codecs


if len(sys.argv) < 2:
    print "Usage:", sys.argv[0], "[-l]", "<tab-delimited file>"
    print "\t-l\tGenerates a LaTeX file that tests the BibTeX file."
    print "\nExample:", sys.argv[0], "LibraryThing_TD.xls"

    sys.exit(1)
    
# Open the bookdata.csv file
latex = False
for arg in sys.argv:
    if arg[0] != '-':
        input_file = arg
    if arg == "-l":
        latex = True

"""
NB: Can now do a download of the data instead if thats useful
"""
#lt2bib.downloadLTCSV('user','pass')
bookdata = codecs.open(input_file, 'rb', 'utf-16')
# False/True if you want to fill in missing info from Worldcat
bib_dict = lt2bib.ltcsv_to_dictdata(bookdata, False)
lt2bib.writeBibTex(bib_dict, 'LibThing.bib')

"""
You can get data from WorldCat if thats useful
"""
#print lt2bib.getDictfromISBN('08889X')

"""
Just not sure about LaTex! Sorry!
"""
#if latex:
#    lt2bib.writeLaTex(bib_dict)
#else:
#    lt2bib.writeBibTex(bib_dict, 'LibThing.bib')
