from token_type import TokenType
from _token import Token

class Lexer:
    def __init__(self, input):
        self.input = input
        self.currentPosition = 0
        self.nextPosition = 0
        self.currentChar = None
    
    def Tokenizer(self):
        self.ReadChar()
        tokens = []
        token = self.NewToken()
        tokens.append(token)
        while token.TokenType != TokenType.EOF:
            token = self.NewToken()
            tokens.append(token)
        return tokens    

    #Generate token based on current char value
    def NewToken(self):
        token = None
        self.SkipWhitespaces()
        if self.currentChar == '+':
            if self.PeekChar() == '+':
                self.ReadChar() #move one step forward
                token = Token(TokenType.INCREMENT, "INCREMENT")
            else:
                token = Token(TokenType.ADDITION, "ADDITION")
        elif self.currentChar == '-':
            if self.PeekChar() == '-':
                self.ReadChar()
                token = Token(TokenType.DECREMENT, "DECREMENT")
            else:
                token = Token(TokenType.SUBTRACTION, "SUBTRACTION")
        elif self.currentChar == '*':
            token = Token(TokenType.MULTIPLICATION, "MULTIPLICATION")
        elif self.currentChar == '/':
            token = Token(TokenType.DIVISION, "DIVISION")
        elif self.currentChar == '!':
            if self.PeekChar == '=':
                self.ReadChar()
                token = Token(TokenType.NOT_EQUAL, "NOT_EQUAL")
            else:
                token = Token(TokenType.NOT, "NOT")
        elif self.currentChar == '>':
            if self.PeekChar() == '=':
                self.ReadChar()
                token = Token(TokenType.GREATER_OR_EQUAL, "GREATER_OR_EQUAL")
            else:
                token = Token(TokenType.GREATER, "GREATER")
        elif self.currentChar == '<':
            if self.PeekChar() == '=':
                self.ReadChar()
                token = Token(TokenType.LESS_OR_EQUAL, "LESS_OR_EQUAL")
            else: 
                token =  Token(TokenType.LESS, "LESS")
        elif self.currentChar == '=':
            if self.PeekChar() == '=':
                self.ReadChar()
                token =  Token(TokenType.EQUAL, "EQUAL")
            else:
                token = Token(TokenType.ASSIGN, "ASSIGN")
        elif self.currentChar == ',':
            token = Token(TokenType.COMMA, "COMMA")
        elif self.currentChar == ';':
            token = Token(TokenType.SEMICOLON, "SEMICOLON")
        elif self.currentChar == '(':
            token = Token(TokenType.OPEN_PARENTHESIS, "OPEN_PARENTHESIS")
        elif self.currentChar == ')':
            token = Token(TokenType.CLOSE_PARENTHESIS, "CLOSE_PARENTHESIS")
        elif self.currentChar == '[':
            token = Token(TokenType.OPEN_BRACKET, "OPEN_BRACKET")
        elif self.currentChar == ']':
            token = Token(TokenType.CLOSE_BRACKET, "CLOSE_BRACKET")
        elif self.currentChar == '{':
            token = Token(TokenType.OPEN_BRACE, "OPEN_BRACE")
        elif self.currentChar == '}':
            token = Token(TokenType.CLOSE_BRACE, "CLOSE_BRACE")
        elif self.currentChar == '\0':
            token = Token(TokenType.EOF, "")
        elif self.currentChar == '"':
            self.ReadChar(); #skip quotation mark at the beginning of the string
            str = self.ReadString()
            self.ReadChar(); #skip quotation mark at the end of the string
            return Token(TokenType.STRING_VALUE, str)
        else:
            if self.currentChar.isalpha():
                literal = self.ReadIdentifier()
                tokenType = Token.CheckKeyword(literal)
                return Token(tokenType, literal)
            elif self.currentChar.isdigit():
                return self.ReadNumber()
            else:
                token = Token(TokenType.ILLEGAL, str(self.currentChar))

        self.ReadChar()
        return token

    def SkipWhitespaces(self):
        while self.currentChar in [' ', '\t', '\n', '\r']:
            self.ReadChar()

    def ReadChar(self):
        #check if EOF
        #go to next char
        if self.nextPosition >= len(self.input): 
            self.currentChar = '\0'
        else:
            self.currentChar = self.input[self.nextPosition]
        self.currentPosition = self.nextPosition
        self.nextPosition += 1

    def ReadIdentifier(self):
        pos = self.currentPosition
        while self.currentChar.isalpha() or self.currentChar.isdigit():
            self.ReadChar()
        #return identifier
        return self.input[pos: self.currentPosition]
    
    def ReadString(self):
        pos = self.currentPosition
        while self.currentChar != '"':
            self.ReadChar()
        #return string
        return self.input[pos: self.currentPosition]
  
    def ReadNumber(self):
        #natural number
        pos = self.currentPosition
        while self.currentChar.isdigit():
            self.ReadChar()
        #float number
        if self.currentChar == '.':
            self.ReadChar(); #skip dot
            while self.currentChar.isdigit():
                self.ReadChar()
        #return number
        return Token(TokenType.NUMBER_VALUE, self.input[pos: self.currentPosition])

    def PeekChar(self):
        if self.nextPosition > len(self.input):
            return '\0'
        return self.input[self.nextPosition]
