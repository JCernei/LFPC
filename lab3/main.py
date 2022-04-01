from lexer import Lexer

fileName = './code_example.txt'
with open(fileName) as f:
    text = f.read()

lexer = Lexer(text)
tokens = lexer.Tokenizer()
f = open("./generatedTokens.txt", "w")
for token in tokens:
    f.write(str(token))
    f.write('\n')
f.close()
for token in tokens:
    print(token)
