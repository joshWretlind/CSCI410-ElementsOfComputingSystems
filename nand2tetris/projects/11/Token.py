#Defines a token object for the list operator of the tokenizer
#Author: Josh Wretlind
#Class: CSCI 410 - Elements of Computing Systems
#Project: ECS 11 - Compiler part #2
#Date: 04/21/13


class Token:
    identifier  = ""
    typeOfToken = 0 #undefined at this point
    
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFER = 3
    STRING_CONST = 4
    INT_CONST = 5
    
    def __init__(self, iden,typeOfToken):
        self.typeOfToken = typeOfToken
        self.identifier = iden
    def toString(self):
        tag = ""
        if(self.typeOfToken == self.KEYWORD):
            tag = "keyword"
        
        if(self.typeOfToken == self.SYMBOL):
            tag = "symbol"
            
        if(self.typeOfToken == self.IDENTIFER):
            tag = "identifier"
        
        if(self.typeOfToken == self.STRING_CONST):
            tag = "stringConstant"
            
        if(self.typeOfToken == self.INT_CONST):
            tag = "integerConstant"
            
        return "<" + tag + ">" + self.identifier + "</" + tag + ">"
        
