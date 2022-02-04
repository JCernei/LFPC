import pprint
import graphviz

TERMINAL = "."
EXIT = "exit"
id = 0
myGrammar = dict()
transformation = dict()

while True: 
    myInput = input()
    if myInput == EXIT:
	    break
    lp, rp = myInput.split(' -> ')
    rp = [x for x in rp]

    # Transform LeftPart into q0 notation
    if lp not in transformation:
        transformation[lp] = f"q{id}"
        id += 1
    lp = transformation[lp]

    # Check for Terminal symbol
    if len(rp) == 1 and rp[0].islower():
        if TERMINAL not in transformation:
            transformation[TERMINAL] = f"q{id}"
            id += 1
        rp.append(transformation[TERMINAL])

    # Transform RightPart UppercaseLetter ito q0 notation
    for index, prod in enumerate(rp):
        if prod in transformation:
            rp[index] = transformation[prod]
        elif prod.isupper():
            transformation[prod] = f"q{id}"
            id += 1
            rp[index] = transformation[prod]

    # Add or Update grammar with LeftPart: RightPart
    if lp not in myGrammar:
        myGrammar[lp] = [rp]
    else:
        myGrammar[lp].append(rp)
# Display FA
pprint.pprint(myGrammar)

# Plot Finite Automaton
f = graphviz.Digraph('d', filename='variant_8_image.gv', format='png')
f.attr(rankdir='LR', size='8,5')
f.attr('node', shape='none')
f.node('')
f.attr('node', shape='circle')
f.edge('', 'q0', label='')
f.attr('node', shape='doublecircle')
f.node(transformation[TERMINAL])
f.attr('node', shape='circle')
for key in myGrammar:
    for pair in myGrammar[key]:
        f.edge(key, pair[1], label=pair[0])
try:
    f.view()
except:
    print("An exception occurred")

# Check if input string is accepted by FA
while True: 
    myInput = input("Word to check: ")
    if myInput == EXIT:
	    break

    possibleNodes = [myGrammar["q0"]]
    isCorrect = True
    for index, letter in enumerate(myInput):
        possibleLetters = [pair[0] for node in possibleNodes for pair in node]
        # Check if the current node is terminal
        canBeTerminal = False
        for node in possibleNodes:
            for pair in node:
                if pair[0] == letter and pair[1] not in myGrammar:
                    canBeTerminal = True
                    break
            if canBeTerminal:
                break
        if index == len(myInput) - 1 and not canBeTerminal:
            isCorrect = False
            break
        #Check for the next possible nodes
        possibleNodes = [myGrammar[pair[1]] for node in possibleNodes for pair in node if pair[0] == letter and pair[1] in myGrammar]
        if letter not in possibleLetters:
            isCorrect = False
            break
        
    if isCorrect:
        print("CORRECT")
    else:
        print("WRONG")

# Variant 8:
# S -> aD
# D -> dE
# D -> bJ
# J -> cS
# E -> e
# E -> aE
# D -> aE
# exit