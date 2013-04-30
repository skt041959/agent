#!/usr/bin/env python2

import sys

class Round():
    def __init__(self, p1=False, p2=False, p3=False, p4=False, p6=False, p7=False, p8=False, p9=False, p=[]):
        if p:
            self.nw = p[0]
            self.n = p[1]
            self.ne = p[2]
            self.w = p[3]
            self.e = p[4]
            self.sw = p[5]
            self.s = p[6]
        else:
            self.nw = p1
            self.n = p2
            self.ne = p3
            self.w = p4
            self.e = p6
            self.sw = p7
            self.s = p8
            self.se = p9

class Mesh():
    def __init__(self, length, width, MeshMatrix):
        self.l = length
        self.w = width
        self.m = MeshMatrix

    def probeRount(self, coor):
        x = coor[0]
        y = coor[1]
        t = [False for e in range(8)]
        for n,e in enumerate(([x-1,y-1], [x,y-1], [x+1,y-1], [x-1,y], [x+1,y], [x-1,y+1], [x,y+1], [x+1,y+1])):
            if e[0] < 0 or e[1] < 0:
                t[n] = False
            else:
                try:
                    t[n] = bool(self.m[e[0], e[1]])
                except IndexError:
                    t[n] = False
        r = Round(t)
        return r

class func():
    def __init__(self, n):
        self.name = n
        self.child1 = func()
        self.child2 = func()

class func_and(func):
    def __init__(self):
        func.__init__("and")

    def reval():
        return child1.reval() and child2.reval()

class func_or(func):
    def __init__(self):
        func.__init__("or")

    def reval():
        return child1.reval() or child2.reval()

class func_not(func):
    def __init__(self):
        func.__init__("not")

    def reval():
        return not child1.reval()

class func_if(func):
    def __init__(self):
        func.__init__("if")
        self.move1 = action()
        self.move2 = action()

def CreateMeshfromfile(filename):
    f = open(filename,'r')
    s = [list(e[:-1]) for e in f]
    w = len(s)
    l = len(s[0])
    for t in s:
        if len(t) == l:
            continue
        else:
            print "please commit a valid mesh file\n"
            sys.exit()
    m = Mesh(l, w, s)
    return m

def fitness_check(func, MeshMatrix):

def main():
    mat = CreateMeshfromfile(sys.argv[1])

if __name__ == "__main__":
    main()
