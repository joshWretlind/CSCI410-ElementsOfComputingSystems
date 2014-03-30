#Author: Josh Wretlind
#ECS 06 - Assembler/base of the software stack
#Class: CSCI 410 - Elements of Computing Systems
#Written in: Python 2.7

import sys,string,os
from Parser import Parser
from Code import Code
from Symbol import Symbol


infile = sys.argv[1] # Sys.argv is the system argument list object

outfile = infile.replace(".asm",".hack")
parse = Parser(infile)
outfilecontents = ""
code = Code()
sym = Symbol()
i = 0
numOfNonLabelSymbols = 0
while parse.hasMoreCommands():
    parse.advance()
    parse.output()
    parse.stripwhitespace()
    if(len(parse.parsedline) != 0 and parse.parsedline != '\n' and parse.commandType() == 2):
        if(not sym.contains(parse.symbol())):
            sym.addEntry(parse.symbol(),str(i))
    if(len(parse.parsedline) != 0 and parse.parsedline != '\n' and parse.commandType() != 2 ):
        i+=1
        
parse = Parser(infile)
while parse.hasMoreCommands():
    parse.advance()
    parse.output()
    parse.stripwhitespace()
    if(len(parse.parsedline) != 0 and parse.parsedline != '\n' and parse.commandType() == 0 and not sym.contains(parse.symbol())):
       sym.addEntry(parse.symbol(), numOfNonLabelSymbols + 15)
       numOfNonLabelSymbols += 1
       
parse = Parser(infile)
while parse.hasMoreCommands():
    parse.advance()
    parse.output()
    parse.stripwhitespace()
    if(len(parse.parsedline) != 0 and parse.parsedline != '\n' and parse.commandType() == 0):
        if(parse.symbol().isdigit()):
            outfilecontents += "0" + bin(int(parse.symbol()))[2:].zfill(15) + "\n"
        else:
            outfilecontents += "0" + bin(int(sym.GetAddress(parse.symbol())))[2:].zfill(15) + "\n"
    elif(len(parse.parsedline) != 0 and parse.parsedline != '\n' and parse.commandType() == 1):
        dest = parse.parsedline.split('=')
        comp = ()
        jump = ()
        if(len(dest) == 2):
            comp = dest[1].split("=")
        else:
            comp = (dest[0])
            dest = (' ')
        if(len(parse.parsedline.split(';')) > 1):
            jump = parse.parsedline.split(';')
        else:
            jump = (' ',' ')
        outfilecontents += "111" + code.comp(comp[0]) + code.dest(dest[0]) + code.jump(jump[1]) + "\n"
    
    
output = open(outfile, 'w')
output.write(outfilecontents)

