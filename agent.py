#!/usr/bin/env python2
#coding=utf8

import sys
from random import randrange,choice
import pdb

di = {'nw':0, 'n':1, 'ne':2, 'w':3, 'e':4, 'sw':5, 's':6, 'se':7}
MAX = 3

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

    def probeRount(self,  coordinate):
        x = coordinate[0]
        y = coordinate[1]
        t = [False for e in range(8)]
        for n,e in enumerate(([x-1,y-1], [x,y-1], [x+1,y-1], [x-1,y], [x+1,y], [x-1,y+1], [x,y+1], [x+1,y+1])):
            if e[0] < 0 or e[1] < 0:
                t[n] = False
            else:
                try:
                    t[n] = bool(self.m[e[0]][e[1]])
                except IndexError:
                    t[n] = False
        r = Round(p=t)
        return r

    def isEdge(self, coordinate):
        r = self.probeRount(coordinate)
        return bool([e for e in r.env if not e])

    def outofEdge(self, coordinate):
        if coordinate[0]<0 or coordinate[0]>=self.l or coordinate[1]<0 or coordinate[1]>=self.w:
            return True

class func():
    def __init__(self):
        self.reval = None

class func_prob(func):
    def __init__(self, direction):
        self.dire = direction

    @property
    def reval(self):
        #global coor
        print >> sys.stderr, "%s" %self.dire
        if self.dire == "true":
            return True
        elif self.dire == "false":
            return False
        r = mat.probeRount(coor)
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

    def __getitem__(self, key):
        if self.type == "not" and key >= 1:
            raise IndexError
        elif key == 2 and not self.type == "branch":
            raise IndexError
        elif key >= 3:
            raise IndexError
        if key == 0:
            return self.child1
        if key == 1:
            return self.child2
        if key == 2:
            return self.cond

    def reval_and(self):
        print >> sys.stderr, "%s" %self.type
        return self.child1.reval and self.child2.reval

    def reval_or(self):
        print >> sys.stderr, "%s" %self.type
        return self.child1.reval or self.child2.reval

    def reval_not(self):
        print >> sys.stderr, "%s" %self.type
        return not self.child1.reval

    def reval_branch(self):
        print >> sys.stderr, "%s" %self.type
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
        if self.cond.reval:
            return self.eval1.reval(coor)
        else:
            return self.eval2.reval(coor)

    def __getitem__(self, key):
        if key >= 3:
            raise IndexError
        if key == 0:
            return self.cond
        if key == 1:
            return self.child1
        if key == 2:
            return self.child2

class func_move():
    def __init__(self, direction=""):
        self.dire = direction

    def reval(self, coor):
        print >> sys.stderr, "%s" %self.dire
        if self.dire == 'north':
            coor[1]-=1
            if mat.outofEdge(coor):
                return False
        elif self.dire == 'south':
            coor[1]+=1
            if mat.outofEdge(coor):
                return False
        elif self.dire == 'west':
            coor[0]-=1
            if mat.outofEdge(coor):
                return False
        elif self.dire == 'east':
            coor[0]+=1
            if mat.outofEdge(coor):
                return False
        print >> sys.stderr, coor
        return True

def generate_random_branch(depth):
    r = func_branch()
    print >> sys.stderr, "\t"*(depth+1)+"if"
    depth +=1
    r.eval1 = func_move(choice(directions))
    r.cond = generate_random_logic(depth)
    if depth < MAX and randrange(2):
        r.eval2 = generate_random_branch(depth)
    else:
        r.eval2 = func_move(choice(directions))
    return r

def generate_random_logic(depth):
    if randrange(5):
        return func_prob(choice(orientations))
    if depth < MAX:
        n1 = func_logic(choice(logics))
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
        n1 = func_logic(choice(logics[:-1]))
        if n1.type == "and" or n1.type == "or":
            n1.child1 = generate_random_logic(depth)
            n1.child2 = generate_random_logic(depth)
        else:
            n1.child1 = generate_random_logic(depth)
    return n1

