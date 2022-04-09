import helper

left, right = 0, 1

terminals, nonTerminals, productions = [],[],[]
variablesJar = ["A", "B", "C","D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


def isUnitary(aProduction, nonTerminals):
	if aProduction[left] in nonTerminals and aProduction[right][0] in nonTerminals and len(aProduction[right]) == 1:
		return True
	return False

def isSimple(aProduction):
	if aProduction[left] in nonTerminals and aProduction[right][0] in terminals and len(aProduction[right]) == 1:
		return True
	return False


for aNonTerminal in nonTerminals:
	if aNonTerminal in variablesJar:
		variablesJar.remove(aNonTerminal)

#Add S0->S rule––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––START
def START(productions, nonTerminals):
	nonTerminals.append('S0')
	return [('S0', [nonTerminals[0]])] + productions
#Remove rules containing both terms and variables, like A->Bc, replacing by A->BZ and Z->c–––––––––––TERM
def TERM(productions, nonTerminals):
	newProductions = []
	#create a dictionari for all base production, like A->a, in the form dic['a'] = 'A'
	dictionary = {}
	for aProduction in productions:
		#if the production is simple, there is nothing to change
		if isSimple(aProduction):
			newProductions.append(aProduction)
		else:
			for aTerminal in terminals:
				for index, value in enumerate(aProduction[right]):
					if aTerminal == value and not aTerminal in dictionary:
						#it's created a new production nonTerminal -> aTerminal and added to it 
						dictionary[aTerminal] = variablesJar.pop()
						#Variables set it's updated adding new variable
						nonTerminals.append(dictionary[aTerminal])
						newProductions.append((dictionary[aTerminal], [aTerminal]))
						aProduction[right][index] = dictionary[aTerminal]
					elif aTerminal == value:
						aProduction[right][index] = dictionary[aTerminal]

			newProductions.append((aProduction[left], aProduction[right]))
			
	#merge created set and the introduced rules
	return newProductions

#Eliminate non unitry rules––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––BIN
def BIN(productions, nonTerminals):
	result = []
	for production in productions:
		lenProductionRight = len(production[right])
		if lenProductionRight <= 2:
			result.append(production)
		else:
			newVar = variablesJar.pop(0)
			nonTerminals.append(newVar+'1')
			result.append((production[left], [production[right][0]]+[newVar + '1']))
			i = 1
			for i in range(1, lenProductionRight - 2):
				var, var2 = newVar + str(i), newVar + str(i + 1)
				nonTerminals.append(var2)
				result.append((var, [production[right][i], var2]))
			result.append((newVar + str(lenProductionRight - 2), production[right][lenProductionRight - 2 : lenProductionRight])) 
	return result
	

#Delete non terminal rules–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––DEL
def DEL(productions):
	newSet = []
	#seekAndDestroy throw back in:
	#        – outlaws all left side of productions such that right side is equal to the outlaw
	#        – productions the productions without outlaws 
	outlaws, productions = helper.seekAndDestroy(target='empty', productions = productions)
	#add new reformulation of old rules
	for outlaw in outlaws:
		#consider every production: old + new resulting important when more than one outlaws are in the same prod.
		for production in productions + [e for e in newSet if e not in productions]:
			#if outlaw is present in the right side of a rule
			if outlaw in production[right]:
				#the rule is rewriten in all combination of it, rewriting "e" rather than outlaw
				#this cycle prevent to insert duplicate rules
				newSet = newSet + [e for e in  helper.rewrite(outlaw, production) if e not in newSet]

	#add unchanged rules and return
	return newSet + ([productions[i] for i in range(len(productions)) if productions[i] not in newSet])

#------------------------------------------------------------------------------------------------------------
def unit_routine(productions, nonTerminals):
	unitaries, result = [], []
	#check if a rule is unitary
	for aProduction in productions:
		if isUnitary(aProduction, nonTerminals):
			unitaries.append( (aProduction[left], aProduction[right][0]) )
		else:
			result.append(aProduction)
	#replace it in all the others
	for uni in unitaries:
		for aProduction in productions:
			if uni[right] == aProduction[left] and uni[left] != aProduction[left]:
				result.append( (uni[left], aProduction[right]) )
	
	return result

def UNIT(productions, nonTerminals):
	result = unit_routine(productions, nonTerminals)
	tmp = unit_routine(result, nonTerminals)
	while result != tmp :
		result = unit_routine(tmp, nonTerminals)
		tmp = unit_routine(result, nonTerminals)
		
	return result

def NONGENERATING(productions):
	generating = set(terminals)

	hasUnprocessed = True
	while hasUnprocessed:
		hasUnprocessed = False
		for production in productions:
			prodGenerating = [x for x in production[right] if x in generating]
			if len(prodGenerating) == len(production[right]) and production[left] not in generating:
				generating.add(production[left])
				hasUnprocessed = True
	
	productions = [x for x in productions if x[left] in generating]
	for production in productions:
		cleanedRight = [x for x in production[right] if x in generating]
		production = (production[left], cleanedRight)
	
	return productions

def UNREACHEABLE(productions, nonTerminals):
	for nonTerminal in nonTerminals:
		found = False
		for production in productions:
			if nonTerminal in production[right]:
				found = True
				break
		if not found:
			productions = [prod for prod in productions if prod[left] != nonTerminal]
			nonTerminals.remove(nonTerminal)
	return productions

	
terminals, nonTerminals, productions = helper.loadInput('input.txt')

# productions = START(productions, nonTerminals)
# print(helper.prettyForm(productions))
# open('output.txt', 'w').write(	helper.prettyForm(productions))
# open('output.txt', 'a').write('\n')
open('output.txt', 'w').write(helper.prettyForm(productions))
open('output.txt', 'a').write('\n')

productions = DEL(productions)
print(helper.prettyForm(productions))
open('output.txt', 'a').write('Delete empty \n')
open('output.txt', 'a').write(helper.prettyForm(productions))
open('output.txt', 'a').write('\n')

productions = NONGENERATING(productions)
print( helper.prettyForm(productions))
open('output.txt', 'a').write('Remove nongenerating \n')
open('output.txt', 'a').write(	helper.prettyForm(productions))
open('output.txt', 'a').write('\n')

productions = UNREACHEABLE(productions, nonTerminals)
print( helper.prettyForm(productions))
open('output.txt', 'a').write('Remove unreachable \n')
open('output.txt', 'a').write(	helper.prettyForm(productions))
open('output.txt', 'a').write('\n')

productions = TERM(productions, nonTerminals)
print( helper.prettyForm(productions))
open('output.txt', 'a').write('Eliminate rules with nonsolitary terminals \n')
open('output.txt', 'a').write(	helper.prettyForm(productions))
open('output.txt', 'a').write('\n')

productions = BIN(productions, nonTerminals)
print( helper.prettyForm(productions))
open('output.txt', 'a').write('Eliminate right-hand sides with more than 2 nonterminals \n')
open('output.txt', 'a').write(	helper.prettyForm(productions))
open('output.txt', 'a').write('\n')

productions = UNIT(productions, nonTerminals)
print( helper.prettyForm(productions))
open('output.txt', 'a').write('Eliminate unit rules \n')
open('output.txt', 'a').write(	helper.prettyForm(productions))

print( len(productions) )
