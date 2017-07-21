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

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = None
        self.weights = None

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

# Function to find the weight of the edges, given the x and y coordinates
def weightsFromCoords(X1, Y1, X2, Y2):
    weight = math.sqrt((X1 - X2)^2 + (Y1 - Y2)^2)
    return weight

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


readTextFile()
