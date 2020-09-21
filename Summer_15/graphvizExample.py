import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import graphviz as gv

class graphVizClass:
    def __init__(self):
        self.nodeCount = 0
        self.graph = gv.Digraph(format='svg')

    def addNodeStyle(self,style):
        for k,v in style.items():
            self.graph.node_attr[k]=v

    def addEdgeStyle(self,style):
        for k,v in style.items():
            self.graph.edge_attr[k]=v

    def addNodes(self,nodes):
        for n in nodes:
            l = ','.join(map(str, n))
            self.graph.node(str(self.nodeCount),label=l)
            self.nodeCount += 1

    def addEdges(self,edges):
        for e in edges:
            self.graph.edge(e[0],e[1])

    def printGraph(self,filename='img/g1'):
        self.graph.render(filename='img/g1')

def GenerateBinaryTreeEdges(count):
    edges = []
    for i in range(count):
        left = ((i+1) * 2) - 1
        right = ((i+1) * 2 + 1) - 1

        if left < count:
            edges.append((str(i),str(left)))
        if right < count:
            edges.append((str(i),str(right)))
    return edges


if __name__ == '__main__':

    myGraph = graphVizClass()

    nodeStyle = {"style":"filled",
                 "shape":"circle",
                 "fixedsize":"true",
                 "fontcolor":"#000000",
                 "shape":"box",
                 "fontsize":"24",
                 "color":"red"}
    edgeStyle = {"color":"Blue", "style":"dashed"}

    myGraph.addNodeStyle(nodeStyle)
    myGraph.addEdgeStyle(edgeStyle)

    Nodes = [[3,1,4],[2,3,7],[4,3,4],[2,1,3],[2,4,5],[6,1,4],[1,4,4],[0,5,7],[5,2,5],[4,0,6],[7,1,6]]
    Edges = GenerateBinaryTreeEdges(len(Nodes))

    myGraph.addNodes(Nodes)
    myGraph.addEdges(Edges)
    myGraph.printGraph()
