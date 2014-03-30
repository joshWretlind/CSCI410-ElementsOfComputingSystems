#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 07 - VM Part #1
#Date: 03/03/13

# Add command:
# --SP
# D = M
# --SP
# A = M
# M = D+A
# ++SP

#Subtract Command:
# --SP
# D = M
# --SP
# A = M
# M = D-A
# ++SP

#Negation:
# @SP
# D = M
# M = -D

#OR:
# --SP
# D = M
# --SP
# M = D|M
# ++SP

#Not:
# $SP
# M = !M

#EQ:
# --sp
# D = M
# --SP 
# @SET
# D = D-M;JEQ
# M = -1 //False
# (set)
# M = 0

class CodeWriter:
    i = 0
    Arith = {'add':'@SP \n A=M-1 \n D=M \n A=A-1 \n M = D+M \n D=A+1 \n @SP \n M=D \n',
             'sub':'@SP \n A=M-1 \n D=M \n A=A-1 \n M=D-M \n M = -M \n D=A+1 \n @SP \n M=D\n',
             'neg':'@SP \n A=M-1 \n D=M \n M=-D \n A=A+1 \n',
             'eq' :'@SP \n A=M-1 \n D=M \n A=A-1 \n D = D-M \n @set \n D;JEQ \n @SP \n A = M-1 \n A = A -1 \n M = 0 \n @end \n 0;JMP \n (set) \n @SP \n A = M-1 \n A = A -1 \n M = -1 \n (end) \n @SP \n D = M-1 \n M = D \n',
             'gt' :'@SP \n A=M-1 \n D=M \n A=A-1 \n D = D-M \n @set \n D;JLT \n @SP \n A = M-1 \n A = A -1 \n M = 0 \n @end \n 0;JMP \n (set) \n @SP \n A = M-1 \n A = A -1 \n M = -1 \n (end) \n @SP \n D = M-1 \n M = D \n',
             'lt' :'@SP \n A=M-1 \n D=M \n A=A-1 \n D = D-M \n @set \n D;JGT \n @SP \n A = M-1 \n A = A -1 \n M = 0 \n @end \n 0;JMP \n (set) \n @SP \n A = M-1 \n A = A -1 \n M = -1 \n (end) \n @SP \n D = M-1 \n M = D \n',
             'and':'@SP \n A=M-1 \n D=M \n A=A-1 \n M=D&M \n D=A+1 \n @SP \n M=D\n',
             'or' :'@SP \n A=M-1 \n D=M \n A=A-1 \n M=D|M \n D=A+1 \n @SP \n M=D\n',
             'not':'@SP \n A=M-1 \n M=!M \n D=A+1 \n @SP \n M=D\n'}
                
    stackPointer = 256
    outfile = ""
    pop = "@SP \n A=M-1 \n M=0 \n D=A-1 \n @SP \n M=D \n"
    
    def __init__(self):
        self.outfile = "@256 \n D=A \n @SP \n M=D \n"
        
        
    def write(self,command,parser):
        self.parser = parser
        if(parser.commandType() == parser.C_ARITHMETIC):
            self.writeArithmetic(command)
        elif(parser.parsedline == ""):
            return
        else:
           self.writePushPop(command)
        
    def writeArithmetic(self,command):
        test = self.Arith[command]
        if(command == 'eq' or command == 'gt' or command == 'lt'):
            test = test.replace("@set", "@set_" + str(self.i))
            test = test.replace("(set)", "(set_" + str(self.i) + ")")
            test = test.replace("@end", "@end_" + str(self.i))
            test = test.replace("(end)", "(end_" + str(self.i) + ")")
            self.i += 1
        self.outfile += test
    
    def writePushPop(self,command):
        if(self.parser.commandType() == self.parser.C_POP):
            self.writePop(command,self.parser.arg1(),self.parser.arg2())
        else:
            self.writePush(command,self.parser.arg1(),self.parser.arg2())

    def writePop(self,command,segment,value):
        self.outfile += pop

    def writePush(self, command,segment, value):
        if(segment == "constant"):
            adds = "@" + value + "\n D = A \n"
            adds += "@SP \n A = M \n M = D \n @SP \n M = M +1\n"
            self.outfile += adds
        elif(segment == "local"):
            adds = "@" + value + "\n D = A \n"
            adds += "@LCL \n A = M \n M = D \n @LCL \n M = M +1\n"
            self.outfile += adds
        elif(segment =="argument"):
            adds = "@" + value + "\n D = A \n"
            adds += "@ARG \n A = M \n M = D \n @ARG \n M = M +1\n"
            self.outfile += adds
        elif(segment == "this"):
            adds = "@" + value + "\n D = A \n"
            adds += "@THIS \n A = M \n M = D \n @THIS \n M = M +1\n"
            self.outfile += adds
        elif(segment == "that"):
            adds = "@" + value + "\n D = A \n"
            adds += "@THAT \n A = M \n M = D \n @THAT \n M = M +1\n"
            self.outfile += adds
