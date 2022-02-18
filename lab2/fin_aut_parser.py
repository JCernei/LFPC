import re

class FinAutParser:
    def parseNFA(filename):
        myNFA = dict()
        lines = []
        with open(filename) as f:
            lines = f.read().splitlines()[4:]

        for line in lines:
            parts = re.split('[d,()= ]', line)
            node1, edge, node2 = list(filter(None, parts))
            
            if node1 in myNFA:
                if edge in myNFA[node1]:
                    myNFA[node1][edge].append(node2)
                else:
                    myNFA[node1][edge] = [node2]
            else:
                myNFA[node1] = {edge: [node2]}
        return myNFA

