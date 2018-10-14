import math
import re
import tkinter as tk
from fractions import Fraction

import networkx as nx
import pygubu
from sympy import Symbol
from sympy import sympify
from sympy.solvers import solve
# import matplotlib.pyplot as plt


def normalizeFraction(f):
    if f.numerator % f.denominator != 0:
        return Fraction(f.numerator % f.denominator, f.denominator)
    else:
        return Fraction(1, 1)


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

#    labels = nx.get_node_attributes(G, 'value')

    for i in range(-4, -numOfNodes - 1, -1):
        adjList = sorted(list(G.neighbors(i)), reverse=True)
        G.nodes[i]['value'] = fareySum(G.nodes[adjList[0]]['value'], G.nodes[adjList[1]]['value'])

#    if G.nodes[-numOfNodes]['value'] != f:
#        print("something is wronh!!!")

#    nx.draw(G, with_labels=True, labels=labels, font_weight='bold')
#    plt.show()

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

wordStr = ""


def getTheWord(c, TorR):
    def blockformToString(b):
        s = ['\u2070', '\u00B9', '\u00B2', '\u00B3', '\u2074', '\u2075', '\u2076', '\u2077', '\u2078', '\u2079']
        r = ""

        def exponent(a1):
            h = ""
            if a1 > 1:
                exp = []
                if a1 > 9:
                    for step in str(a1):
                        exp.append(int(step))
                else:
                    exp.append(a1)

                for w in exp:
                    h += s[w]
            return h

        for a in b:
            if a[0] == 'TSS':
                r += '(TS' + s[2] + ')'
            elif a[0] == 'TS':
                r += '(' + a[0] + ')'
            else:
                r += a[0]

            r += exponent(a[1]) + ' '

        return r

    global wordStr

    word = [("TS", int(c[0] - 1))]

    for i in range(1, len(c) - 1):
        word.append(("TSS", 1))
        word.append(("TS", int(c[i] - 2)))

    word.append(("TSS", 1))
    word.append(("TS", int(c[len(c) - 1] - 1)))
    word.append((TorR, 1))

    newWord = ""
    for w in word:
        if w[1] >= 0:
            for j in range(w[1]):
                newWord += w[0]
        elif w[0] == "TS":
            for j in range(-w[1]):
                newWord += "SST"

#    print("\t" + str(word))

    oldWord = ""
    while oldWord != newWord:
        oldWord = newWord
        newWord = newWord.replace("SSS", "").replace("TT", "")

    i=0
    blockform=[]

    while i < len(newWord):
        if i+3 > len(newWord):
            break
        else:
            temp = newWord[i : i+3]

            if temp == 'TSS':
                j = 3
                count = 1
                while newWord[i+j : i+j+3] == 'TSS':
                    count += 1
                    j+=3
                blockform.append(('TSS', count))
                i += j

            else:
                j = 2
                count = 1
                while newWord[i+j : i+j+2] == 'TS' and newWord[i+j+2] != 'S':
                    count += 1
                    j+=2
                blockform.append(('TS', count))
                i += j

    while i < len(newWord):
        blockform.append((newWord[i], 1))
        i += 1

    wordStr += "\n" + blockformToString(blockform)


    newWord = newWord.replace("TSS", "Rh").replace("TS", "Rf")

    newWord = newWord.replace("RhR", "f").replace("RfR", "h")


    while newWord.count('R') > 1:
        newWord = newWord.replace("Rh", "fR").replace("Rf", "hR").replace("RT", "TR").replace("RR", "")

    if newWord.count('R') == 1:
        if newWord.count("Rh") == 1:
            newWord = newWord.replace("Rh", "fR")
        elif newWord.count("Rf") == 1:
            newWord = newWord.replace("Rf", "hR")

#    print("\t" + str(newWord))

    x = []
    i=0
    while i < len(newWord):
        letter = newWord[i]
        j=1
        if i+j < len(newWord):
            while (i+j) < len(newWord) and newWord[i+j] == letter:
                j+=1

        x.append((newWord[i], j))
        i += j

#    print("\t" + str(x))

    wordStr += "\n" + blockformToString(x) + '\n'

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
            m.append([[0, -1],
                     [1, 0]])

        elif w[0] == 'R':
            m.append([[0, 1],
                     [1, 0]])

    return m

pathsStr = ""
ICFStr = ""


