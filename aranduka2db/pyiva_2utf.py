#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:        pyiva_2utf.py (Python 3.x).
# description: Convert exported CVS file from Aranduka to UTF - for import to MySQL
# purpose:     Construcción de menús, barras de herramientas
#              y de estado 
# author:      python para impacientes
#
#------------------------------------------------------------

   
__author__ = 'Klemens Häckel'
__title__= 'pyiva_2utf.py'
__date__ = '202106'
__version__ = '0.0.1'
__license__ = 'GNU GPLv3'

import glob, sys
import codecs, chardet

"""

history:
002: 
test.. optimized imported columns (table egresos) function colshuffle - not used, but ready

001: initial version
conserve original structure of exported spreadsheet (table aranduka_egresos)

"""

def prompt_confirm(question, answer = 'yYsS'):
    answer_is = False
    try:
        # python 2
        answer_is = raw_input( question + " ? (y/n)>" )[:1] in answer
    except NameError:
        # python 3
        #print("Not in scope!")
        answer_is = input( question + " ? (y/n)>" )[:1] in answer
    
    return answer_is


def colshuffle(lstring_in, picks = [-1, -1, 0, 1,3,2,4]):
    # use negative picks item to add additional tab spacing
    lstring = ""
    ltick = 0
    
    ltemp = lstring_in.split()      # careful columns with space within the text
    for pp in picks:
        if ltick > 0:
            lstring += "\t"    
        ltick += 1
        if pp >= 0 and ltemp[pp]:
            lstring += ltemp[pp]
    
    return lstring + "\n"


def file_xiso(in_filename):
    sourceEncoding = "iso-8859-1"       # 
    try:
        bytes_file = open(in_filename,  errors="surrogateescape").read()
        chardet_data = chardet.detect(bytes_file)
        sourceEncoding = (chardet_data['encoding'])
    except:
        bytes_file = open(in_filename, encoding='iso-8859-1').read()
        sourceEncoding = "iso-8859-1"       # 
    print (sourceEncoding)

    targetEncoding = "utf-8"
    source = open(in_filename, "r",  encoding=sourceEncoding, errors="surrogateescape")
    target = open(in_filename.split(".")[0] + ".csv", "w",  encoding=targetEncoding)

    #target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))
    #lines = source.readlines()[1:]
    for line in source.readlines()[1:]: 
        #print (line[:70])
        try:
            target.write(unicode(line, sourceEncoding).encode(targetEncoding))
        except:
            target.write(line)
            
        #target.write(colshuffle(unicode(line, sourceEncoding).encode(targetEncoding)))


def main():
    ''' Iniciar aplicación '''
    get_filename = "LIE_2019_94e9090a_33507_952-egresos.xls"
    
    searchlike = ['egresos', 'ingresos']
    for xfile in searchlike:

        get_filename = "LIExx"
        #for infile in glob.glob("*egresos.xls"):
        for infile in glob.glob("*" + xfile + ".xls"):
            #if input("Procesar archivo " + infile + " [Y/N]? ").lower() in "ys":
            if prompt_confirm("Procesar archivo " + infile + " [Y/N]? "):
                get_filename = infile
                break
        print ("procesando: " + get_filename)

        #in_filename = "LIE_2019_94e9090a_33507_952-egresos.xls"
        if get_filename == "LIExx":
            print("no hay archivo de origen")
            sys.exit("no hay archivo de origen")
        
        file_xiso(get_filename)

    print("finish..")


if __name__ == '__main__':
    main()
