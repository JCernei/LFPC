from prettytable import PrettyTable
import copy


def parseGrammar(rules):
    for rule in rules:
        k = rule.split("->")
        # remove un-necessary spaces
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multipleRhs = rhs.split('|')
        # remove un-necessary spaces
        for i in range(len(multipleRhs)):
            multipleRhs[i] = multipleRhs[i].strip()
            multipleRhs[i] = multipleRhs[i].split()
        diction[k[0]] = multipleRhs


def removeLeftRecursion(rulesDiction):
    store = {}
    for lhs in rulesDiction:
        # recursiveRules stores subrules with left-recursion
        # nonRecursiveRules stores subrules without left-recursion
        recursiveRules = []
        nonRecursiveRules = []
        # get rhs for current lhs
        allRhs = rulesDiction[lhs]
        for subRhs in allRhs:
            if subRhs[0] == lhs:
                recursiveRules.append(subRhs[1:])
            else:
                nonRecursiveRules.append(subRhs)
        # now form two new rules
        if len(recursiveRules) != 0:
            # to generate new unique symbol add ' till unique not generated
            newLhs = lhs + "'"
            while (newLhs in rulesDiction.keys()) \
                    or (newLhs in store.keys()):
                newLhs += "'"
            # make nonRecursive rule
            for b in range(0, len(nonRecursiveRules)):
                nonRecursiveRules[b].append(newLhs)
            rulesDiction[lhs] = nonRecursiveRules
            # make recursive rule
            for a in range(0, len(recursiveRules)):
                recursiveRules[a].append(newLhs)
            recursiveRules.append(['empty'])
            # store in temp dict, append to rulesDiction at end of traversal
            store[newLhs] = recursiveRules
    # add newly generated rules generated after removing left recursion
    for left in store:
        rulesDiction[left] = store[left]
    return rulesDiction


def leftFactoring(rulesDiction):
    newDict = {}
    for lhs in rulesDiction:
        allRhs = rulesDiction[lhs]
        temp = {}
        for subRhs in allRhs:
            if subRhs[0] not in list(temp.keys()):
                temp[subRhs[0]] = [subRhs]
            else:
                temp[subRhs[0]].append(subRhs)
        # if value list count for any key in temp is > 1, it has left factoring
        # newRule stores new subrules for current LHS symbol
        newRule = []
        # tempDict stores new subrules for left factoring
        tempoDict = {}
        for termKey in temp:
            if len(temp[termKey]) > 1:
                newLhs = lhs + "'"
                while (newLhs in rulesDiction.keys()) \
                        or (newLhs in tempoDict.keys()):
                    newLhs += "'"
                # append the left factored result
                newRule.append([termKey, newLhs])
                # add expanded rules to tempoDict
                expandedRules = []
                for lfProduction in temp[termKey]:
                    expandedRules.append(lfProduction[1:])
                tempoDict[newLhs] = expandedRules
            else:
                # no left factoring required
                newRule.append(temp[termKey][0])
        # add original rule
        newDict[lhs] = newRule
        # add newly generated rules after left factoring
        for key in tempoDict:
            newDict[key] = tempoDict[key]
    return newDict


def first(rule):
    # condition for terminal or empty
    if rule[0] in terminalsList:
        return rule[0]
    elif rule[0] == 'empty':
        return 'empty'

    # condition for Non-Terminals
    if rule[0] not in diction:
        return
    # firstRes temporary list of result
    firstRes = []
    rhsRules = diction[rule[0]]
    # call first on each rule of RHS fetched and take union
    for rhsRule in rhsRules:
        indivRes = first(rhsRule)
        if type(indivRes) is list:
            for i in indivRes:
                firstRes.append(i)
        else:
            firstRes.append(indivRes)
    # if no empty in result return firstRes
    if 'empty' not in firstRes:
        return firstRes
    # apply empty rule: first(ABC)=first(A)-{e} U first(BC)
    newList = []
    firstRes.remove('empty')
    if len(rule) > 1:
        ansNew = first(rule[1:])
        if ansNew != None:
            if type(ansNew) is list:
                newList = firstRes + ansNew
            else:
                newList = firstRes + [ansNew]
        else:
            newList = firstRes
        return newList
    firstRes.append('empty')
    return firstRes


def follow(nonTerminal):
    # for start symbol add $
    followSet = set()
    if nonTerminal == startSymbol:
        followSet.add('$')

    for currNT in diction:
        rhs = diction[currNT]
        for subrule in rhs:
            # call for all occurrences on non terminal in subrule
            while nonTerminal in subrule:
                indexNonTerminal = subrule.index(nonTerminal)
                subrule = subrule[indexNonTerminal + 1:]
                if len(subrule) != 0:
                    # compute first() if symbols of RHS of target non terminal exists
                    res = first(subrule)
                    # if empty in result apply rule (A->aBX): follow(B)=(first(X)-{e}) U follow(A)
                    if 'empty' in res:
                        newList = []
                        res.remove('empty')
                        ansNew = follow(currNT)
                        if ansNew != None:
                            if type(ansNew) is list:
                                newList = res + ansNew
                            else:
                                newList = res + [ansNew]
                        else:
                            newList = res
                        res = newList
                else:
                    # use the rule  A -> aB, FOLLOW(B) = FOLLOW(A)
                    if nonTerminal != currNT:
                        res = follow(currNT)

                # add follow result in set form
                if res is not None:
                    if type(res) is list:
                        for g in res:
                            followSet.add(g)
                    else:
                        followSet.add(res)
    return list(followSet)


