'''
Carlo Scanelli
CSCI 3104 - Assignment 7
'''
import math
from collections import defaultdict
import operator
import copy
import sys
import timeit
import matplotlib.pyplot as plt
import pylab as p
import numpy as np

class Node:
    def __init__(self):
        self.id = None
        self.x = None
        self.y = None
        self.neighbors = []
        self.color = "white"
        self.pi = None
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
    #txtFile = open("bigTest.txt","r")
    txtFile = open("smallTest.txt","r")

    # reads first line of file, to extract number of vertices and edges
    firstLine = txtFile.readline()
    vAnde = map(int, firstLine.split())
    print "Number of vertices: ", vAnde[0]
    print "Number of edges: ", vAnde[1]

    # Read the rest of the file
    lines = txtFile.readlines()

    # Find the first section, which holds the information about the locations
    firstSection = detectSection(lines, 1)

    # finds second section, which lists the connections
    firstSectionLength = len(firstSection);
    secondSection = detectSection(lines, firstSectionLength + 1)

    # Extract ids, x and y coords. Use these info to make an array of nodes.
    infos = getVerticesInfo(firstSection)

    # Creates an array of nodes, with respective ids and positions.
    # Sort the array, in case the nodes are not given in order in the txt file.
    nodes = buildNodes(infos)

    # gets the connections/edges from the text file, and stores them in a list.
    connections = findEdges(secondSection)

    # build the graph from the edges list, and represent it as an adjacency list
    g = edgesToDict(connections)

    # add the neighboring vertices to the node instances
    for item in g:
        nodes[int(item[0])].neighbors = map(int, item[1])

    # build the graph of node instances
    graph = buildGraph(nodes)

    # determine if the graph is acyclic
    cycle = findCycle(graph)
    if cycle == True:
        print "The graph is cyclic."
    else:
        print "The graph is acyclic."

    # Input desired starting vertex and destination here
    # source = 87536
    # destination = 87546
    source = 4
    destination = 3

    if source == destination:
        print "You are already there! The source is your destination. Shortest path distance is zero."
        quit()
    if source > vAnde[0]:
        print "Source too big."
    if destination > vAnde[0]:
        print "Destination too big."
    else:
        findShortestPath(cycle, graph, source, destination)

    txtFile.close() # To free up any system resources taken up by the open file

def getVerticesInfo(firstSection):
    infos = []
    for i in firstSection:
        if (i != "\n"):
            info = i.split()
            infos.append(info)
    return infos

def buildNodes(nodesInfo):
    nodes = []
    for i in range(0, len(nodesInfo)):
        newNode = Node()
        newNode.id = int(nodesInfo[i][0])
        newNode.x = int(nodesInfo[i][1:-1][0])
        newNode.y = int(nodesInfo[i][2])
        nodes.append(newNode)
    nodes.sort(key=operator.attrgetter('id'))
    return nodes

def buildGraph(nodes):
    newGraph = Graph()
    newGraph.nodes = nodes
    return newGraph

def findEdges(connectionsList):
    connections = []
    for line in connectionsList:
        if (line != "\n"):
            parts = line.split()
            connections.append((parts[0], parts[1]))
    return connections

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
    while increasingOrder:
        vertexIndex = increasingOrder.pop()
        for vIndex in graph.nodes[vertexIndex].neighbors:
            DAGrelax(graph, vertexIndex, vIndex)

def initSingleSource(graph, s):
    for vertex in graph.nodes:
        vertex.d = float("inf")
        vertex.pi = None
    graph.nodes[s].d = 0

def DAGrelax(graph, u, v):
    if graph.nodes[v].d > graph.nodes[u].d + weightsFromCoords(graph.nodes[u],graph.nodes[v]):
        graph.nodes[v].d = graph.nodes[u].d + weightsFromCoords(graph.nodes[u],graph.nodes[v])
        graph.nodes[v].pi = u

# Function to find the weight of the edges, given the x and y coordinates
def weightsFromCoords(node1, node2):
    weight = math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
    return weight

