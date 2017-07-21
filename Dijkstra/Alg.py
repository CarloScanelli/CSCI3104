# Python program that reads a directed, weighted graph from a file and constructs the graph
import glob
import sys
import math
import copy
import string

end = 0
def readGraph(file):
        graph = {}
        f = open(file, 'r')     #open the file
        for lines in f:
            line = lines.split()    #read lines from file
            v = int(''.join(line[0:1]).replace(":",""))     #get start vertex
            e = line[1:]
            ed = {int(e[i]):int(e[i+1]) for i in range(0, len(e),2)}    #get end vertex and weights
            graph[v] = ed   #add edge to the graph
        f.close()
        return graph

def dijkstra(graph, start):
        if start not in graph:  #check if start vertex exists
                print("Start vertex not found")
                return
        if end not in graph:    #check if end vertex exists
                print("End vertex not found")
                return
        calculatePathWeight(graph, start, {}, {}, [])     #calculate shortest path and weight

def calculatePathWeight(graph, start, distances, predecessors, visited):
        if start == end:
                if(distances == {} and predecessors == {} and visited == []):   #check if the start and end vertices are the same
                    print("start and end vertices are the same")
                    return
                path=[]
                pred=end
                while pred != None:     #add to the path
                        path.append(pred)
                        pred=predecessors.get(pred,None)
                path.reverse()
                print("path: " + str(path) + " weight: " + str(distances[end]))
        else:
                if not visited:     #initialize the weight
                        distances[start]=0
                for connected in graph[start]:  #check connected vertices
                        if connected not in visited:
                                new_distance = distances[start] + int(graph[start][connected])
                                if new_distance < distances.get(connected,float('inf')):
                                        distances[connected] = new_distance
                                        predecessors[connected] = start
                visited.append(start)   #mark as visited vertex
                pending = {}
                for v in graph:     #for those not visited, make the pending list
                        if v not in visited:
                                pending[v] = distances.get(v,float('inf'))
                m = min(pending, key=pending.get)
                if(pending[m] == float('inf')):     #check for not reachable vertex
                        print("not reachable")
                        return
                calculatePathWeight(graph, m, distances, predecessors, visited)

def main():
        global end
        file = "smallTest.txt"
        graph = readGraph(file)
        while(1):   #keep asking for two vertices endlessly
                start = int(input("\n\ninput start vertex, press return "))
                end = int(input("input end vertex, press return "))
                print()
                dijkstra(graph, start)
main()