def computeAllFirsts():
    for nonTerminal in diction:
        firstSet = set()
        for rhs in diction[nonTerminal]:
            res = first(rhs)
            if res != None:
                if type(res) is list:
                    for firstTerm in res:
                        firstSet.add(firstTerm)
                else:
                    firstSet.add(res)
        firsts[nonTerminal] = firstSet


def computeAllFollows():
    for nonTerminal in diction:
        followSet = set()
        if follow(nonTerminal) is not None:
            for followTerm in follow(nonTerminal):
                followSet.add(followTerm)
        follows[nonTerminal] = followSet


def createPredictiveMatrix():
    # create matrix of row(nonTerminal) x [col(terminal) + 1($)]
    # create list of non-terminals
    nonTerminalList = list(diction.keys())
    terminals = copy.deepcopy(terminalsList)
    terminals.append('$')

    # create the initial empty state of matrix
    mat = []
    for nonTerminal in diction:
        row = []
        for terminal in terminals:
            row.append('')
        mat.append(row)

    # rules implementation
    for lhs in diction:
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)
            # empty is present, take union with follow
            if 'empty' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('empty')
                    res = list(res) + list(follows[lhs])
            # add rules to table
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = nonTerminalList.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] + f"{lhs}->{' '.join(y)}"

    return mat


def validateString(predictiveMatrix,
                   tableTermList, inputString,
                   terminalsList, startSymbol):

    stack = [startSymbol, '$']

    inputString = inputString.split()
    input = inputString + ['$']

    validationTable = PrettyTable()
    validationTable.field_names = ["Stack", "Input", "Action"]
    validationTable.align = "l"

    while True:
        # end loop if all symbols matched
        if stack == ['$'] and input == ['$']:
            action = "Valid"
            validationTable.add_row([stack, input, action])
            print(validationTable)
            return "\nValid String!"
        elif stack[0] not in terminalsList:
            # take font of input (y) and tos (x)
            x = list(diction.keys()).index(stack[0])
            y = tableTermList.index(input[0])
            if predictiveMatrix[x][y] != '':
                # format from predictiv matrix
                entry = predictiveMatrix[x][y]
                action = entry
                validationTable.add_row([stack, input, action])
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('empty', '').strip()
                entryRhs = lhs_rhs[1].split()
                stack = entryRhs + stack[1:]
            else:
                print(validationTable)
                return f"\nInvalid String! No rule at " \
                    f"predictiveMatrix[{stack[0]}][{input[0]}]."
        else:
            # stack top is Terminal
            if stack[0] == input[0]:
                action = "terminal"
                validationTable.add_row([stack, input, action])
                input = input[1:]
                stack = stack[1:]
            else:
                print(validationTable)
                return "\nInvalid String! " \
                    "Unmatched terminal symbols"


# Main
rules = ["S -> L d X",
         "X -> D",
         "L -> c a | a L",
         "D -> b | D e b"]

nonTerminalsList = ['S', 'L', 'X', 'D']
terminalsList = ['a', 'b', 'c', 'd', 'e']
inputString = "a a a a c a d e e b b b"

diction = {}
firsts = {}
follows = {}

parseGrammar(rules)

startSymbol = list(diction.keys())[0]

print(f"\nRules: \n")
for nonTerminal in diction:
    print(f"{nonTerminal}->{diction[nonTerminal]}")

print(f"\nAfter elimination of left recursion:\n")
diction = removeLeftRecursion(diction)
for nonTerminal in diction:
    print(f"{nonTerminal}->{diction[nonTerminal]}")

print("\nAfter left factoring:\n")
diction = leftFactoring(diction)
for nonTerminal in diction:
    print(f"{nonTerminal}->{diction[nonTerminal]}")

computeAllFirsts()
computeAllFollows()

print("\nFirst and Follow table\n")
ffTable = PrettyTable()
ffTable.field_names = ["", "FIRST", "FOLLOW"]
for u in diction:
    ffTable.add_row([u, str(firsts[u]), str(follows[u])])
ffTable.align = "l"
print(ffTable)

predictiveMatrixInfo = createPredictiveMatrix()
matrixTermminals = copy.deepcopy(terminalsList)
matrixTermminals.append('$')

print("\nGenerated predictive matrix:\n")
nonTerminalList = list(diction.keys())
predictiveMatrix = PrettyTable()
predictiveMatrix.field_names = [''] + matrixTermminals
j = 0
for y in predictiveMatrixInfo:
    rowComponents = [nonTerminalList[j]] + y
    predictiveMatrix.add_row(rowComponents)
    j += 1
predictiveMatrix.align = "l"
print(predictiveMatrix)

# validate string input using stack-input-action concept
print(f"\nValidate String: {inputString}\n")
validity = validateString(predictiveMatrixInfo, matrixTermminals,
                          inputString, terminalsList,
                          startSymbol)
print(validity)