def CreateMeshfromfile(filename):
    f = open(filename,'r')
    s = [list(e[:-1]) for e in f]
    w = len(s)
    l = len(s[0])
    if [t for t in s if len(t) != l]:
        print >> sys.stderr, 'please commit a valid mesh file'
        sys.exit()
    m = Mesh(l, w, s)
    return m

def cross(p1, p2):
    stack_p1=[]
    stack_p2=[]

    nt = p1
    t=-1
    pt1 = None
    pt2 = None
    while stack_p1 or nt is p1:
        if not isinstance(nt, func_prob) and not isinstance(nt, func_move):
            if not randrange(10):
                pt2 = nt
                break
            stack_p1.append(nt)
            try:
                t+=1
                nt = nt[t]
            except IndexError:
                nt = stack_p1.pop()
                t = -1
        else:
            if randrange(1):
                pt1 = nt
                break
            nt = stack_p1.pop()
            t = -1
    nt = p2
    t=-1
    while stack_p2 or nt is p2:
        if not isinstance(nt, func_prob):
            if not randrange(10):
                pt2 = stack_p2.pop()
                break
            stack_p1.append(nt)
            try:
                t+=1
                nt = nt[t]
            except IndexError:
                nt = stack_p1.pop()
                t = -1
        else:
            if randrange(1):
                pt2 = nt
                break
            nt = stack_p1.pop()
            t = -1
    pt2[t]=pt1

def fitness_check(root_func):
    global coor
    coors = list()
    count = 0
    #the program will be checked for 10 times
    for i in range(10):
        print >> sys.stderr, "---"
        _x = 0
        _y = 0
        while mat.isEdge([_x,_y]):
            _x = randrange(mat.w)
            _y = randrange(mat.l)
            print >> sys.stderr, _x,_y
        coors.append([_x,_y])
        accessed = list()
        #the program will be run for 60 steps
        for t in range(60):
            print >> sys.stderr, '===='
            coor = coors[-1]
            if not root_func.reval(coor):
                break
            if mat.isEdge(coor):
                try:
                    accessed.index(coor)
                except ValueError:
                    accessed.append(coor)
        count+=len(accessed)
    return count

def main():
    generation_0_list=[]
    generation_0_list.append({"fitness":0, "root":None})

    for i in range(5000):
        root = generate_random_branch(0)
        fitness = fitness_check(root)
        print >> sys.stderr, "%d:fitness %d\n" %(i, fitness)
        for n,e in enumerate(generation_0_list):
            if fitness > e["fitness"]:
                generation_0_list.insert(n,{"fitness":fitness, "root":root})
                break
        print len(generation_0_list)

if __name__ == "__main__":
    mat = CreateMeshfromfile(sys.argv[1])

    logics=['and', 'or', 'not', 'branch']
    directions=['east', 'west', 'south', 'north']
    orientations=['nw', 'n', 'ne', 's', 'e', 'sw', 's', 'se', 'false', 'true']
    main()

    #n1 = func_logic('and')
    #n2 = func_logic('or')
    #n3 = func_logic('not')
    #n4 = func_logic('and')
    #n5 = func_logic('or')
    #n6 = func_logic('not')
    #n7 = func_logic('and')
    #n8 = func_logic('or')
    #n9 = func_logic('not')
    #m1 = func_move('north')
    #m2 = func_move('south')
    #m3 = func_move('west')
    #m4 = func_move('east')
    #f1 = func_branch()
    #f2 = func_branch()
    #f3 = func_branch()
    #f1.cond = n1
    #n1.child1 = n2
    #n2.child1 = p1
    #n2.child2 = p2
    #n1.child2 = n3
    #n3.child1 = p3
    #f1.move1 = m4
    #f1.move2 = f2
    #f2.cond = n4
    #n4.child1 = n5
    #n5.child1 = p4
    #n5.child2 = p5
    #n4.child2 = n6
    #n6.child1 = p6
    #f2.move1 = m2
    #f2.move2 = f3
    #f3.cond = n7
    #n7.child1 = n8
    #n8.child1 = p7
    #n8.child2 = p8
    #n7.child2 = p9
    #f3.move1 = m3
    #f3.move2 = m1

