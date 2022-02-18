from fin_aut_parser import FinAutParser
from nfa_to_dfa import NfaToDfa
import pprint

# Parse NFA from file
myNFA = FinAutParser.parseNFA("NFA_variant_8.txt")

print('NFA:')
pprint.pprint(myNFA)

print()

print('DFA conversion:')
myDFA = NfaToDfa.convert_to_DFA(myNFA)
