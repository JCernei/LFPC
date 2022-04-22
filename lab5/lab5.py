from prettytable import PrettyTable
import copy


def parseGrammar(rules):
    for rule in rules:
        k = rule.split("->")
        # remove un-necessary spaces
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        # remove un-necessary spaces
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs


def removeLeftRecursion(rulesDiction):
    store = {}
    # traverse over rules
    for lhs in rulesDiction:
        # alphaRules stores subrules with left-recursion
        # betaRules stores subrules without left-recursion
        alphaRules = []
        betaRules = []
        # get rhs for current lhs
        allrhs = rulesDiction[lhs]
        for subrhs in allrhs:
            if subrhs[0] == lhs:
                alphaRules.append(subrhs[1:])
            else:
                betaRules.append(subrhs)
        # alpha and beta containing subrules are separated
        # now form two new rules
        if len(alphaRules) != 0:
            # to generate new unique symbol
            # add ' till unique not generated
            lhs_ = lhs + "'"
            while (lhs_ in rulesDiction.keys()) \
                    or (lhs_ in store.keys()):
                lhs_ += "'"
            # make beta rule
            for b in range(0, len(betaRules)):
                betaRules[b].append(lhs_)
            rulesDiction[lhs] = betaRules
            # make alpha rule
            for a in range(0, len(alphaRules)):
                alphaRules[a].append(lhs_)
            alphaRules.append(['empty'])
            # store in temp dict, append to
            # - rulesDiction at end of traversal
            store[lhs_] = alphaRules
    # add newly generated rules generated
    # - after removing left recursion
    for left in store:
        rulesDiction[left] = store[left]
    return rulesDiction


def leftFactoring(rulesDiction):
    newDict = {}
    # iterate over all rules of dictionary
    for lhs in rulesDiction:
        # get rhs for given lhs
        allrhs = rulesDiction[lhs]
        # temp dictionary helps detect left factoring
        temp = dict()
        for subrhs in allrhs:
            if subrhs[0] not in list(temp.keys()):
                temp[subrhs[0]] = [subrhs]
            else:
                temp[subrhs[0]].append(subrhs)
        # if value list count for any key in temp is > 1,
        # - it has left factoring
        # new_rule stores new subrules for current LHS symbol
        new_rule = []
        # temp_dict stores new subrules for left factoring
        tempo_dict = {}
        for term_key in temp:
            # get value from temp for term_key
            allStartingWithTermKey = temp[term_key]
            if len(allStartingWithTermKey) > 1:
                # left factoring required
                # to generate new unique symbol
                # - add ' till unique not generated
                lhs_ = lhs + "'"
                while (lhs_ in rulesDiction.keys()) \
                        or (lhs_ in tempo_dict.keys()):
                    lhs_ += "'"
                # append the left factored result
                new_rule.append([term_key, lhs_])
                # add expanded rules to tempo_dict
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            else:
                # no left factoring required
                new_rule.append(allStartingWithTermKey[0])
        # add original rule
        newDict[lhs] = new_rule
        # add newly generated rules after left factoring
        for key in tempo_dict:
            newDict[key] = tempo_dict[key]
    return newDict


def first(rule):
    # recursion base condition
    # (for terminal or epsilon)
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == 'empty':
            return 'empty'

    # condition for Non-Terminals
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            # fres temporary list of result
            fres = []
            rhs_rules = diction[rule[0]]
            # call first on each rule of RHS
            # fetched (& take union)
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            # if no epsilon in result
            # - received return fres
            if 'empty' not in fres:
                return fres
            else:
                # apply epsilon
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                fres.remove('empty')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                # if result is not already returned
                # - control reaches here
                # lastly if eplison still persists
                # - keep it in result of first
                fres.append('empty')
                return fres


