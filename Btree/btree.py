# Based on C++ implementation here:
# http://www.geeksforgeeks.org/b-tree-set-1-introduction-2/

class BTreeNode(object):
    def __init__(self,t,leaf):
        self.keys = []      # An array of keys
        self.t =t           # Minimum degree (defines the range for number of keys)
        self.C = []         # An array of child pointers
        self.n = 0          # Current number of keys
        self.leaf = leaf   # Leaf or not

    def traverse(self):
        # There are n keys and n+1 children, travers through n keys
        # and first n children
        for i in range(self.n):
            # If this is not leaf, then before printing key[i],
            # traverse the subtree rooted with child C[i].
            if self.leaf == False:
                self.C[i].traverse()
            print self.keys[i]


        # Print the subtree rooted with last child
        if self.leaf == False
            self.C[-1].traverse();

    def search(self,k):
        # Find the first key greater than or equal to k
        i = 0
        while i < self.n and k > self.keys[i]:
            i += 1

        # If the found key is equal to k, return this node
        if self.keys[i] == k:
            return self

        # If key is not found here and this is a leaf node
        if leaf == True:
            return None

        # Go to the appropriate child
        return self.C[i].search(k);


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
            self.root.search(k)