#Helper functions to determine the left and right child of a node, used in minHeapify.
def left(i):
    return 2*i
def right(i):
    return 2*i + 1

#Function that restores the min-heap property, which states that the value
#held by the children needs to be greater than the value held by the parent.
def minHeapify(A, i):
    size = len(A)
    l = left(i)
    r = right(i)
    if (l < size and A[l].d < A[i].d):
        smallest = l
    else:
        smallest = i
    if (r < size and A[r].d < A[smallest].d):
        smallest = r
    if (smallest != i):
        A[i], A[smallest] = A[smallest], A[i]
        minHeapify(A, smallest)
    return A

#Function that builds a min-heap from a list
#It will be used as a priority queue in Dijkstra algorithm.
def buildMinHeap(A):
    heapSize = len(A)
    i = int(math.floor(heapSize/2))
    while i >= 1:
        minHeapify(A, i)
        i = i - 1
    return A

#It extracts the minimum value in the min-heap.
def extractMin(A):
    size = len(A)-1
    if size < 1:
        return None
    minValue = A[1]
    A[1] = A[-1]
    del A[-1]
    minHeapify(A, 1)
    return minValue

def Dijkstra(graph, s, d):
    initSingleSource(graph, s)
    S = []
    Q = copy.copy(graph.nodes)
    paddingNode = Node()
    paddingNode.id = -1
    Q.insert(0, paddingNode)
    Q = buildMinHeap(Q)
    while len(Q)>1:
        u = extractMin(Q)
        S.append(u)
        if d == u:  #first optimization on Dijkstra: as soon as the destnation is reached, return.
            return;
        for v in u.neighbors:
            DijkstraRelax(u, graph.nodes[v])

def DijkstraRelax(u, v):
    if v.d > u.d + weightsFromCoords(u,v):
        v.d = u.d + weightsFromCoords(u,v)
        v.pi = u.id

#Call DAG if the graph is acyclic, Dijkstra otherwise
def findShortestPath(cycle, graph, source, destination):
    #start the running timer
    start = timeit.default_timer()
    print "The source vertex is: ", source
    print "The destination vertex is: ", destination
    if cycle == True:
        Dijkstra(graph, source, destination)
    else:
        shortestPathDAG(graph, source)
    path = []
    path.append(destination)
    distance = graph.nodes[destination].d
    while graph.nodes[destination].pi != None:
        destination = graph.nodes[destination].pi
        path.append(destination)
    if distance == float("inf"):
        print "Destination ", destination, " is not reachable by source ", source
    else:
        print "The total distance of the shortest path is: ", round(distance, 2)
        shortestPath = list(reversed(path))
        print "The sequence of vertices that form the shortest path is: ", shortestPath
        end = timeit.default_timer()    #ends the timer
        print "Run time: ", round((end - start), 8)   #prints time in seconds
        plotPath(graph, shortestPath)

# function to plot the shortest path, as requested in part d.
def plotPath(g, path):
    xcoords = []
    ycoords = []
    dist = []
    length = len(path)
    for element in path:
        xcoords.append(g.nodes[element].x)
        ycoords.append(g.nodes[element].y)
        dist.append(g.nodes[element].d)
    for i in range (length-1):
        dist[i] = dist[i+1] - dist[i]
    plt.plot(xcoords, ycoords)
    plt.xlabel('x')
    plt.ylabel('y')
    for i in range(length - 1):
        plt.text((xcoords[i] + xcoords[i+1])/2,((ycoords[i]+ycoords[i+1])/2), round(dist[i], 2))
    for element in path:
        plt.text(g.nodes[element].x, g.nodes[element].y, element)
    # range of the picture migh need to be adjusted depending on locations of test vertices.
    # this settings work fine with the small test
    p.axis([min(xcoords) - 50 ,max(xcoords) + 50, min(ycoords) - 50,max(ycoords) + 50])
    ax = p.gca()
    ax.set_autoscale_on(False)
    plt.show()

def main():
    readTextFile()
#insert source and destination verices on line 78

if __name__ == "__main__":
    main()
