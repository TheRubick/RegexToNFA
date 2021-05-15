import json
#0 for concat, 1 for oring, 2 for repeat
#((0|1)*+(01))
#((C)*+(01))
#(D+(01))
#(D+E)
#Z0
table = {'Z':{"operation":1,'oprd1':'D', 'oprd2':'E' },
        'D':{'operation':2,'oprd1':'C', 'oprd2':-1 },
        'C':{'operation':1,'oprd1':'0', 'oprd2':'1' },
        'E':{'operation':0,'oprd1':'0', 'oprd2':'1' }}

node0= {'n':0, 't':'S','p':[], 'c':[(1,'z')]}
node1= {'n':1, 't':'I','p':[0], 'c':[(2,-1)]}
node2= {'n':2, 't':'E','p':[1], 'c':[]}
graph = []
graph.append(node0)
graph.append(node1)
graph.append(node2)

def printNFAgraph(graph):
    print("/////////////////////////")
    startingNode = -1
    endingNode = -1
    for i in range(len(graph)):
        if graph[i]['n']!= -1:
            if graph[i]['t'] == 'S':
                startingNode = graph[i]['n']
            elif graph[i]['t'] == 'E':
                endingNode = graph[i]['n']
            for j in range(len(graph[i]['c'])):
                print(graph[i]['n'],"--->",graph[i]['c'][j][0],"by value = ",graph[i]['c'][j][1])
    print("Starting Node = ",startingNode)
    print("Ending Node = ",endingNode)
def ORing(graph, node, op1, op2):
    counter = len(graph)
    node3 = {'n':counter, 
            't':'I',
            'p': graph[node]['p'],
            'c': [(counter+1,-1),(counter+2,-1)]
            }
    node4 = {'n':counter+1, 
            't':'I',
            'p': [counter],
            'c': [(counter+3,op1)]
            }
    node5 = {'n':counter+2, 
            't':'I',
            'p': [counter],
            'c': [(counter+4,op2)]
            }
    node6 = {'n':counter+3, 
            't':'I',
            'p': [counter+1],
            'c': [(counter+5,-1)]
            }
    node7 = {'n':counter+4, 
            't':'I',
            'p': [counter+2],
            'c': [(counter+5,-1)]
            }
    node8 = {'n':counter+5, 
            't':'I',
            'p': [counter+3,counter+4],
            'c': graph[node]['c']
            }
    #modify parents of node2
    for i in graph[node]['p']: #number of parents
        for j in range(len(graph[i]['c'])): #number of children 
            if graph[i]['c'][j][0] == node:
                graph[i]['c'].pop(j)
                graph[i]['c'].append((counter,-1))
                break
    #modify children of node
    for i in range(len(graph[node]['c'])):
        graph[graph[node]['c'][i][0]]['p'].remove(node)
        graph[graph[node]['c'][i][0]]['p'].append(counter+5)
    #remove node 2
    graph[node]['n'] = -1
    #append new nodes
    graph.append(node3)
    graph.append(node4)
    graph.append(node5)
    graph.append(node6)
    graph.append(node7)
    graph.append(node8)
    return graph

def Concat(graph, node, op1, op2):
    counter = len(graph)
    node3 = {'n':counter, 
            't':'I',
            'p': graph[node]['p'],
            'c': [(counter+1,op1)]
            }
    node4 = {'n':counter+1, 
            't':'I',
            'p': [counter],
            'c': [(counter+2,op2)]
            }
    node5 = {'n':counter+2, 
            't':'I',
            'p': [counter+1],
            'c': graph[node]['c']
            }
    
    #modify parents of node
    for i in graph[node]['p']: #number of parents
        for j in range(len(graph[i]['c'])): #number of children 
            if graph[i]['c'][j][0] == node:
                graph[i]['c'].pop(j)
                graph[i]['c'].append((counter,-1))
                break
    #modify children of node
    for i in range(len(graph[node]['c'])):
        graph[graph[node]['c'][i][0]]['p'].remove(node)
        graph[graph[node]['c'][i][0]]['p'].append(counter+2)
    #remove node 2
    graph[node]['n'] = -1
    #append new nodes
    graph.append(node3)
    graph.append(node4)
    graph.append(node5)
    return graph
    
def Repeat(graph, node, op):
    counter = len(graph)
    node3 = {'n':counter, 
            't':'I',
            'p': [graph[node]['p'],counter+1],
            'c': [(counter+1,op),(counter+2,-1)]
            }
    node4 = {'n':counter+1, 
            't':'I',
            'p': [counter],
            'c': [(counter,-1),(counter+2,-1)]
            }
    node5 = {'n':counter+2, 
            't':'I',
            'p': [counter,counter+1],
            'c': graph[node]['c']
            }
    
    #modify parents of node
    for i in graph[node]['p']: #number of parents
        for j in range(len(graph[i]['c'])): #number of children 
            if graph[i]['c'][j][0] == node:
                graph[i]['c'].pop(j)
                graph[i]['c'].append((counter,-1))
                break
    #modify children of node
    for i in range(len(graph[node]['c'])):
        graph[graph[node]['c'][i][0]]['p'].remove(node)
        graph[graph[node]['c'][i][0]]['p'].append(counter+2)
    #remove node 2
    graph[node]['n'] = -1
    #append new nodes
    graph.append(node3)
    graph.append(node4)
    graph.append(node5)
    return graph

