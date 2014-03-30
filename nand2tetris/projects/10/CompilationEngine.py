#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 10 - Compiler part #1
#Date: 04/07/13
from Token import Token

class CompilationEngine:
    
    outtext = ""
    listOfTokens = []
    i = 0 #represents which index we are on
    op = [ "+",
           "-",
           "*",
           "/",
           "&",
           "|",
           "<",
           ">",
           "="]
    keywordConst = ["true" ,
                    "false",
                    "null" ,
                    "this" ]
    
    def __init__(self):
        outtext = ""
        i=0
        
    def setListOfTokens(self,tokens):
        self.listOfTokens = tokens

    def run(self):
        self.compileClass()
            
    def compileClass(self):
        if(not(self.listOfTokens[self.i].identifier == "class" and self.listOfTokens[self.i].typeOfToken == Token.KEYWORD)):
            raise Exception("Syntax Error- Classes must start with 'class' keyword")
        self.outtext += "<class>" + self.listOfTokens[self.i].toString()
        self.i += 1
        
        self.compileIdentifer()
        
        if(not(self.listOfTokens[self.i].identifier == "{" and self.listOfTokens[self.i].typeOfToken == Token.SYMBOL)):
            raise Exception("Syntax Error - class definitions must start with a '{'")
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        
        if(self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and (self.listOfTokens[self.i].identifier == "static" or self.listOfTokens[self.i].identifier == "feild")):
            self.compileClassVarDec()
        
        if(self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and (self.listOfTokens[self.i].identifier == "constructor"
                                                                       or self.listOfTokens[self.i].identifier == "function"
                                                                       or self.listOfTokens[self.i].identifier == "method")):
            self.compileSubroutine()
        
        if(not(self.listOfTokens[self.i].identifier == "}" and self.listOfTokens[self.i].typeOfToken == Token.SYMBOL)):
            raise Exception("Syntax Error - class definitions must end with a '}'")
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        
        self.outtext += "</class>"
        
        
    def compileExpressionList(self):
        return
        
    def compileTerm(self):
        return
        
    def compileExpression(self):
        return
        
    def compileIf(self):
        return
        
    def compileReturn(self):
        return
        
    def compileWhile(self):
        return
        
    def compileLet(self):
        return
        
    def compileDo(self):
        self.outtext += "<doStatement>"
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1 
        
        if(not(self.listOfTokens[self.i].typeOfToken == Token.IDENTIFER)):
            raise Exception("Syntax error - name of the variable is required for do statemets")
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        while(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == "."):
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            
            if(not(self.listOfTokens[self.i].typeOfToken == Token.IDENTIFER)):
                raise Exception("Syntax Error - Identifier required afer . operator")
            
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
        
        if(not(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == "(")):
            raise Exception("Syntax Error - Parameter List required for subroutine call")
        
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        
        
        if(not(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == ";")):
            raise Exceptipn("Syntax error - Missing Semicolon in do statement")
        
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        self.outtext += "</doStatment>"
        
    def compileStatements(self):
        self.outtext += "<statments>"
        while(self.isValidStatement()):
            if(self.listOfTokens[self.i].identifier == "let"):
                self.compileLet()
            elif(self.listOfTokens[self.i].identifier == "if"):
                self.compileIf()
            elif(self.listOfTokens[self.i].identifier == "while"):
                self.compileWhile()
            elif(self.listOfTokens(self.i).identifier == "do"):
                self.compileDo()
            elif(self.listOfTokens(self.i).identifier == "return"):
                self.compileReturn()
        self.outtext += "</statements>"
        
    def compileVarDec(self):
        self.outtext += "<vardec>"
        while(self.listOfTokens[self.i].identifier == "var" and self.listOfTokens[self.i].typeOfToken == Token.KEYWORD):
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            if(not(self.isValidType())):
                raise Exception("Syntax error - type required for variable declarations")
            
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            
            if(not(self.listOfTokens[self.i].typeOfToken == Token.IDENTIFER)):
                raise Exception("Syntax Error - Identifier requried for variable declarations")
            
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            
            while(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == ","):
                self.outtext += self.listOfTokens[self.i].toString()
                self.i += 1
                if(not(self.listOfTokens[self.i].identifier)):
                    raise Exception("Syntax Error - Identifier required for variable declarations")
                
                self.outtext += self.listOfTokens[self.i].toString()
                self.i += 1
                
            if(not(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == ";")):
                raise Exception("Syntax Error - semicolons required at the end of statements")
            
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
        self.outtext += "</vardec>"
        
    def compileParameterList(self):
        self.outtext += "<parameterList>"
        if(self.listOfTokens[self.i].identifier == ")"):
            self.outtext += "</parameterList>"
            return
        while(self.isValidType()):
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            if(self.listOfTokens[self.i].identifier == "," and self.listOfTokens[self.i].typeOfToken == Token.SYMBOL):
                self.outtext += self.listOfTokens[self.i].toString()
                self.i += 1
        self.outtext += "</parameterList>"
            
    def compileSubroutine(self):
        self.outtext += "<subroutineDec>"
        while(self.listOfTokens[self.i].identifier == "constructor" or self.listOfTokens[self.i].identifier == "function" or self.listOfTokens[self.i].identifier == "method"):
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            if(not(self.isValidType() or (self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and self.listOfTokens[self.i].identifier == "void"))):
                raise Exception("Syntax Error - invalid return type for method")
            
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            
            if(not(self.listOfTokens[self.i].typeOfToken == Token.IDENTIFER)):
                raise Exception("Syntax Error - Methods require names")
            
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            
            if(not(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == "(")):
                raise Exception("Syntax Error - Methods require at least an empty parameter list")
                
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            
            self.compileParameterList()
            
            if(not(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == ")")):
                raise Exception("Syntax Error - parameter list not closed")
                
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            
            self.compileSubroutineBody()
            
        self.outtext += "</subroutinedec>"
        
    def compileIdentifer(self):
        if(not(self.listOfTokens[self.i].typeOfToken == Token.IDENTIFER)):
            raise Expeption("Identifier not found")
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        
    def isValidType(self):
        if(self.listOfTokens[self.i].typeOfToken == Token.IDENTIFER or 
               (self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and self.listOfTokens[self.i].identifier == "int") or
               (self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and self.listOfTokens[self.i].identifier == "char") or
               (self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and self.listOfTokens[self.i].identifier == "boolean")):
            return True
        else:
            return False
            
    def compileClassVarDec(self):
        self.outtext += "<classVarDec>"
        while(self.listOfTokens[self.i].identifier == "static" or self.listOfTokens[self.i].identifier == "field"):
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
            if(self.isValidType()):
                self.outtext += self.listOfTokens[self.i].toString()
                self.i += 1
            else:
                raise Exception("Syntax Error - type required for class variables")
                
            if(not(self.listOfTokens[self.i].typeOfToken == Token.identifier)):
                raise Exception("Syntax Error - handle required for class variables")
            
            self.outtext += self.listOfTokens[self.i].toString()
            i += 1
            while(self.listOfTokens[self.i].identifier == "," and self.listOfTokens[self.i].typeOfToken == Token.SYMBOL):
                self.outtext += self.listOfTokens[self.i].toString()
                self.i += 1
                if(not(self.listOfTokens[self.i].typeOfToken == Token.identifier)):
                    raise Exception("Syntax Error - handle required for class variables")
                self.outtext += self.listOfTokens[self.i].toString()
                self.i += 1
            
            if(not(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == ";")):
                raise Excpetion("Syntax Error - Semicolon missing")
            
            self.outtext += self.listOfTokens[self.i].toString()
            self.i += 1
        self.outtext += "</classvardec>"
        
    def compileSubroutineBody(self):
        self.outtext += "<subroutineBody>"

        if(not(self.listOfTokens[self.i].typeOfToken == Token.SYMBOL and self.listOfTokens[self.i].identifier == "{")):
            raise Exception("Syntax Error - curly braces required at begining of the body of the subroutine")
            
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        
        if(self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and self.listOfTokens[self.i].identifier == "var"):
            self.compileVarDec()
            
        if(self.isValidStatement()):
            self.compileStatements()
        
        if(not(self.listOfTokens[self.i].identifier == "}" and self.listOfTokens[self.i].typeOfToken == Token.SYMBOL)):
            raise Exception("Syntax Error - subroutine was never closed")
        
        self.outtext += self.listOfTokens[self.i].toString()
        self.i += 1
        
        self.outtext += "</subroutineBody>"
        
    def isValidStatement(self):
        if(self.listOfTokens[self.i].typeOfToken == Token.KEYWORD and (self.listOfTokens[self.i].identifier == "let"     or
                                                                       self.listOfTokens[self.i].identifier == "if"      or
                                                                       self.listOfTokens[self.i].identifier == "while"   or
                                                                       self.listOfTokens[self.i].identifier == "do"      or
                                                                       self.listOfTokens[self.i].identifier == "return"  )):
            return True
        else:
            return False
    def isValidTerm(self):
        if(self.listOfTokens[self.i].typeOfToken == Token.INT_CONST    or
           self.listOfTokens[self.i].typeOfToken == Token.STRING_CONST or
           self.listOfTokens[self.i].identifier in self.keywordConst   or
           self.listOfTokens[self.i].typeOfToken == Token.IDENTIFER    or
           self.listOfTokens[self.i].identifier in self.unaryOp and self.isValudTerm(self.i + 1)):
            return True
        else:
            return False
    
    def isValidTerm(self,j):
        if(self.listOfTokens[j].typeOfToken == Token.INT_CONST    or
           self.listOfTokens[j].typeOfToken == Token.STRING_CONST or
           self.listOfTokens[j].identifier in self.keywordConst   or
           self.listOfTokens[j].typeOfToken == Token.IDENTIFER    or
           self.listOfTokens[j].identifier in self.unaryOp and self.isValudTerm(j + 1)):
            return True
        else:
            return False