def pathToString(p):
    a = ""
    r = ""
    for i in range(len(p)):
        if type(p[i]) is Fraction:
            a = str(Fraction(p[i]).numerator) + '/' + str(Fraction(p[i]).denominator)
        elif p[i] == math.inf:
            a = "\u221E"
        r += a if i == len(p) - 1 else a + ",  "
    r += "\n"

    return r


def calculate(f, TorR):
    global pathsStr
    global ICFStr
    global wordStr

#    f = normalizeFraction(f)
    n = simpleContinuedFraction(f)
#    print("basit sürekli kesir: " + str(n))

    sp = findThePath(n)

    pathsStr = ""
    ICFStr = ""

    if TorR == 'R':
        for p in sp: pathsStr += pathToString(p)

    '''
    for i in range(len(sp)):
        c = integerContinuedFraction(sp[i])
        for s in c:
            print(s, end='  ')
        print()
    '''

    c1 = integerContinuedFraction(sp[0])
#    print(str(sp[0]) + " için;\n\ttamsayı sürekli kesir: " + str(c1))
    if TorR == 'R':
        ICFStr += "For the path (" + (pathToString(sp[0]).split("\n"))[0] + "):\n" + str([int(c) for c in c1]) + "\n"
        wordStr += "\nAnti Automorphism:\n"
    elif TorR == 'T':
        wordStr += "\nAutomorphism:\n"

    word1 = getTheWord(c1, TorR)

#    print(word1)

    m = []
    m.append(getTheMatrix(word1))

    if len(sp) > 1:
        i = 1
        while i < len(sp) and sp[0][len(sp[0]) - 2] == sp[i][len(sp[i]) - 2]:
            i += 1
        if i == len(sp):
            i -= 1
        c2 = integerContinuedFraction(sp[i])
#        print(str(sp[i]) + " için;\n\ttamsayı sürekli kesir: " + str(c2))
        if TorR == 'R': ICFStr += "\nFor the path (" + (pathToString(sp[i]).split("\n"))[0] + "):\n" + str([int(c) for c in c2]) + "\n"

        word2 = getTheWord(c2, TorR)

#        print(word2)

        m.append(getTheMatrix(word2))

#    print()
#    for n in m[0]:
#        print(str(n[0]) + "\n" + str(n[1]) + "\n")

    return m


def matrixToString(m):
    r = ""

    for i in range(len(m[0][0])):
        for j in range(len(m[0])):
            r += str(m[0][j][i]) + "\t"
        r += "\n"

    r += "\n\n"
    if len(m) > 1:
        for i in range(len(m[1][0])):
            for j in range(len(m[1])):
                r += str(m[1][j][i]) + "\t"
            r += "\n"

    return r


def onclick():
    global inp
    global out
    global pathsStr
    global ICFStr
    global wordStr

    wordStr = ""

    if re.match("-*[0-9]+\/[1-9][0-9]*", inp.get()):
        f = Fraction(int(inp.get().split('/')[0]), int(inp.get().split('/')[1]))

        if 0 < f <= 1:
            result = ""

            result += "Automorphism:\n"
            result += matrixToString(calculate(f, "T"))

            result += "\n\nAnti Automorphism:\n"
            result += matrixToString(calculate(f, "R"))

            outPaths.set(pathsStr)
            outICF.set(ICFStr)
            outWord.set(wordStr)

            out.set(result)

        else:
            outPaths.set("Input must be between 0 and 1.")
            outICF.set("Input must be between 0 and 1")
            outWord.set("Input must be between 0 and 1")
            out.set("Input must be between 0 and 1")

    else:
        outPaths.set("Wrong input")
        outICF.set("Wrong input")
        outWord.set("Wrong input")
        out.set("Wrong input")


class Application(pygubu.TkApplication):
    def _create_ui(self):
        global inp
        global out
        global outPaths
        global outICF
        global outWord
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ui.xml')
        self.mainwindow = builder.get_object('container', self.master)
        builder.connect_callbacks({'onClick': onclick})
        self.set_title("")
        self.set_resizable()
        inp = builder.get_variable('inp')
        out = builder.get_variable('out')
        outPaths = builder.get_variable('outPaths')
        outICF = builder.get_variable('outICF')
        outWord = builder.get_variable('outWord')

    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    inp = tk.StringVar()
    out = tk.StringVar()
    outPaths = tk.StringVar()
    outICF = tk.StringVar()
    outWord = tk.StringVar()

    app = Application(root)
    app.run()