#graph = ORing(graph,1,'a','1')
#graph = Concat(graph,6,'0','1')
#graph = Repeat(graph,1,'0',)
#(1+0)*1 example1
def example1(graph):
    graph = Concat(graph,1,'B','1')
    graph = Repeat(graph,4,'A')
    graph = ORing(graph,7,'1','0')
    printNFAgraph(graph)
#(a|b)*abb
def example2(graph):
    graph = Concat(graph,1,'X4','b')
    graph = Concat(graph,4,'X3','b')
    graph = Concat(graph,7,'X2','a')
    graph = Repeat(graph,10,'X1')
    graph = ORing(graph,13,'a','b')
    printNFAgraph(graph)


def createNFA(table,originalChars,superNode):
    #create initial graph
    print(table)
    node0= {'n':0, 't':'S','p':[], 'c':[(1,superNode)]}
    node1= {'n':1, 't':'I','p':[0], 'c':[(2,-1)]}
    node2= {'n':2, 't':'E','p':[1], 'c':[]}
    graph = []
    graph.append(node0)
    graph.append(node1)
    graph.append(node2)
    exit = False
    while not exit:
        exit = True
        for i in range(len(graph)):#all nodes in graph
            if graph[i]['n']!= -1:#for valid nodes
                for j in range(len(graph[i]['c'])):#check children
                    value = graph[i]['c'][j][1]
                    node = graph[i]['c'][j][0]
                    if value not in originalChars and value != -1:#means expression to expand
                        exit = False
                        operation = table[value]["operation"]#define type of operation
                        opd1 = table[value]["oprd1"]
                        #apply the operation
                        if operation == 0:#concat
                            opd2 = table[value]["oprd2"]
                            print("Concat between ",opd1,", ",opd2)
                            Concat(graph,node,opd1,opd2)
                        elif operation == 1:#oring
                            opd2 = table[value]["oprd2"]
                            print("Oring between ",opd1,", ",opd2)
                            ORing(graph,node,opd1,opd2)
                        elif operation == 2:#repeat
                            print("Repeat ",opd1)
                            Repeat(graph,node,opd1)
    return graph
#Same as example 1
# 0 for concat, 1 for oring, 2 for repeat
#(1+0)*1
#A*1
#B1
#Z
table1 = {
        'Z':{"operation":0,'oprd1':'B', 'oprd2':'1' },
        'B':{'operation':2,'oprd1':'A', 'oprd2':-1 },
        'A':{'operation':1,'oprd1':'1', 'oprd2':'0' }
        }
originalChars1 = ['0','1']

#Same as example 2
# 0 for concat, 1 for oring, 2 for repeat
#(a|b)*abb
#(x1)*abb
#x2abb
#x3bb
#x4b
#Z
table2 = {
        'Z':{"operation":0,'oprd1':'x4', 'oprd2':'b' },
        'x4':{'operation':0,'oprd1':'x3', 'oprd2':'b' },
        'x3':{'operation':0,'oprd1':'x2', 'oprd2':'a' },
        'x2':{'operation':2,'oprd1':'x1' },
        'x1':{'operation':1,'oprd1':'a', 'oprd2':'b' }
        }
originalChars2 = ['a','b']



#graph = createNFA(table2,originalChars2,'Z')
#printNFAgraph(graph)

def OutputGraph(graph, alphabet):
    print("/////////////////////////")
    #endNode = False
    out = {"startingState":-1}
    for i in range(len(graph)):
        if graph[i]['n']!= -1:
            out[str(graph[i]['n'])] = {"isTerminatingState": False}
            for ch in alphabet:
                out[str(graph[i]['n'])][ch] = []
            out[str(graph[i]['n'])]["epsilon"] = []
            if graph[i]['t'] == 'S':
                out["startingState"] = str(graph[i]['n'])
            elif graph[i]['t'] == 'E':
                out[str(graph[i]['n'])]["isTerminatingState"] = True
            for j in range(len(graph[i]['c'])):
                value = graph[i]['c'][j][1]
                child = graph[i]['c'][j][0]
                print(graph[i]['n'],"--->",graph[i]['c'][j][0],"by value = ",graph[i]['c'][j][1])
                if(value == -1):
                    out[str(graph[i]['n'])]["epsilon"].append(str(child))
                else:
                    out[str(graph[i]['n'])][str(value)].append(str(child))

    print(json.dumps(out, indent=2))
    return out
                
    
            
     