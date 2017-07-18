# Function to read the textFile containing the information about
# the graph. Detects and stores in separate variables the number
# of nodes and the number of edges present in the graph.
def readTextFile():
    txtFile = open("smallTest.txt","r") # open the textfile

    firstLine = txtFile.readline()  # reads first line of file

    space = detectWhiteSpace(firstLine, 0)  # find the first space in the first line
    vertices = firstLine[0:space]           # Get number of nodes
    print "Vertices: ", vertices

    space2 = detectWhiteSpace(firstLine, space) # find the second space, which
                                                # in case of the first line is the
                                                # end of the line.

    edges = firstLine[space:space2]             # Find number of edges
    print "Edges: ", edges

    lines = txtFile.readlines() #read every line of file
    firstSection = detectSection(lines, 1)
    for i in firstSection:
        print i,
    firstSectionLength = len(firstSection);

    print "Section 2: "
    secondSection = detectSection(lines, firstSectionLength + 1)
    for i in secondSection:
        print i,

    print "Section 3: "
    secondSectionLength = len(secondSection);
    thirdSection = detectSection(lines, secondSectionLength + firstSectionLength + 1)
    for i in thirdSection:
        print i,
    txtFile.close() # To free up any system resources taken up by the open file


# Function to determine a whitespace in a given line, starting at index start.
# Retuns the index of the whitespace + 1.
def detectWhiteSpace(line, start):
    counter = 0
    size = len(line) - start
    for i in range(start, size - 1):
        counter = counter + start + 1
        if line[i] == ' ':
            spaceIndex = counter + start
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
