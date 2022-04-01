from token_type import TokenType

class Token:
    predefinedKeywords = {
        "PROCEED" : TokenType.PROCEED,
        "STOP" : TokenType.STOP,
        "function" : TokenType.FUNCTION,
        "Main" : TokenType.MAIN,
        "var" : TokenType.VAR,
        "true" : TokenType.TRUE,
        "false" : TokenType.FALSE,
        "null" : TokenType.NULL,
        "return" : TokenType.RETURN,
        "message" : TokenType.MESSAGE,
        "input" : TokenType.INPUT,
        "output" : TokenType.OUTPUT,
        "if" : TokenType.IF,
        "else" : TokenType.ELSE,
        "elif" : TokenType.ELIF,
        "pow" : TokenType.POW,
    }

    valueTypes = [TokenType.IDENTIFIER, TokenType.NUMBER_VALUE, TokenType.STRING_VALUE]
    
    def __init__(self, tokenType, value):
        self.TokenType = tokenType
        self.Value = value
    
    @classmethod
    def CheckKeyword(cls, keyword):
        if keyword in cls.predefinedKeywords:
            return cls.predefinedKeywords[keyword] 
        else:
            return TokenType.IDENTIFIER

    def __str__(self):
        if self.TokenType in self.valueTypes:
            return f'{self.TokenType}: ({self.Value})'
        return str(self.TokenType)
