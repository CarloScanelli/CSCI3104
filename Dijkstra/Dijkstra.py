import math
from collections import defaultdict
import operator

class Node:
    def __init__(self):
        self.id = None
        self.x = None
        self.y = None
        self.neighbors = []
        self.color = "white"
        self.pi = None
        self.adj = []
        self.d = None
        self.f = None

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = None
        self.weights = None
        self.time = 0

# Function to read the textFile containing the information about the graph
def readTextFile():
    # open the textfile
    txtFile = open("smallTest.txt","r")

    # reads first line of file, to extract number of vertices and edges
    firstLine = txtFile.readline()
    vAnde = firstLine.split()
    print "\nNumber of vertices: ", vAnde[0]
    print "Number of edges: ", vAnde[1]

    # Read the rest of the file
    lines = txtFile.readlines()

    # Find the first section, which holds the information about the locations
    firstSection = detectSection(lines, 1)

    # Extract ids, x and y coords. Use these info to make an array of nodes.
    # Sort the array, in case the nodes are not given in order in the txt file.
    infos = []
    for i in firstSection:
        if (i != "\n"):
            info = i.split()
            infos.append(info)
    nodes = buildNodes(infos)
    nodes.sort(key=operator.attrgetter('id'))

    # finds second section, which lists the connections
    firstSectionLength = len(firstSection);
    secondSection = detectSection(lines, firstSectionLength + 1)

    # get the connections/edges from the text file
    connections = findEdges(secondSection)

    # build the graph, and represent it as an adjacency list
    g = edgesToDict(connections)
    #print "\nGraph: ", g

    # add the neighboring vertices to the node instances
    for item in g:
        nodes[int(item[0])].neighbors = map(int, item[1])

    # build the graph
    graph = buildGraph(nodes)

    # find cycle
    cycle = findCycle(graph)
    print "Cycle? ", cycle

    print "TEst: "
    ksjd = DFS(graph)
    print ksjd

    shortestPathDAG(graph, 0)
    pid = 4
    while pid:
        print "parent of "+str(pid)+" is "+str(graph.nodes[pid].pi)+"  the distance to parent is "+str(graph.nodes[pid].d)
        pid = graph.nodes[pid].pi
    # print "+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+="
    # for each in graph.nodes:
    #     print each.id, each.pi

    # finds the last section
    secondSectionLength = len(secondSection);
    # print "\nTests: "
    thirdSection = detectSection(lines, secondSectionLength + firstSectionLength + 1)
    # for i in thirdSection:
    #     print i,

    txtFile.close() # To free up any system resources taken up by the open file

# creates an array of nodes, with respective ids and positions
def buildNodes(nodesInfo):
    nodes = []
    for i in range(0, len(nodesInfo)):
        newNode = Node()
        newNode.id = int(nodesInfo[i][0])
        newNode.x = int(nodesInfo[i][1:-1][0])
        newNode.y = int(nodesInfo[i][2])
        nodes.append(newNode)
    return nodes

# function to build the graph of nodes instances
def buildGraph(nodes):
    newGraph = Graph()
    newGraph.nodes = nodes
    return newGraph

# Function to create a list which stores the connections
def findEdges(connectionsList):
    connections = []
    for line in connectionsList:
        if (line != "\n"):
            parts = line.split()
            connections.append((parts[0], parts[1]))
    return connections

# Function to convert the list of connections to an adjacency list.
# This is used to represent the graph.
def edgesToDict(edges):
    graphDict = defaultdict(list)
    for k, v in edges:
        graphDict[k].append(v)
    return sorted(graphDict.items())

# Function to divide the textfile into sections
def detectSection(file, start):
    section = []
    length = len(file)
    for i in range(start, length):
        section.append(file[i])
        if (file[i] == "\n"):
            break
    return section

# Next two functions determine whether the graph has a cycle
def findCycle(graph):
    V = len(graph.nodes)
    visited = [False] * V
    path = [False] * V
    for node in range(0, V):
        if visited[node] == False:
            if isCyclic(graph, node, visited, path) == True:
                return True
    return False

def isCyclic(graph, index, visited, path):
    visited[index] = True
    path[index] = True
    for i in graph.nodes[index].neighbors:
        if visited[i] == False:
            if isCyclic(graph, i, visited, path) == True:
                return True
        elif path[i] == True:
            return True
    path[index] = False
    return False

def DFS(graph):
    for vertex in graph.nodes:
        vertex.color = "white"
        vertex.pi = None
    graph.time = 0
    stack = []
    for vertex in graph.nodes:
        if (vertex.color == "white"):
            DFSvisit(graph, vertex, stack)
    return stack

def DFSvisit(graph, u, stack):
    graph.time = graph.time + 1
    u.d = graph.time
    u.color = "gray"
    for vertexIndex in u.neighbors:
        if (graph.nodes[vertexIndex].color == "white"):
            graph.nodes[vertexIndex].pi = u.id
            DFSvisit(graph, graph.nodes[vertexIndex], stack)
    u.color = "black"
    graph.time = graph.time + 1
    u.f = graph.time
    stack.append(u.id)

def topologicalSort(graph):
    order = DFS(graph)
    return order

def shortestPathDAG(graph, s):
    increasingOrder = topologicalSort(graph)
    initSingleSource(graph, s)
    # for vertexIndex in increasingOrder:
    while increasingOrder:
        vertexIndex = increasingOrder.pop()
        print "vertexIndex :", vertexIndex
        for vIndex in graph.nodes[vertexIndex].neighbors:
            relax(graph, vertexIndex, vIndex)

def initSingleSource(graph, s):
    for vertex in graph.nodes:
        vertex.d = float("inf")
        vertex.pi = None
    graph.nodes[s].d = 0

def relax(graph, u, v):
    print "relax " + str(u)+" to "+str(v)
    print "distance to u: " + str(graph.nodes[u].d)
    if graph.nodes[v].d > graph.nodes[u].d + weightsFromCoords(graph.nodes[u],graph.nodes[v]):
        graph.nodes[v].d = graph.nodes[u].d + weightsFromCoords(graph.nodes[u],graph.nodes[v])
        graph.nodes[v].pi = u
        print "I just set the parent of node "+ str(v)+" to "+str(u)


# Function to find the weight of the edges, given the x and y coordinates
def weightsFromCoords(node1, node2):
    weight = math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
    return weight

readTextFile()
