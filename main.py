from fractions import Fraction
import math
import networkx as nx
import matplotlib.pyplot as plt

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










inp = input("Enter a fraction(as a/b): ")
f = Fraction(int(inp.split('/')[0]), int(inp.split('/')[1]))

f = normalizeFraction(f)

print(simpleContinuedFraction(f))

n = simpleContinuedFraction(f)

G = nx.Graph()
G.add_node(math.inf)
for val in n:
    if val != 0:
        G.add_node(Fraction(1, val))
    else:
        G.add_node(val)

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

