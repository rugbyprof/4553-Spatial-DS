# Based on C++ implementation here:
# http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/
# Probably could be much better, but
from _bisect import *

class BTreeNode(object):
    def __init__(self,t,leaf):
        self.t = t                               # Minimum degree (defines the range for number of keys)
        self.keys = []                        # An array of keys and children
        self.children = []
        self.n = 0                               # Current number of keys
        self.leaf = leaf                         # Leaf or not

    def traverse(self):
        # There are n keys and n+1 children, travers through n keys
        # and first n children
        for i in range(self.n):
            # If this is not leaf, then before printing key[i],
            # traverse the subtree rooted with child children[i].
            if self.leaf == False:
                self.children[i].traverse()
            print self.keys[i]

        # Print the subtree rooted with last child
        if self.leaf == False:
            self.children[-1].traverse()

    def search(self,k):
        # Find key that is next largest or equal to k
        v = self.find_ge(self.keys, k)
        if v:
            i = self.keys.index(v)
        else:
            i = len(self.keys)-1

        # If the found key is equal to k, return this node
        if k in self.keys:
            return self

        # If key is not found here and this is a leaf node
        elif self.leaf == True:
            return None

        else:
            # Go to the appropriate child
            #print "go chile"
            return self.children[i].search(k)

    # A utility function to insert a new key in this node
    # The assumption is, the node must be non-full when this
    # function is called
    def insertNonFull(self, k):

        # Initialize index as index of rightmost element
        i = self.n-1

        print i

        # If this is a leaf node
        if self.leaf == True:

            # The following loop does two things
            # a) Finds the location of new key to be inserted
            # b) Moves all greater keys to one place ahead
            print self.keys

            self.keys.append(k)

            self.keys = sorted(self.keys)

            self.n = self.n+1

        else: # If this node is not leaf

            # Find the child which is going to have the new key
            while i >= 0 and self.keys[i] > k:
                i -= 1

            # See if the found child is full
            if self.children[i+1].n == 2 * self.t - 1:

                # If the child is full, then split it
                self.splitChild(i+1, self.children[i+1])

                # After split, the middle key of children[i] goes up and
                # children[i] is splitted into two.  See which of the two
                # is going to have the new key
                if self.keys[i+1] < k:
                    i += 1

            self.children[i+1].insertNonFull(k)

    # A utility function to split the child y of this node
    # Note that y must be full when this function is called
    def splitChild(self, i, y):
        # Create a new node which is going to store (t-1) keys
        # of y
        z = BTreeNode(y.t, y.leaf)
        z.n = self.t - 1

        # Copy the last (t-1) keys of y to z
        for j in range(self.t-1):
            z.keys.append(y.keys[j+self.t])

        # Copy the last t children of y to z
        if y.leaf == False:

            for j in range(self.t):
                z.children[j].append(y.children[j+self.t])


        # Reduce the number of keys in y
        y.n = self.t - 1

        # Link the new child to this node
        self.children.insert(i+1,z)

        # Copy the middle key of y to this node
        self.keys.append(y.keys[self.t-1])

        self.keys = sorted(self.keys)

        # Increment count of keys in this node
        self.n = self.n + 1

    def find_ge(self,a, x):
        'Find leftmost item greater than or equal to x'
        i = bisect_left(a, x)
        if i != len(a):
            return a[i]

        return None

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.t,self.keys,self.children,self.n,self.leaf)
    def __repr__(self):
        return "%s, %s, %s, %s, %s" % (self.t,self.keys,self.children,self.n,self.leaf)


class BTree(object):
    def __init__(self,t):
        self.root = None
        self.t = t

    def traverse(self):
        if not self.root == None:
            self.root.traverse()

    def search(self,k):
        if self.root == None:
            return None
        else:
            return self.root.search(k)

    # The main function that inserts a new key in this B-Tree
    def insert(self, k):
        # If tree is empty
        if self.root == None:
            # Create instance for root
            self.root = BTreeNode(self.t, True)
            self.root.keys.append(k)         # Insert key
            self.root.n = 1                  # Update number of keys in root

        else: # If tree is not empty

            # If root is full, then tree grows in height
            if self.root.n == 2 * self.t - 1:

                # Allocate memory for new root
                s = BTreeNode(self.t, False)

                # Make old root as child of new root
                s.children.append(self.root)

                # Split the old root and move 1 key to the new root
                s.splitChild(0, self.root)

                # New root has two children now.  Decide which of the
                # two children is going to have new key
                i = 0
                if s.keys[0] < k:
                    i += 1
                s.children[i].insertNonFull(k)

                # Change root
                self.root = s

            else:  # If root is not full, call insertNonFull for root
                self.root.insertNonFull(k)


if __name__ == '__main__':

    t = BTree(3)
    t.insert(10)
    t.insert(20)
    t.insert(5)
    t.insert(6)
    t.insert(12)
    t.insert(30)
    t.insert(7)
    t.insert(17)

    print"Traversal of the constucted tree is ";
    t.traverse()

    print "================\n\n"

    k = 6
    print t.search(k)

    k = 15
    print t.search(k)
