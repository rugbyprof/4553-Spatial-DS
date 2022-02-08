#! / Usr / bin / python
# - * - Coding: utf-8 - * -


# class MBR(object):
#     def __init__(self, xmin=None, ymin=None, xmax=None, ymax=None):
#         self.xmin = xmin
#         self.ymin = ymin
#         self.xmax = xmax
#         self.ymax = ymax

#     def __str__(self):
#         return f"[({self.xmin},{self.ymin}) - ({self.xmax},{self.ymax})]"

#     def __repr__(self):
#         return self.__str__()


class node(object):
    """
    Define storage object that Contains its location information MBR,
    - level is fixed at 0 indicates the bottom,
    - index for the index in the database,
    - father of its parent.
    """

    def __init__(self, MBR=None, level=0, index=None, father=None):
        if MBR == None:
            self.MBR = {"xmin": None, "xmax": None, "ymin": None, "ymax": None}
        else:
            self.MBR = MBR
        self.level = level
        self.index = index
        self.father = father

    def __str__(self):
        return f""


class Rtree(object):
    """
    Definition of R tree node that Contains the location information MBR.
    - level of its layers, the default is 1 leaf node,
    - m and M for minimum and maximum number of children's,
    - father of its parent.
    """

    def __init__(self, leaves=None, MBR=None, level=1, m=1, M=3, father=None):
        self.leaves = []
        if MBR == None:
            self.MBR = {"xmin": None, "xmax": None, "ymin": None, "ymax": None}
        else:
            self.MBR = MBR
        self.level = level
        self.m = m
        self.M = M
        self.father = father

    def __repr__(self):
        return "%s" % (self.MBR)

    # ChooseLeaf Choose Insert node.
    def ChooseLeaf(self, node):
        # If the current node layers higher than the node to be inserted one layer, indicating that found the appropriate node.
        if self.level == node.level + 1:
            return self
        else:
            # Otherwise its MBR child node traversal, find an area of increasing minimum.
            increment = [
                (i, SpaceIncrease(self.leaves[i].MBR, node.MBR))
                for i in range(len(self.leaves))
            ]
            res = min(increment, key=lambda x: x[1])
            return self.leaves[res[0]].ChooseLeaf(node)

    # SplitNode Split node.
    def SplitNode(self):
        # If the current node has no parent, the parent is bound to accommodate the need to produce two nodes split.
        if self.father == None:
            # Parent node level than the current one.
            self.father = Rtree(level=self.level + 1, m=self.m, M=self.M)
            self.father.leaves.append(self)
        # Create new nodes, m, M and father are the same as the current node.
        leaf1 = Rtree(level=self.level, m=self.m, M=self.M, father=self.father)
        leaf2 = Rtree(level=self.level, m=self.m, M=self.M, father=self.father)
        # Call PickSeeds to leaf1 and leaf2 distribution of child nodes
        self.PickSeeds(leaf1, leaf2)
        # Traverse the remaining sub-node insertion.
        while len(self.leaves) > 0:
            # If the remaining child node into a group in order to make the set of nodes is greater than m, fully inserted directly into it, and adjust the MBR.
            if (
                len(leaf1.leaves) > len(leaf2.leaves)
                and len(leaf2.leaves) + len(self.leaves) == self.m
            ):
                for leaf in self.leaves:
                    leaf2.MBR = Merge(leaf2.MBR, leaf.MBR)
                    leaf2.leaves.append(leaf)
                    leaf.father = leaf2
                self.leaves = []
                break
            if (
                len(leaf2.leaves) > len(leaf1.leaves)
                and len(leaf1.leaves) + len(self.leaves) == self.m
            ):
                for leaf in self.leaves:
                    leaf1.MBR = Merge(leaf1.MBR, leaf.MBR)
                    leaf1.leaves.append(leaf)
                    leaf.father = leaf1
                self.leaves = []
                break
            # Otherwise call PickNext for the next leaf1 and leaf2 assign a node.
            self.PickNext(leaf1, leaf2)
        # Of the current node's parent deleted the current node and added two new nodes, complete split.
        self.father.leaves.remove(self)
        self.father.leaves.append(leaf1)
        self.father.leaves.append(leaf2)
        self.father.MBR = Merge(self.father.MBR, leaf1.MBR)
        self.father.MBR = Merge(self.father.MBR, leaf2.MBR)

    # PickSeeds Child node is assigned two nodes.
    def PickSeeds(self, leaf1, leaf2):
        d = 0
        t1 = 0
        t2 = 0
        # Through all the possible combinations of child nodes, to find the difference between the largest item.
        for i in range(len(self.leaves)):
            for j in range(i + 1, len(self.leaves)):
                MBR_new = Merge(self.leaves[i].MBR, self.leaves[j].MBR)
                S_new = (
                    1.0
                    * (MBR_new["xmax"] - MBR_new["xmin"])
                    * (MBR_new["ymax"] - MBR_new["ymin"])
                )
                S1 = (
                    1.0
                    * (self.leaves[i].MBR["xmax"] - self.leaves[i].MBR["xmin"])
                    * (self.leaves[i].MBR["ymax"] - self.leaves[i].MBR["ymin"])
                )
                S2 = (
                    1.0
                    * (self.leaves[j].MBR["xmax"] - self.leaves[j].MBR["xmin"])
                    * (self.leaves[j].MBR["ymax"] - self.leaves[j].MBR["ymin"])
                )
                if S_new - S1 - S2 > d:
                    t1 = i
                    t2 = j
                    d = S_new - S1 - S2
        n2 = self.leaves.pop(t2)
        n2.father = leaf1
        leaf1.leaves.append(n2)
        leaf1.MBR = leaf1.leaves[0].MBR
        n1 = self.leaves.pop(t1)
        n1.father = leaf2
        leaf2.leaves.append(n1)
        leaf2.MBR = leaf2.leaves[0].MBR

    # PickNext Assigned a child node to two nodes.
    def PickNext(self, leaf1, leaf2):
        d = 0
        t = 0
        # Traverse the child nodes, found after inserting two nodes of a difference between the maximum area increased.
        for i in range(len(self.leaves)):
            d1 = SpaceIncrease(Merge(leaf1.MBR, self.leaves[i].MBR), leaf1.MBR)
            d2 = SpaceIncrease(Merge(leaf2.MBR, self.leaves[i].MBR), leaf2.MBR)
            if abs(d1 - d2) > abs(d):
                d = d1 - d2
                t = i
        if d > 0:
            target = self.leaves.pop(t)
            leaf2.MBR = Merge(leaf2.MBR, target.MBR)
            target.father = leaf2
            leaf2.leaves.append(target)
        else:
            target = self.leaves.pop(t)
            leaf1.MBR = Merge(leaf1.MBR, target.MBR)
            target.father = leaf1
            leaf1.leaves.append(target)

    # AdjustTree Bottom upward adjustment R tree.
    def AdjustTree(self):
        p = self
        while not p == None:
            # If the number of the leaf nodes of the current exceeds M, the division of the parent node and adjust the MBR.
            if len(p.leaves) > p.M:
                p.SplitNode()
            else:
                # Otherwise adjust MBR parent node.
                if not p.father == None:
                    p.father.MBR = Merge(p.father.MBR, p.MBR)
            p = p.father

    # Search Search for a given rectangle.
    def Search(self, MBR):
        result = []
        # If you have reached a leaf node, then add the result objects directly.
        if self.level == 1:
            for leaf in self.leaves:
                if Intersect(MBR, leaf.MBR):
                    result.append(leaf.index)
            return result
        # Otherwise, the target for MBR Intersects child nodes Search, and added to the result.
        else:
            for leaf in self.leaves:
                if Intersect(MBR, leaf.MBR):
                    result = result + leaf.Search(MBR)
            return result

    # FindLeaf Locate a given object.
    def FindLeaf(self, node):
        result = []
        # If the current node is not a leaf node, all child nodes are recursively search the MBR Contains the target.
        if not self.level == 1:
            for leaf in self.leaves:
                if Contain(leaf.MBR, node.MBR):
                    result.append(leaf.FindLeaf(node))
            for x in result:
                if not x == None:
                    return x
        # If the current node is a leaf node, the direct traversal of these objects to determine whether the same index, and return.
        else:
            for leaf in self.leaves:
                if leaf.index == node.index:
                    return self

    # CondenseTree Compress the tree.
    def CondenseTree(self):
        # Q To save the node to be inserted.
        Q = []
        p = self
        q = self
        while not p == None:
            p.MBR = {"xmin": None, "xmax": None, "ymin": None, "ymax": None}
            # re path
            for leaf in p.leaves:
                p.MBR = Merge(p.MBR, leaf.MBR)
            # If the leaves of the tree is less than the current node m, the parent node to remove the node, if the node still Contain child nodes, child nodes need to be reinserted.
            if len(p.leaves) < self.m and not p.father == None:
                p.father.leaves.remove(p)
                if not len(p.leaves) == 0:
                    Q = Q + p.leaves
            q = p
            p = p.father
        # Reinsert the node to be inserted
        for node in Q:
            q = Insert(q, node)

    # CondenseRoot Used for the root compression.
    def CondenseRoot(self):
        p = self
        q = p
        # If the root node has only one child node, replace the child node as the root node, multiple sub-node until the root node is a leaf node or the root node.
        while len(p.leaves) == 1 and p.father == None and not p.level == 1:
            p = p.leaves[0]
            q.leaves = []
            p.father = None
            q = p
        return p


