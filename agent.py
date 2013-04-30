#!/usr/bin/env python2

import sys

di = {'nw':0, 'n':1, 'ne':2, 'w':3, 'e':4, 'sw':5, 's':6, 'se':7}

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

    def probeRount(self, coor):
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

class func_logic():
    def __init__(self, logic_type=""):
        if not logic_type:
            pass
        else:
            self.type = logic_type
            self.child1 = func_logic()
            self.child2 = func_logic()

    def reval(self, coor):
        if self.type == 'and':
            return self.child1.reval(coor) and self.child2.reval(coor)
        elif self.type == 'or':
            return self.child1.reval(coor) or self.child2.reval(coor)
        elif self.type == 'not':
            return self.child1.reval(coor)

class func_if():
    def __init__(self):
        self.cond = func_logic()
        self.move1 = func_action()
        self.move2 = func_action()

    def eval(self, coor):
        if self.cond.reval(coor):
            self.move1.eval(coor)
        else:
            self.move2.eval(coor)

class func_action():
    def __init__(self, direction=""):
        self.dire = direction

    def eval(self, coor):
        if self.dire == 'north':
            coor[1]-=1
        elif self.dire == 'south':
            coor[1]+=1
        elif self.dire == 'west':
            coor[0]-=1
        elif self.dire == 'east':
            coor[0]+=1


class func_prob(func_logic):
    def __init__(self, direction):
        self.dire = direction

    def reval(self, coor):
        r = mat.probeRount(coor)
        return r.env[di[self.dire]]

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

def fitness_check(func, MeshMatrix):
    func.eval([3,3])

#def main():
    #pass

if __name__ == "__main__":
    mat = CreateMeshfromfile(sys.argv[1])
    n1 = func_logic('and')
    n2 = func_logic('or')
    n3 = func_logic('not')
    n4 = func_logic('and')
    n5 = func_logic('or')
    n6 = func_logic('not')
    n7 = func_logic('and')
    n8 = func_logic('or')
    n9 = func_logic('not')
    m1 = func_action('north')
    m2 = func_action('south')
    m3 = func_action('west')
    m4 = func_action('east')
    f1 = func_if()
    f2 = func_if()
    f3 = func_if()
    p1 = func_prob('n')
    p2 = func_prob('ne')
    p3 = func_prob('e')
    p4 = func_prob('e')
    p5 = func_prob('se')
    p6 = func_prob('s')
    p7 = func_prob('s')
    p8 = func_prob('sw')
    p9 = func_prob('w')
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
    fitness_check(f1,mat)

