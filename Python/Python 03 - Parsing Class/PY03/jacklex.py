#Author: Josh Wretlind
#Python Assignment #3
#Class: CSCI 410 - Elements of Computing Systems
#Written in: Python 2.7

import sys,string,os
from Parser import Parser

infile = sys.argv[1] # Sys.argv is the system argument list object
outfile = sys.argv[2]

parse = Parser(infile)
outfilecontents = ""
while parse.hasMoreCommands():
    parse.advance()
    outfilecontents += parse.output()
    
output = open(outfile, 'w')
output.write(outfilecontents)

parse.stats()
