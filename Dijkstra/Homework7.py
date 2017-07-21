import operator
class Vertex:
	def __init__(self,vertexid,x,y):
		self.vertexid = int(vertexid)
		self.x = int(x)
		self.y = int(y)
		self.vertexFriend = []
	def __str__(self):
		return "Node "+str(self.vertexid)+" at ("+str(self.x)+","+str(self.y)+") with neighbor(s) "+str(self.vertexFriend)
	def __repr__(self):
		return self.__str__()

class Graph:
	def __init__(self,vertex):
		self.edge = None
		self.vertex = vertex
		self.weight = None


test = open("smallTest.txt","r")
#this = test.read()
this2 = test.readline()
this3 = this2.split(" ")
#print this
#print this2
print ""
print "There are", int(this3[0]), "vertices and", int(this3[1]), "edges", "in this graph."

allLines = test.readlines()
#print allLines
#print "++++++++++++)"
#print allLines
#print "+++++++++++++"

Vertices = []
for i in range(1, int(this3[0])+1):
	#print allLines[i]
	vertexData = allLines[i].split(" ")
	#print vertexData
	newVertex = Vertex(vertexData[0],vertexData[1],vertexData[2])
	Vertices.append(newVertex)
Vertices.sort(key=operator.attrgetter('vertexid'))
'''print " "
print Vertices
print " "
print vertexData'''
print " "
for i in range(int(this3[0])+1+1, int(this3[0])+1+1+int(this3[1])):
	vertexData = allLines[i].split(" ")
	#print str(i)+", "+str(allLines[i])
	Vertices[int(vertexData[0])].vertexFriend.append(int(vertexData[1]))

print Vertices
print " "
