#   Carlo Scanelli
#   CSCI 3104
#   Summer 2017 - Assignment 4

import math

#Class to hold the information about the nodes
class Node:
    def __init__(self):
        self.freq = None
        self.char = None
        self.right = None
        self.left = None
        self.code = None

#Function that returns a two-dimendional array which stores the characters with their frequencies.
def strToFreq(x):
    adt = {}
    for char in x:
        if char in adt:
            adt[char] += 1
        else:
            adt[char] = 1
    freqVect = list(adt.values())
    charVect = list(adt.keys())
    a = []
    for i in range(len(freqVect)):
        newNode = Node()
        newNode.char = charVect[i]
        newNode.freq = freqVect[i]
        a.append(newNode)
    paddingNode = Node()
    paddingNode.freq = -1
    a.insert(0, paddingNode)
    return a

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
    if (l < size and A[l].freq < A[i].freq):
        smallest = l
    else:
        smallest = i
    if (r < size and A[r].freq < A[smallest].freq):
        smallest = r
    if (smallest != i):
        A[i], A[smallest] = A[smallest], A[i]
        minHeapify(A, smallest)
    return A

#Function that builds a min-heap.
#It will be used as a priority queue in the Huffman algorithm.
def buildMinHeap(A):
    heapSize = len(A)
    i = int(math.floor(heapSize/2))
    while i >= 1:
        minHeapify(A, i)
        i = i - 1
    return A

#Main function of the program. It builds the Huffman tree.
def huffmanEncode(adt):
    length = len(adt)
    q = buildMinHeap(strToFreq(string))
    print('')
    print("Building Huffman Tree: ")
    for i in range(1, length - 1):
        newNode = Node()
        newNode.left = x = extractMin(q)
        print ("xmin:" ,x.freq)
        newNode.right = y = extractMin(q)
        print ("ymin: ", y.freq)
        newNode.freq = x.freq + y.freq
        print ("newNodefreq: ", newNode.freq)
        q.insert(i, newNode)
        minHeapify(q, i)
    print('')
    print ("Huffmann tree total frequency (i.e number of characters before encoding):")
    print q[1].freq
    q[1].code = ""
    huffmanvariable = q[1]
    adt = {}
    print('')
    print("Codebook: ")
    cb = makeCodebook(huffmanvariable, adt)
    print adt
    print('')
    print("Encoded string: ")
    return adt

#Function that builds the codebook, which represents the path you need to
#take to reach a specific character in the Huffmann tree. '0' means go to
#the left child. '1' means go to the right child.
def makeCodebook(curr, adt):
    if (curr.left):
        curr.left.code = curr.code + "0"
        makeCodebook(curr.left, adt)
    if (curr.right):
        curr.right.code = curr.code + "1"
        makeCodebook(curr.right, adt)
    if (curr.right == None and curr.left == None):
        adt[curr.char] = curr.code

#Final funtion which encodes the input string.
def encodeStr(x, codebook):
    text = ""
    for i in codebook:
        text += codebook[i]
    print text

#Helper function needed in the Huffman algorithm. It extracts the minimum
#value in the min-heap.
def extractMin(A):
    size = len(A)-1
    if size < 1:
        return None
    minValue = A[1]
    A[1] = A[-1]
    #size = size - 1
    del A[-1]
    minHeapify(A, 1)
    return minValue

#TEST FUNCTIONS
#note: the name of the input string must be "string"
string3 = "fffffeeeeeeeeeccccccccccccbbbbbbbbbbbbbddddddddddddddddaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
string2 = "ddddcccbba"
string = "Nel mezzo del cammin di nostra vita mi ritrovai per una selva oscura, che la diritta via era smarrita. Ahi quanto a dir qual era e cosa dura esta selva selvaggia e aspra e forte che nel pensier rinova la paura! Tant' e amara che poco e piu morte; ma per trattar del ben ch'i' vi trovai, diro de l'altre cose ch'i' v'ho scorte. Io non so ben ridir com' i' v'intrai, tant' era pien di sonno a quel punto che la verace via abbandonai. Ma poi ch'i' fui al pie d'un colle giunto, la dove terminava quella valle che m'avea di paura il cor compunto, guardai in alto e vidi le sue spalle vestite gia de' raggi del pianeta che mena dritto altrui per ogne calle."
StringToFrequency = strToFreq(string)
MinHeap = buildMinHeap(StringToFrequency)
Encoding = huffmanEncode(MinHeap)
encodeStr(string, Encoding)
