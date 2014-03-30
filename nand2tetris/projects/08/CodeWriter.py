#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 08 - VM Part #2
#Date: 03/17/13

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
    pop = "@SP \n A=M-1 \n D= M \n @addr \n M = D \n @SP \n A = M-1 \n M=0 \n D=A-1 \n @SP \n M=D \n"
    functionHeader1 = "@SP \n A = M \n D = A \n @RET M = D \n @SP \n A = M \n"
    pushArg = "@SP \n M = M -1  \n" #Decivingly Simple way of pushing argmuments onto the called frame
    functionHeader2 = "@LCL \n D = M \n @SP \n A = M \n M = D \n @SP \n M = M +1 \n @ARG \n D = M \n @SP \n A = M \n M = D \n @SP \n M = M +1 \n @THIS \n D = M \n @SP \n A = M \n M = D @SP \n M = M + 1 \n @THAT \n D = M \n @SP \n A = M \n M = D \n @SP \n M = M + 1\n @SP \n D = M \n @LCL \n M = D \n @funcName \n 0;JMP \n"
     
    def __init__(self):
        self.outfile = "@256 \n D=A \n @SP \n M=D \n"
        
    def write(self,command,parser):
        self.parser = parser
        if(parser.commandType() == parser.C_ARITHMETIC):
            self.writeArithmetic(command)
        elif(parser.parsedline == ""):
            return
        elif(parser.commandType() == parser.C_LABEL):
            self.writeLabel(parser.arg1())
        elif(parser.commandType() == parser.C_IF):
            self.writeIf(parser.arg1())
        elif(parser.commandType() == parser.C_GOTO):
            self.writeGoto(parser.arg1())
        elif(parser.commandType() == parser.C_RETURN):
            self.writeReturn()
        elif(parser.commandType() == parser.C_FUNCTION):
            self.writeFunction(parser.arg1(), parser.arg2())
        elif(parser.commandType() == parser.C_CALL):
            self.writeCall(parser.arg1(), parser.arg2())
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
        write = ""
        if(segment == "local"):
            write = self.pop.replace("SP", "LCL")
        elif(segment == "argument"):
            write = self.pop.replace("SP", "ARG")
        elif(segment == "this"):
            write = self.pop.replace("SP", "THIS")
        elif(segment == "that"):
            write = self.pop.replace("SP", "THAT")
            
        write = write.replace("addr", str(value))
        self.outfile += write

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
            
    def writeLabel(self, label):
        self.outfile += "(" + label + ")\n"
        
    def writeIf(self, label):
        self.outfile += "@SP \n A = M \n D = M \n @" + label + "\n D;JEQ \n"
        
    def writeGoto(self, label):
        self.outfile += "@" + label + "\n 0;JMP \n"
    
    def writeFunction(self, funcName, numOfArgs):
        self.outfile += "(" + funcName + ") \n"
        for i in range(0,int(numOfArgs)):
            self.writePop(" ","constant", 0)
        
    def writeReturn(self):
        self.outfile += "@RET \n D = M \n @SP \n M = D\n"
         
    def writeCall(self, funcName, numOfArgs):
        self.outfile += functionHeader1
        self.outfile += functionHeader2.replace("funcName", funcName)
        
