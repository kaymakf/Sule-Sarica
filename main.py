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


def findThePath(n):
    G = nx.Graph()
    numOfNodes = 2

    for val in n:
        numOfNodes += val

    for i in range(-1, -numOfNodes - 1, -1):
        G.add_node(i)

    G.add_edge(-1, -2)

    c = -2
    i = 1
    while i < len(n):
        G.add_edge(c, c - n[i])
        c -= n[i]
        i += 1

    c = -3
    pb = -1
    b = -2
    for i in range(len(n) - 1):
        G.add_edge(pb, c)
        for j in range(n[i + 1] - 1):
            G.add_edge(c, b)
            G.add_edge(c, c + 1)
            G.add_edge(c, c - 1)
            c -= 1
        c -= 1
        pb = b
        b -= n[i + 1]

    G.nodes[-1]['value'] = math.inf
    G.nodes[-2]['value'] = Fraction(0, 1)
    G.nodes[-3]['value'] = Fraction(1, 1)

    for i in range(-4, -numOfNodes - 1, -1):
        adjList = sorted(list(G.neighbors(i)), reverse=True)
        G.nodes[i]['value'] = fareySum(G.nodes[adjList[0]]['value'], G.nodes[adjList[1]]['value'])

    if G.nodes[-numOfNodes]['value'] != f:
        print("something is wronh!!!")

    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.show()

    shortestPath = nx.dijkstra_path(G, -1, -numOfNodes)
    shortestPathValues = []

    for i in shortestPath:
        shortestPathValues.append(G.nodes[i]['value'])

    return shortestPathValues




while True:
    inp = input("Enter a fraction(as a/b): ")
    if re.match("[0-9]+\/[1-9][0-9]*", inp):
        break
    else:
        print("Wrong input.\n")

f = Fraction(int(inp.split('/')[0]), int(inp.split('/')[1]))
f = normalizeFraction(f)

#print(simpleContinuedFraction(f))

n = simpleContinuedFraction(f)

sp = findThePath(n)

#print(sp)




