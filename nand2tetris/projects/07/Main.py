#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 07 - VM Part #1
#Date: 03/03/13

import sys,string,os
from Parse import Parser
from CodeWriter import CodeWriter

infile = sys.argv[1] # Sys.argv is the system argument list object

outfile = infile.replace(".vm",".asm")
parse = Parser(infile)
cw = CodeWriter()

while parse.hasMoreCommands():
    parse.advance()
    parse.output()
    arg1 = ""
    arg2 = ""
    print parse.parsedline
    if(parse.commandType() == parse.C_ERROR):
        print "Oops, there was an error"
        break
    elif(parse.commandType() != parse.C_RETURN):
        arg1 = parse.arg1()
    if(parse.commandType() == parse.C_PUSH or parse.commandType() == parse.C_POP or parse.commandType() == parse.C_FUNCTION or parse.commandType() == parse.C_CALL):
        arg2 = parse.arg2()
    cw.write(parse.parsedline, parse)

output = open(outfile, 'w')
output.write(cw.outfile)
