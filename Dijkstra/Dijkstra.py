import math

# Function to read the textFile containing the information about
# the graph.
def readTextFile():
    txtFile = open("smallTest.txt","r") # open the textfile

    firstLine = txtFile.readline()  # reads first line of file
    vAnde = firstLine.split()

    print "Number of vertices: ", vAnde[0]
    print "Number of edges: ", vAnde[1]

    lines = txtFile.readlines() #read every line of file

    print "\nSection 1 - Nodes locations: "
    firstSection = detectSection(lines, 1)  # find first section

    # nodeIDs = []
    # nodeX = []
    # nodeY = []
    # wombocombo = []
    infos = []
    for i in firstSection:  # extract ids, x and y coords, and combine them
        if (i != "\n"):
            #print "i: ", i,
            info = i.split()
            infos.append(info);
    #         idDelimiter = detectWhiteSpace(i, 0)
    #         print "idDelimiter: ", idDelimiter
    #         nodeIDs.append(i[0 :idDelimiter])
    #         xDelimiter = detectWhiteSpace(i, idDelimiter + 1)
    #         print "xDelimiter: ", xDelimiter
    #         nodeX.append(i[idDelimiter + 1 : xDelimiter])
    #         yDelimiter = detectWhiteSpace(i, xDelimiter + 1)
    #         nodeY.append(i[xDelimiter + 1 : yDelimiter])
    #         wombocombo.append((i[0 :idDelimiter], i[idDelimiter + 1 : xDelimiter], i[xDelimiter + 1 : yDelimiter]))
    # # print "Nodes IDs: ", nodeIDs
    # print "X coords: ", nodeX
    # print "Y coords: ", nodeY
    print infos

    firstSectionLength = len(firstSection);
    print "\nSection 2 - connections: "
    secondSection = detectSection(lines, firstSectionLength + 1)

    print findEdges(secondSection)

    secondSectionLength = len(secondSection);
    print "\nSection 3 - tests: "
    thirdSection = detectSection(lines, secondSectionLength + firstSectionLength + 1)
    for i in thirdSection:
        print i,
    txtFile.close() # To free up any system resources taken up by the open file


def findEdges(connectionsList):
    connections = []
    for line in connectionsList:
        if (line != "\n"):
            parts = line.split()
            #print parts
            connections.append((parts[0], parts[1]))
    return connections


    #{(1,2), (3),  }


# def find_path(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return path
#     if not start not in graph:
#         return None
#     for node in graph:
#         if node not in path[start]:
#             newpath = find_path(graph, node, end, path)
#             if newpath: return newpath
#     return None
    # testdict = {}
    # keys = [0, 1]
    # list1 = [1, [3, 4]]
    # testdict[keys] = list1
    # print "testdict :", testdict
    #
    # graphDict = {}
    # # key = edges[0][0]
    # # graphDict[key] = edges[0][1]
    # # print "Dic: ", graphDict
    # # print edges
    # print "length: ", len(edges)
    # startingNodes = []
    # startingNodes.append(edges[0][0])
    # for i in range(0, len(edges)):
    #     if edges[i][0] not in startingNodes:
    #         startingNodes.append(edges[i][0])
    # key = startingNodes
    # multiple = []
    # for i in range(0, len(edges)):
    #     if edges[i][0] in startingNodes:
    #         multiple.append(edges[i][1:-1])
    #
    # graphDict[key] = multiple
    # print "Dic: ", graphDict
    # print "startingNodes: ", startingNodes
def weightsFromCoords(X1, Y1, X2, Y2):
    weight = math.sqrt((X1 - X2)^2 + (Y1 - Y2)^2)
    return weight

# Function to find a whitespace in a given line, starting at index start.
# Retuns the index of the whitespace
def detectWhiteSpace(line, start):
    spaceIndex = line.find(" ", start);
    return spaceIndex


def detectSection(file, start):
    section = []
    length = len(file)
    for i in range(start, length):
        section.append(file[i])
        if (file[i] == "\n"):
            break
    return section

readTextFile()
