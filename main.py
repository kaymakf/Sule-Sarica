from fractions import Fraction
import math
import networkx as nx
#import matplotlib.pyplot as plt

from sympy.solvers import solve
from sympy import Symbol
from sympy import sympify

from tkinter import *
from tkinter import ttk


def normalizeFraction(f):
    return Fraction(f.numerator % f.denominator, f.denominator)

def fib(n):
    if n == 0: return 0
    if n == 1 or n == 2: return 1
    return fib(n-1) + fib(n-2)

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

    #labels = nx.get_node_attributes(G, 'value')

    for i in range(-4, -numOfNodes - 1, -1):
        adjList = sorted(list(G.neighbors(i)), reverse=True)
        G.nodes[i]['value'] = fareySum(G.nodes[adjList[0]]['value'], G.nodes[adjList[1]]['value'])

    #if G.nodes[-numOfNodes]['value'] != f:
    #    print("something is wronh!!!")

    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.show()

    shortestPaths = list(nx.all_shortest_paths(G, -1, -numOfNodes))
    shortestPathValues = []
    spaths = []

    for j in range(len(shortestPaths)):
        for i in shortestPaths[j]:
            shortestPathValues.append(G.nodes[i]['value'])
        spaths.append(shortestPathValues.copy())
        shortestPathValues.clear()

    return spaths

def integerContinuedFraction(p):
    c = [p[1]]
    x = Symbol('x')
    for i in range(1, len(p)-1):
        eq = "(" + str(c[0])
        for j in range(1, i):
            eq += "-(1/(" + str(c[j])
        eq += "-(1/(x"
        for k in range(2*i+1): eq += ")"
        eq += "-(" + str(p[i+1]) + ")"
        eq = sympify(eq)
        c.append(list(solve(eq, x)).pop())

    return c

def getTheWord(c):
    word = [("TS", int(c[0] - 1))]

    for i in range(1, len(c) - 1):
        word.append(("TSS", 1))
        word.append(("TS", int(c[i] - 2)))

    word.append(("TSS", 1))
    word.append(("TS", int(c[len(c) - 1] - 1)))
    word.append(("R", 1))

    newWord = ""
    for w in word:
        if w[1] >= 0:
            for j in range(w[1]):
                newWord += w[0]
        elif w[0] == "TS":
            for j in range(-w[1]):
                newWord += "SST"

#    print(word)
#    print(newWord)

    oldWord = ""
    while oldWord != newWord:
        oldWord = newWord
        newWord = newWord.replace("SSS", "").replace("TT", "")

#    print(newWord)

    newWord = newWord.replace("TSS", "Rh").replace("TS", "Rf")
#    print(newWord)
    newWord = newWord.replace("RhR", "f").replace("RfR", "h")
#    print(newWord)

    while newWord.count('R') > 1:
        newWord = newWord.replace("Rh", "fR").replace("Rf", "hR").replace("RT", "TR").replace("RR", "")

#    print(newWord)

    x = []
    i=0
    while i < len(newWord):
        letter = newWord[i]
        j=1
        if i+j < len(newWord):
            while newWord[i+j] == letter:
                j+=1

        x.append((newWord[i], j))
        i += j

#    print(x)

    return x

def getTheMatrix(word):
    m = []
    for w in word:
        if w[0] == 'f':
            m.append([[fib(w[1] - 1), fib(w[1])],
                     [fib(w[1]), fib(w[1] + 1)]])

        elif w[0] == 'h':
            m.append([[fib(w[1] + 1), fib(w[1])],
                     [fib(w[1]), fib(w[1] - 1)]])

        elif w[0] == 'T':
            m.insert(0, ['T', ''])

    return m


def calculate(f):
    f = normalizeFraction(f)

#    print(simpleContinuedFraction(f))

    n = simpleContinuedFraction(f)

    sp = findThePath(n)

    '''
    for s in sp:
        print(s)

    for i in range(len(sp)):
        c = integerContinuedFraction(sp[i])
        for s in c:
            print(s, end='  ')
        print()
    '''

    c1 = integerContinuedFraction(sp[0])
    word1 = getTheWord(c1)
    m = []
    m.append(getTheMatrix(word1))

    if len(sp) > 1:
        i = 1
        while sp[0][len(sp[0]) - 2] == sp[i][len(sp[i]) - 2]:
            i += 1
        c2 = integerContinuedFraction(sp[i])
        word2 = getTheWord(c2)
        m.append(getTheMatrix(word2))

#    print()
#    for n in m[0]:
#        print(str(n[0]) + "\n" + str(n[1]) + "\n")

    return m


def onclick(*args):
    if re.match("[0-9]+\/[1-9][0-9]*", inp.get()):
        f = Fraction(int(inp.get().split('/')[0]), int(inp.get().split('/')[1]))
        m = calculate(f)
        result = ""

        for i in range(len(m[0][0])):
            for j in range(len(m[0])):
                result += str(m[0][j][i]) + "\t"
            result += "\n"

        result += "\n\n"
        if len(m) > 1:
            for i in range(len(m[1][0])):
                for j in range(len(m[1])):
                    result += str(m[1][j][i]) + "\t"
                result += "\n"

        out.set(result)

    else:
        out.set("Wrong input")



root = Tk()
#root.title("MERHABA ŞULE HANIM")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

inp = StringVar()
out = StringVar()

inputF = ttk.Entry(mainframe, width=4, textvariable=inp)
inputF.grid(column=3, row=1, sticky=(W, E))


ttk.Label(mainframe, textvariable=out).grid(column=1, row=2, sticky=(W, E, S))
ttk.Button(mainframe, text="Hesapla", command=onclick).grid(column=4, row=1, sticky=W)

ttk.Label(mainframe, text="Bir kesir girin (a/b): ").grid(column=1, row=1, sticky=W)
#ttk.Label(mainframe, text="Result: ").grid(column=1, row=2, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

inputF.focus()
root.bind('<Return>', onclick)

root.mainloop()