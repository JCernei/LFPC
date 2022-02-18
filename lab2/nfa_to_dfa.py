from collections import OrderedDict
import pprint

def get_each_node_transactions(myNFA, newNode):
    nodeTransactions = []
    for node in newNode:
        nodeTransactions.append(myNFA[node])
    return nodeTransactions

def get_node_edges(nodeTransactions):
    nodeEdges = set()
    for transaction in nodeTransactions:
        nodeEdges = set.union(nodeEdges, transaction.keys())
    return nodeEdges

def get_unprocessed_nodes(myDFA, newNodeLabel):
    unprocessedNodes = []
    for edge in myDFA[newNodeLabel]:
        unprocessedNodes.append(myDFA[newNodeLabel][edge])
    return unprocessedNodes

def get_new_nodes(myDFA, unprocessedNodes):
    nodes = []
    for node in unprocessedNodes:
        label = ''.join(sorted(node))
        if label not in myDFA:
            nodes.append(node)
    return nodes

class NfaToDfa:
    def convert_to_DFA(myNFA):
        myDFA = OrderedDict()

        newNodes = [['q0']]
        step = 0

        while (len(newNodes) > 0):
            unprocessedNodes = []
            for newNode in newNodes:
                nodeTransactions = get_each_node_transactions(myNFA, newNode)
                                
                nodeEdges = get_node_edges(nodeTransactions)

                # get newNode destinations for each edge
                newNodeLabel = ''.join(sorted(newNode))
                myDFA[newNodeLabel] = {}
                for edge in nodeEdges:
                    myDFA[newNodeLabel][edge] = []
                    for transaction in nodeTransactions:
                        if edge in transaction:
                            myDFA[newNodeLabel][edge] += transaction[edge]
                
                unprocessedNodes += get_unprocessed_nodes(myDFA, newNodeLabel)
                
            newNodes = get_new_nodes(myDFA, unprocessedNodes)

            # print DFA step by step
            print(f"STEP {step}")
            pprint.pprint(myDFA)
            print(f"new nodes ={newNodes}:")
            print()
            step += 1 