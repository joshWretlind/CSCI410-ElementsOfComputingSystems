#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 10 - Compiler part #1
#Date: 04/07/13

import sys,string,os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from Parse import Parse

infile = sys.argv[1] # Sys.argv is the system argument list object

outfile = infile.replace(".jack",".xml")
parse = Parse(infile)
infileText = ""
jtok = JackTokenizer()

tokenList = []

while parse.hasMoreCommands():
    parse.advance()
    blah = parse.output()
    infileText += blah
    jtok.advance(blah)

tokenList.extend(jtok.listOfTokens)

ce = CompilationEngine()
ce.setListOfTokens(tokenList)
ce.run()

print ce.outtext
    
output = open(outfile, 'w')

output.write(ce.outtext)


