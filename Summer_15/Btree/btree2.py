# Based on C++ implementation here:
# http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/
# Probably could be much better, but
from _bisect import *
import random


class BTreeNode(object):
    def __init__(self,t,leaf):
        self.t = t                               # Minimum degree (defines the range for number of keys)
        self.keys = []                           # An array of keys and children
        self.children = []
        self.leaf = leaf                         # Leaf or not

    def __repr__(self):
        return "\n\tt: %s\n keys: %s\n\t children: %s\n\t leaf: %s\n\t" % (self.t,self.keys,self.children,self.leaf)

    def __str__(self):
        return "\n\tt: %s\n\t keys: %s\n\t children: %s\n\t leaf: %s\n\t" % (self.t,self.keys,self.children,self.leaf)

    def insert(self,k):
        self.keys.append(k)
        self.keys = sorted(self.keys)

        if len(self.keys) == self.t:
            if self.leaf:
                middle = self.keys[[len(self.keys)//2][0]]  #On even values it chooses the one on the right
                self.keys.remove(middle)
                self.splitNode()
                self.keys = [middle]
                self.leaf = False
            else:
                pass


    def traverse(self):
        if self.leaf == True:
            for k in self.keys:
                print (k)
        else:
            for i in range(len(self.children)):
                self.children[i].traverse()


    def splitNode(self):
        self.createChildNode(self.keys[:len(self.keys)//2])
        self.createChildNode(self.keys[len(self.keys)//2:])


    def createChildNode(self,l):
        self.children.append(BTreeNode(self.t,True))
        for i in l:
            self.children[len(self.children)-1].insert(i)

class BTree(object):
    def __init__(self,t):
        self.t = t
        self.root = None

    def __repr__(self):
        return "t:%s\n root: %s\n " % (self.t,self.root)
    def __str__(self):
        return "t:%s\n root: %s\n " % (self.t,self.root)

    def insert(self,k):
        if self.root == None:
            self.root = BTreeNode(self.t,True)

        self.root.insert(k)


    def traverse(self):
        self.root.traverse()

if __name__ == '__main__':
    size = 7
    b = BTree(size)
    for i in range(size*3):
        b.insert(random.randint(0,99))
    print
    b.traverse()
    print (b)
