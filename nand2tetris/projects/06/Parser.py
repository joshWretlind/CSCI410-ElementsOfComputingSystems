#Author: Josh Wretlind
#ECS 06 - Assembler/base of the software stack
#Class: CSCI 410 - Elements of Computing Systems
#Written in: Python 2.7

class Parser:
    state = 0
    currentline = ""
    parsedline = ""
    inputlines = 0
    outputlines = 0
    incharcount = 0
    outcharcount = 0
    filetext = ""
    global A_COMMAND
    A_COMMAND = 0
    global C_COMMAND
    C_COMMAND = 1
    global L_COMMAND 
    L_COMMAND = 2
	
    def __init__(self,filename):
        global f
        f = open(filename,'r')
        self.filetext = f.read()
        f = open(filename, 'r')
        
    def advance(self):
        self.currentline = f.readline()
        self.inputlines += 1
        self.incharcount += len(self.currentline)
     
    def hasMoreCommands(self):
        return (self.incharcount != len(self.filetext))
    
    def output(self):
        self.parsedline = ""
        for s in self.currentline:
            paststate = self.state
            if(s == '/' and self.state == 0):
                self.state = 1 #potential start of a comment
            elif(s == '/' and self.state == 1):
                self.state = 2 # We're in a line comment 
            elif(s== '*' and self.state == 1):
                self.state = 3  # we're in a block comment
            elif(s == '\n' and self.state == 2):
                self.state = 0 # comment is done
            elif(s == '*' and self.state == 3):
                self.state = 4 #potential end of comment
            elif(s == '/' and self.state == 4):
                self.state = 0 #Comment done
            elif(s == '*' and self.state == 4):
                self.state = 4 #Hesitate to say the comment is done
            elif(self.state == 4):
                self.state = 3 #Nope, comment isn't close to being done
            elif(self.state == 1):
	        	self.state = 0 #If we get anything other than a / or a *, we go here
    
            if(self.state == 0 and paststate == 0):
                self.parsedline += s
            elif(self.state == 0 and paststate == 1):
	        	self.parsedline += pastchar 
	        	self.parsedline += s
            pastchar = s
        self.outcharcount += len(self.parsedline)
        if(self.parsedline != ""):
            self.outputlines += 1
        return self.parsedline
    
    def commandType(self):
        if(self.parsedline[0] == '@'):
            return A_COMMAND
        elif(self.parsedline[0] == '('):
            return L_COMMAND
        else:
            return C_COMMAND
            
    def stripwhitespace(self):
        self.parsedline = self.parsedline.replace(" ", "")
        self.parsedline = self.parsedline.replace('\t', '')
        self.parsedline = self.parsedline.replace('\n','')
    
    def symbol(self):
        if(self.commandType() == A_COMMAND):
            return self.parsedline.replace("@","")
        else:
            temp = ""
            temp = self.parsedline.replace("(","")
            temp = temp.replace(")","")
            temp = temp.replace('\n', "")
            return temp
            		
    def stats(self):
        print "                  INPUT             OUTPUT"
        print "Characters        " + str(self.incharcount) + "                " + str(self.outcharcount)
        print "Lines             " + str(self.inputlines) + "                " + str(self.outputlines)
