from graphviz import Digraph
from NFA import createNFA
from NFA import printNFAgraph
from NFA import OutputGraph
from regex import buildTable
from regex import isValidInput
#graph
node0= {'n':0, 't':'S','p':[], 'c':[(1,'z')]}
node1= {'n':1, 't':'I','p':[0], 'c':[(2,-1)]}
node2= {'n':2, 't':'E','p':[1], 'c':[]}
graph = []
graph.append(node0)
graph.append(node1)
graph.append(node2)

def drawNFA(graph):
    dot = Digraph(comment='The Round Table')
    for i in range(len(graph)):
        if graph[i]['n']!= -1:
            if graph[i]['t'] == 'E':
                dot.node(str(graph[i]['n']), str(graph[i]['n']), shape = "doublecircle")
            elif graph[i]['t'] == 'S':
                dot.node(str(graph[i]['n']), str(graph[i]['n']), shape = "box")
            else:
                dot.node(str(graph[i]['n']), str(graph[i]['n']), shape = "circle")
    for i in range(len(graph)):
        if graph[i]['n']!= -1:
            for j in range(len(graph[i]['c'])):
                dot.edge(str(graph[i]['n']), str(graph[i]['c'][j][0]), label =str(graph[i]['c'][j][1]) if graph[i]['c'][j][1] != -1 else "ε")
    #dot = dot.unflatten(stagger=2)
    dot.render('test-output/NFA', view=True) 
    #u = dot.unflatten(stagger=3)
    #u.view()
table2 = {
        'Z':{"operation":0,'oprd1':'x4', 'oprd2':'b' },
        'x4':{'operation':0,'oprd1':'x3', 'oprd2':'b' },
        'x3':{'operation':0,'oprd1':'x2', 'oprd2':'a' },
        'x2':{'operation':2,'oprd1':'x1' },
        'x1':{'operation':1,'oprd1':'a', 'oprd2':'b' }
        }
originalChars2 = ['a','b']
#example assignmet
#0+(1((0+1)*)00)
#0+(1B*00)
#0+(1F00)
#0+(C00)
#0+D0
#0+E
#Z
table3 = {
        'Z':{"operation":1,'oprd1':'0', 'oprd2':'E' },
        'E':{'operation':0,'oprd1':'D', 'oprd2':'0' },
        'D':{'operation':0,'oprd1':'C', 'oprd2':'0' },
        'C':{'operation':0,'oprd1':'1', 'oprd2':'F' },
        'B':{'operation':1,'oprd1':'0', 'oprd2':'1' },
        'F':{'operation':2,'oprd1':'B' }
        }
originalChars3 = ['0','1']
regex = "(a|b)*abb"#"0|(1(0+1)*00)"
#check the validity of the input and return its specialchars if it valid , none otherwise
originalChars = isValidInput(regex)
if(originalChars is not None):
    #get table from regex
    x,y,z,table = buildTable(0,0,regex)
    superNode = "Node"+str(len(table)-1)
    #create NFA
    graph = createNFA(table,originalChars,superNode)
    #json  of graph
    graph_jason = OutputGraph(graph,originalChars)
    #sketch the graph
    drawNFA(graph)
else:
    print("invalid character(s)")