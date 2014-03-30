#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 11 - Compiler part #2
#Date: 04/21/13


import re
from Token import Token

class JackTokenizer:
    currentLine = ""
    currentTokenLength = 0
    currentPartialPeice = ""
    keywords = [ "class"      ,
                 "constructor",
                 "function"   ,
                 "method"     ,
                 "field"      ,
                 "static"     ,
                 "var"        ,
                 "int"        ,
                 "char"       ,
                 "boolean"    ,
                 "void"       ,
                 "true"       ,
                 "false"      ,
                 "null"       ,
                 "this"       ,
                 "let"        ,
                 "do"         ,
                 "of"         ,
                 "else"       ,
                 "while"      ,
                 "retirm"     ]
     
    symbols = [ "{" ,
                "}" ,
                "(" ,
                ")" ,
                "[" ,
                "]" ,
                "." ,
                "," ,
                ";" ,
                "+" ,
                "-" ,
                "*" ,
                "/" ,
                "&" ,
                "|" ,
                "<" ,
                ">" ,
                "=" ,
                "~" ]
                 
    stringConstRegEx = re.compile('^\"[^\"\n\r]*\"$')
    identifierRegEx = re.compile('^[a-zA-Z_]+[a-zA-Z0-0_]*$') #at least one non-numaric charicter at the start, followed by >= 0 word characters(alphanumaric+underscore)
    integerRegEx = re.compile('^[0-9]+$')
    listOfTokens = []
    
    def __init__(self):
        self.currentLine = ""
    
    def advance(self,input):
        self.currentLine = input
        currentChar = ""
        for s in self.currentLine:
            if(self.isKeyword(self.currentPartialPeice) and (not (self.isKeyword(self.currentPartialPeice + s)))):
                tok = Token(self.currentPartialPeice, Token.KEYWORD)
                self.listOfTokens.append(tok)
                self.currentPartialPeice = ""
            elif(self.isSymbol(self.currentPartialPeice)):
                tok = Token(self.getSymbol(self.currentPartialPeice), Token.SYMBOL)
                self.listOfTokens.append(tok)
                self.currentPartialPeice = ""
            elif(self.isIdentifier(self.currentPartialPeice) and (not (self.isIdentifier(self.currentPartialPeice + s)))):
                tok = Token(self.currentPartialPeice, Token.IDENTIFER)
                self.listOfTokens.append(tok)
                self.currentPartialPeice = ""
            elif(self.isStringConst(self.currentPartialPeice)):
                tok = Token(self.currentPartialPeice, Token.STRING_CONST)
                self.listOfTokens.append(tok)
                self.currentPartialPeice = ""
            elif(self.isIntConst(self.currentPartialPeice)):
                tok = Token(self.currentPartialPeice, Token.INT_CONST)
                self.listOfTokens.append(tok)
                self.currentPartialPeice = ""
            
            if(s != " "):
                self.currentPartialPeice += s
        
    def isKeyword(self,peice):
        return peice in self.keywords
    
    def isSymbol(self,peice):
        return peice in self.symbols
    
    def isIntConst(self,peice):
        if(not(len(self.integerRegEx.split(peice))) == 1):
            return 1
        else:
            return 0
        
    def isStringConst(self,peice):
        return (not (len(self.stringConstRegEx.split(peice)) <= 1))
        
    def isIdentifier(self,peice):
        return  (len(self.identifierRegEx.split(peice)) > 1)
        
    def getKeyword(self,peice):
        return peice
        
    def intVal(self,peice):
        return int(peice)
    
    def getIdentifier(self,peice):
        return peice
    
    def stringVal(self,peice):
        return peice
    
    def getSymbol(self,peice):
        return peice
    
