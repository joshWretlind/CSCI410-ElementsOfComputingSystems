#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 07 - VM Part #1
#Date: 03/03/13


class Parser:
    state = 0
    currentline = ""
    parsedline = ""
    inputlines = 0
    outputlines = 0
    incharcount = 0
    outcharcount = 0
    filetext = ""
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8
    C_BLANK = 9
    C_ERROR = 100
	
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
        self.stripwhitespace()
        return self.parsedline
    
    def commandType(self):
        command = self.parsedline.split(' ')
        if(command[0] == ''):
            return self.C_BLANK
        elif(command[0] == 'push'):
            return self.C_PUSH
        elif(command[0] == 'pop'):
            return self.C_POP
        elif(command[0] == 'function'):
            return self.C_FUNCTION
        elif(command[0] == 'label'):
            return self.C_LABEL
        elif(command[0] == 'return'):
            return self.C_RETURN
        elif(command[0][0:1] == 'if'):
            return self.C_IF
        elif(command[0] == 'goto'):
            return self.C_GOTO
        elif(command[0] == 'call'):
            return self.C_CALL
        elif(command[0] == 'add' or command[0] == 'sub' or command[0] == 'neg' or command[0] =='eq' or command[0] == 'gt' or command[0] == 'lt' or command[0] == 'and' or command[0] == 'or' or command[0] == 'not'):
            return self.C_ARITHMETIC
        else:
            return self.C_ERROR

    
    def arg1(self):
        if(self.parsedline != "" and self.commandType() != self.C_ARITHMETIC):
            return self.parsedline.split(" ")[1]
        elif(self.parsedline != "" and self.commandType() == self.C_ARITHMETIC):
            return self.parsedline.split(" ")[0]
            
    def arg2(self):
        if(self.parsedline != ""):
            return self.parsedline.split(" ")[2]

    def stripwhitespace(self):
        #self.parsedline = self.parsedline.replace(" ", "")
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