# Insert a new node, return to the root node after the update.
def Insert(root, node):
    target = root.ChooseLeaf(node)
    node.father = target
    target.leaves.append(node)
    target.MBR = Merge(target.MBR, node.MBR)
    target.AdjustTree()
    if not root.father == None:
        root = root.father
    return root


# Delete Delete the target object, return to the root updated.
def Delete(root, node):
    target = root.FindLeaf(node)
    if target == None:
        print("no result")
        return root
    target.leaves.remove(node)
    target.CondenseTree()
    root = root.CondenseRoot()
    return root


# Merge to Merge two MBR.
def Merge(MBR1, MBR2):
    if MBR1["xmin"] == None:
        return MBR2
    if MBR2["xmin"] == None:
        return MBR1
    MBR = {}
    MBR["xmin"] = min(MBR1["xmin"], MBR2["xmin"])
    MBR["ymin"] = min(MBR1["ymin"], MBR2["ymin"])
    MBR["xmax"] = max(MBR1["xmax"], MBR2["xmax"])
    MBR["ymax"] = max(MBR1["ymax"], MBR2["ymax"])
    return MBR


# SpaceIncrease used to calculate the increase MBR1 area after MBR2 into MBR1.
def SpaceIncrease(MBR1, MBR2):
    xmin = min(MBR1["xmin"], MBR2["xmin"])
    ymin = min(MBR1["ymin"], MBR2["ymin"])
    xmax = max(MBR1["xmax"], MBR2["xmax"])
    ymax = max(MBR1["ymax"], MBR2["ymax"])
    return 1.0 * (
        (xmax - xmin) * (ymax - ymin)
        - (MBR1["xmax"] - MBR1["xmin"]) * (MBR1["ymax"] - MBR1["ymin"])
    )


# Intersect MBR1 and MBR2 judge whether there is common ground.
def Intersect(MBR1, MBR2):
    if (
        MBR1["xmin"] > MBR2["xmax"]
        or MBR1["xmax"] < MBR2["xmin"]
        or MBR1["ymin"] > MBR2["ymax"]
        or MBR1["ymax"] < MBR2["ymin"]
    ):
        return 0
    return 1


# Contain judge MBR1 Contains MBR2.
def Contain(MBR1, MBR2):
    return (
        MBR1["xmax"] >= MBR2["xmax"]
        and MBR1["xmin"] <= MBR2["xmin"]
        and MBR1["ymax"] >= MBR2["ymax"]
        and MBR1["ymin"] <= MBR2["ymin"]
    )