def follow(nonTerminal):
    # for start symbol return $ (recursion base case)
    solset = set()
    if nonTerminal == start_symbol:
        # return '$'
        solset.add('$')

    # check all occurrences
    # solset - is result of computed 'follow' so far

    # For input, check in all rules
    for curNT in diction:
        rhs = diction[curNT]
        # go for all productions of NT
        for subrule in rhs:
            if nonTerminal in subrule:
                # call for all occurrences on
                # - non-terminal in subrule
                while nonTerminal in subrule:
                    index_nt = subrule.index(nonTerminal)
                    subrule = subrule[index_nt + 1:]
                    # empty condition - call follow on LHS
                    if len(subrule) != 0:
                        # compute first if symbols on
                        # - RHS of target Non-Terminal exists
                        res = first(subrule)
                        # if epsilon in result apply rule
                        # - (A->aBX)- follow of -
                        # - follow(B)=(first(X)-{ep}) U follow(A)
                        if 'empty' in res:
                            newList = []
                            res.remove('empty')
                            ansNew = follow(curNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        # when nothing in RHS, go circular
                        # - and take follow of LHS
                        # only if (NT in LHS)!=curNT
                        if nonTerminal != curNT:
                            res = follow(curNT)

                    # add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)


def computeAllFirsts():
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        # save result in 'firsts' list
        firsts[y] = t


def computeAllFollows():
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset


def createParseTable():
    print("\nFirst and Follow table\n")
    ffTable = PrettyTable()
    ffTable.field_names = ["", "FIRST", "FOLLOW"]
    for u in diction:
        ffTable.add_row([u, str(firsts[u]), str(follows[u])])
    ffTable.align = "l"
    print(ffTable)

    # create matrix of row(NT) x [col(T) + 1($)]
    # create list of non-terminals
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    terminals.append('$')

    # create the initial empty state of ,matrix
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        # of $ append one more col
        mat.append(row)

    # Classifying grammar as LL(1) or not LL(1)
    grammar_is_LL = True

    # rules implementation
    for lhs in diction:
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)
            # epsilon is present,
            # - take union with follow
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
                    res = list(res) +\
                        list(follows[lhs])
            # add rules to table
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] \
                        + f"{lhs}->{' '.join(y)}"
                else:
                    # if rule already present
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] \
                            + f",{lhs}->{' '.join(y)}"

    # print parsing table
    space = ['']
    print("\nGenerated parsing table:\n")
    parsingTable = PrettyTable()
    parsingTable.field_names = space + terminals
    j = 0
    for y in mat:
        rowComponents = [ntlist[j]] + y
        parsingTable.add_row(rowComponents)
        j += 1
    parsingTable.align = "l"
    print(parsingTable)
    return (mat, grammar_is_LL, terminals)


def validateStringUsingStackBuffer(parsing_table, grammarll1,
                                   table_term_list, input_string,
                                   term_userdef, start_symbol):

    print(f"\nValidate String: {input_string}\n")

    # for more than one entries
    # - in one cell of parsing table
    if grammarll1 == False:
        return f"\nInput String = " \
            f"\"{input_string}\"\n" \
            f"Grammar is not LL(1)"

    # implementing stack input
    stack = [start_symbol, '$']

    # reverse input string store in input
    input_string = input_string.split()
    input_string.reverse()
    input = ['$'] + input_string

    validationTable = PrettyTable()
    validationTable.field_names = ["Stack", "Input", "Action"]
    validationTable.align = "l"

    while True:
        # end loop if all symbols matched
        if stack == ['$'] and input == ['$']:
            action = "Valid"
            validationTable.add_row([stack, input, action])
            return print(validationTable), "\nValid String!"
        elif stack[0] not in term_userdef:
            # take font of input (y) and tos (x)
            x = list(diction.keys()).index(stack[0])
            y = table_term_list.index(input[-1])
            if parsing_table[x][y] != '':
                # format table entry received
                entry = parsing_table[x][y]
                action = f"T[{stack[0]}][{input[-1]}] = {entry}"
                validationTable.add_row([stack, input, action])
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('empty', '').strip()
                entryrhs = lhs_rhs[1].split()
                stack = entryrhs + stack[1:]
            else:
                return print(validationTable), f"\nInvalid String! No rule at " \
                    f"Table[{stack[0]}][{input[-1]}]."
        else:
            # stack top is Terminal
            if stack[0] == input[-1]:
                action = f"Matched:{stack[0]}"
                validationTable.add_row([stack, input, action])
                input = input[:-1]
                stack = stack[1:]
            else:
                return print(validationTable), "\nInvalid String! " \
                    "Unmatched terminal symbols"


# DRIVER CODE - MAIN
sample_input_string = None

rules = ["S -> L d X",
         "X -> D",
         "L -> c a | a L",
         "D -> b | D e b"]

nonterm_userdef = ['S', 'L', 'X', 'D']
term_userdef = ['a', 'b', 'c', 'd', 'e']
sample_input_string = "a a a a c a d e e b b b"

diction = {}
firsts = {}
follows = {}

parseGrammar(rules)

print(f"\nRules: \n")
for y in diction:
    print(f"{y}->{diction[y]}")

print(f"\nAfter elimination of left recursion:\n")
diction = removeLeftRecursion(diction)
for y in diction:
    print(f"{y}->{diction[y]}")

print("\nAfter left factoring:\n")
diction = leftFactoring(diction)
for y in diction:
    print(f"{y}->{diction[y]}")

# computes all FIRSTs for all non terminals
computeAllFirsts()

# assuming first rule has start_symbol
# start symbol can be modified in below line of code
start_symbol = list(diction.keys())[0]

# computes all FOLLOWs for all occurrences
computeAllFollows()

# generate formatted first and follow table
# then generate parse table
(parsing_table, result, tabTerm) = createParseTable()

# validate string input using stack-buffer concept
if sample_input_string != None:
    validity = validateStringUsingStackBuffer(parsing_table, result,
                                              tabTerm, sample_input_string,
                                              term_userdef, start_symbol)
    print(validity)
else:
    print("\nNo input String detected")
