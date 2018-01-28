from fractions import Fraction
import math
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def normalizeFraction(f):
    return Fraction(f.numerator % f.denominator, f.denominator)


def simpleContinuedFraction(f):
    n = [0]
    b = f

    while b.numerator != 1:
        b = Fraction(1/b)
        n.append(int(math.floor(b.numerator/b.denominator)))
        b = normalizeFraction(b)

    n.append(b.denominator)
    return n


def fareySum(f1, f2):
    return Fraction(f1.numerator + f2.numerator, f1.denominator + f2.denominator)









while True:
    inp = input("Enter a fraction(as a/b): ")
    if re.match("[0-9]+\/[1-9][0-9]*", inp):
        break
    else:
        print("Wrong input.\n")

f = Fraction(int(inp.split('/')[0]), int(inp.split('/')[1]))

f = normalizeFraction(f)

print(simpleContinuedFraction(f))

n = simpleContinuedFraction(f)











'''
numOfNodes = 0
for val in n:
    numOfNodes += val

#adjMatrix = [[0 for x in range(numOfNodes)] for y in range(numOfNodes)]
'''



'''
G = nx.Graph()
numOfNodes = 0

for val in n:
    numOfNodes += val

secPrevNode = G.add_node(math.inf)
prevNode = G.add_node(Fraction(0, 1))

for i in range(numOfNodes - 1):
    G.add_node(-1)



currentNode = G.add_node(f)
#G.add_edge(math.inf, 0)

for i in range(numOfNodes-1):
    G.add_edge(prevNode, secPrevNode)
    G.add_edge(currentNode, prevNode)





#
for val in n:
    if val != 0:
        G.add_node(Fraction(1, val))
    else:
        G.add_node(val)
        G.add_edge(math.inf, val)




nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

'''