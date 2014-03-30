#Josh Wretlind
#Python Assignment #2
# Course: CSCI/CS 410: Elements of Computing Systems
# Parses comments from a Jack File
# Written in: Python 2.7


# STATES:
# 000 = 0 = default
# 001 = 1 = first / discovered
# 010 = 2 = a second / discovered(line comment, go back to 0 if EOL char found
# 011 = 3 = /* found
# 100 = 4 = potential end of comment found

import sys,string,os

#CONSTANT
newline = 13 #The ascii code for a newline is 13

infile = sys.argv[1] # Sys.argv is the system argument list object
outfile = sys.argv[2]
state = 0
inputlines = 0
f = open(infile,'r')
filecopy = ""

for s in f:
    inputlines += 1 
    if(s != newline):
        filecopy += s

file = ""
file += filecopy
outputfile = ""
i = 0
paststate = 0;
pastchar = ""

#Here's where we begin the file parsing
for s in file:
    paststate = state
    if(s == '/' and state == 0):
        state = 1 #potential start of a comment
    elif(s == '/' and state == 1):
        state = 2 # We're in a line comment 
    elif(s== '*' and state == 1):
        state = 3  # we're in a block comment
    elif(s == '\n' and state == 2):
        state = 0 # comment is done
    elif(s == '*' and state == 3):
        state = 4 #potential end of comment
    elif(s == '/' and state == 4):
        state = 0 #Comment done
    elif(s == '*' and state == 4):
        state = 4 #Hesitate to say the comment is done
    elif(state == 4):
        state = 3 #Nope, comment isn't close to being done
    elif(state == 1):
		state = 0 #If we get anything other than a / or a *, we go here
    
    if(state == 0 and paststate == 0):
        outputfile += s
    elif(state == 0 and paststate == 1):
		outputfile += pastchar 
		outputfile += s
		
    i = i + 1
    pastchar = s
outlines = 1
for c in outputfile:
	if(c == '\n'):
		outlines += 1
output = open(outfile, 'w')
output.write(outputfile)
print "                  INPUT             OUTPUT"
print "Filename          " + infile + "        " + outfile
print "Characters        " + str(len(filecopy)) + "                " + str(len(outputfile))
print "Lines             " + str(inputlines) + "                " + str(outlines)

