import graphviz as gv

g1 = gv.Digraph(format='svg')

nodeStyle = {"style":"filled",
             "shape":"circle",
             "fixedsize":"true",
             "fontcolor":"#FFFFFF"}

print nodeStyle

for k, v in nodeStyle.iteritems():
    g1.node_attr[k]=v

Nodes = [[],[3,1,4],
[2,3,7],
[4,3,4],
[2,1,3],
[2,4,5],
[6,1,4],
[1,4,4],
[0,5,7],
[5,2,5],
[4,0,6],
[7,1,6]]

for n in range(len(Nodes)):
    if n == 0:
        continue
    print n
    l = ','.join(map(str, Nodes[n]))
    print l
    g1.node(str(n),label=l)

for i in range(len(Nodes)):
    if i == 0:
        continue
    left = i * 2
    right = i * 2 + 1

    if left < len(Nodes):
        g1.edge(str(i),str(left))
    if right < len(Nodes):
        g1.edge(str(i),str(right))

filename = g1.render(filename='img/g1')
