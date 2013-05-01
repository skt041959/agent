#!/usr/bin/env python2
#coding=utf8

import sys
import random

di = {'nw':0, 'n':1, 'ne':2, 'w':3, 'e':4, 'sw':5, 's':6, 'se':7}
MAX = 2

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
            self.env = p[:]
        else:
            self.nw = p1
            self.n = p2
            self.ne = p3
            self.w = p4
            self.e = p6
            self.sw = p7
            self.s = p8
            self.se = p9
            self.env = [p1,p2,p3,p4,p6,p7,p8,p9]

class Mesh():
    def __init__(self, length, width, MeshMatrix):
        self.l = length
        self.w = width
        self.m = MeshMatrix

    def probeRount(self):
        global coor
        x = coor[0]
        y = coor[1]
        t = [False for e in range(8)]
        for n,e in enumerate(([x-1,y-1], [x,y-1], [x+1,y-1], [x-1,y], [x+1,y], [x-1,y+1], [x,y+1], [x+1,y+1])):
            if e[0] < 0 or e[1] < 0:
                t[n] = False
            else:
                try:
                    t[n] = bool(self.m[e[0]][e[1]])
                except IndexError:
                    t[n] = False
        r = Round(t)
        return r
    def isEdge(self, c):
        pass

class func():
    def __init__(self):
        self.reval = None

class func_prob(func):
    def __init__(self, direction):
        self.dire = direction

    @property
    def reval(self):
        global coor
        global moved
        print "func_prob\n"
        if moved:
            r = mat.probeRount()
            moved = False
        if self.dire == "true":
            return True
        elif self.dire == "false":
            return False
        else:
            return r.env[di[self.dire]]

class func_logic():
    def __init__(self, logic_type=""):
        self.type = logic_type
        self.child1 = func()
        self.child2 = func()
        if self.type == 'and':
            self.reval = property(self.reval_and)
        elif self.type == 'or':
            self.reval = property(self.reval_or)
        elif self.type == 'not':
            self.reval = property(self.reval_not)
        elif self.type == 'branch':
            self.cond = func()
            self.reval = property(self.reval_branch)

    def reval_and(self):
        return self.child1.reval and self.child2.reval

    def reval_or(self):
        return self.child1.reval or self.child2.reval

    def reval_not(self):
        return not self.child1.reval

    def reval_branch(self):
        if self.cond.reval():
            return self.child1.reval
        else:
            return self.child2.reval

class func_branch():
    def __init__(self):
        self.cond = func()
        self.eval1 = func()
        self.eval2 = func()

    def reval(self, coor):
        print "func_branch\n"
        if self.cond.reval:
            self.eval1.reval(coor)
        else:
            self.eval2.reval(coor)

class func_move():
    def __init__(self, direction=""):
        self.dire = direction

    def reval(self, coor):
        print "func_action\n"
        if self.dire == 'north':
            coor[1]-=1
        elif self.dire == 'south':
            coor[1]+=1
        elif self.dire == 'west':
            coor[0]-=1
        elif self.dire == 'east':
            coor[0]+=1

def CreateMeshfromfile(filename):
    f = open(filename,'r')
    s = [list(e[:-1]) for e in f]
    w = len(s)
    l = len(s[0])
    for t in s:
        if len(t) == l:
            continue
        else:
            print 'please commit a valid mesh file\n'
            sys.exit()
    m = Mesh(l, w, s)
    return m

def fitness_check(root_func):
    global count
    global coor
    x = list()
    y = list()
    for i in range(10):
        x.append(random.randrange(0, mat.w))
        y.append(random.randrange(0, mat.l))
        for t in range(60):
            coor = [x,y]
            root_func.reval()
            if isEdge(coor):
                count+=1

def generate_random_branch(depth):
    r = func_branch()
    depth +=1
    r.eval1 = func_move(random.choice(directions))
    r.cond = generate_random_logic(depth)
    if depth < MAX and random.randrange(1):
        r.eval2 = generate_random_branch(depth)
    else:
        r.eval2 = func_move(random.choice(directions))

def generate_random_logic(depth):
    if depth < MAX:
        n1 = func_logic(random.choice(logics))
        if n1.type == "branch":
            depth+=1
            n1.cond = generate_random_logic(depth)
            n1.child1 = generate_random_logic(depth)
            n1.child2 = generate_random_logic(depth)
        elif n1.type == "and" or n1.type == "or":
            n1.child1 = generate_random_logic(depth)
            n1.child2 = generate_random_logic(depth)
        else:
            n1.child1 = generate_random_logic(depth)
    else:
        n1 = func_logic(random.choice(logics[:-1]))
        if n1.type == "and" or n1.type == "or":
            n1.child1 = generate_random_logic(depth)
            n1.child2 = generate_random_logic(depth)
        else:
            n1.child1 = generate_random_logic(depth)
    return n1

if __name__ == "__main__":
    mat = CreateMeshfromfile(sys.argv[1])
    moved = True
    p1 = func_prob('nw')
    p2 = func_prob('n')
    p3 = func_prob('ne')
    p4 = func_prob('w')
    p6 = func_prob('e')
    p7 = func_prob('sw')
    p8 = func_prob('s')
    p9 = func_prob('se')
    p_t = func_prob('true')
    p_f = func_prob('false')
    probs=[p1,p2,p3,p4,p6,p7,p8,p9,p_t,p_f]
    logics=['and', 'or', 'not', 'branch']
    directions=['east', 'west', 'south', 'north']
    orientations=['nw', 'n', 'ne', 's', 'e', 'sw', 's', 'se']

    for i in range(5000):
        count = 0
        root = generate_random_branch(0)
        fitness_check(root)

    n1 = func_logic('and')
    n2 = func_logic('or')
    n3 = func_logic('not')
    n4 = func_logic('and')
    n5 = func_logic('or')
    n6 = func_logic('not')
    n7 = func_logic('and')
    n8 = func_logic('or')
    n9 = func_logic('not')
    m1 = func_move('north')
    m2 = func_move('south')
    m3 = func_move('west')
    m4 = func_move('east')
    f1 = func_branch()
    f2 = func_branch()
    f3 = func_branch()
    f1.cond = n1
    n1.child1 = n2
    n2.child1 = p1
    n2.child2 = p2
    n1.child2 = n3
    n3.child1 = p3
    f1.move1 = m4
    f1.move2 = f2
    f2.cond = n4
    n4.child1 = n5
    n5.child1 = p4
    n5.child2 = p5
    n4.child2 = n6
    n6.child1 = p6
    f2.move1 = m2
    f2.move2 = f3
    f3.cond = n7
    n7.child1 = n8
    n8.child1 = p7
    n8.child2 = p8
    n7.child2 = p9
    f3.move1 = m3
    f3.move2 = m1

