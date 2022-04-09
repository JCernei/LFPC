import itertools

left, right = 0, 1

def loadInput(inputPath):
	file = open(inputPath).read()
	T = (file.split("NonTerminals:\n")[0].replace("Terminals:\n","").replace("\n",""))
	N = (file.split("NonTerminals:\n")[1].split("Productions:\n")[0].replace("NonTerminals:\n","").replace("\n",""))
	P = (file.split("Productions:\n")[1])

	return cleanAlphabet(T), cleanAlphabet(N), cleanProduction(P)

#Make production easy to work with
def cleanProduction(expression):
	result = []
	#remove spaces and explode on ";"
	rawRulse = expression.replace('\n','').split(';')
	for rule in rawRulse:
		#Explode evry rule on "->" and make a couple
		leftSide = rule.split(' -> ')[0].replace(' ','')
		rightTerminals = rule.split(' -> ')[1].split(' | ')
		for teminal in rightTerminals:
			result.append( (leftSide, teminal.split(' ')) )
	return result

def cleanAlphabet(expression):
	return expression.replace('  ',' ').split(' ')

def seekAndDestroy(target, productions):
	trash, ereased = [],[]
	for production in productions:
		if target in production[right] and len(production[right]) == 1:
			trash.append(production[left])
		else:
			ereased.append(production)
			
	return trash, ereased

def rewrite(target, production):
	result = []
	#get positions corresponding to the occurrences of target in production right side
	positions = [i for i,x in enumerate(production[right]) if x == target]
	#for all found targets in production
	for i in range(len(positions)+1):
		#for all combinations of all possible lenght phrases of targets
		for element in list(itertools.combinations(positions, i)):
			#Example: if positions is [1 4 6]
			#now i've got: [] [1] [4] [6] [1 4] [1 6] [4 6] [1 4 6]
			#erase position corresponding to the target in production right side
			cleanProductionRight = [production[right][i] for i in range(len(production[right])) if i not in element]
			if cleanProductionRight != []:
				result.append((production[left], cleanProductionRight))
	return result

def prettyForm(rules):
	dictionary = {}
	for rule in rules:
		if rule[left] in dictionary:
			dictionary[rule[left]] += ' | '+' '.join(rule[right])
		else:
			dictionary[rule[left]] = ' '.join(rule[right])
	result = ""
	for key in dictionary:
		result += key+" -> "+dictionary[key]+"\n"
	return result