Enter file contents here
# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 
# each node represents a building
# each edge represents a directional route with a total distance and an outdoor distance
# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    print "Loading map from file..."
    myGraph = WeightedDigraph()
    sourceNode=0;
    destNode=0;
    totalDist=0;
    outsideDist=0
    with open(mapFilename) as f:
        for line in f:
            values = line.split()
            sourceNode=Node(values[0])
            destNode=Node(values[1])
            totalDist=values[2]
            outsideDist=values[3]
            try:
                myGraph.addNode(sourceNode)
            except ValueError as E:
                pass
            try:
                myGraph.addNode(destNode)
            except ValueError as E:
                pass
            myEdge = WeightedEdge(sourceNode,destNode,totalDist,outsideDist)
            try:
                myGraph.addEdge(myEdge)
            except ValueError as E:
                pass
    return myGraph
            
            
    

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
# find the shortest path from start to end
#     constraint - do not exceed the max outdoor dist
#     raise error if no path exists
def getEdge(graph, start, end):
    myEdges = graph.edges[start]
    #print "---Looking for edge -- source:", start, " end: ", end
    #print "myEdges: ",myEdges
    #print "source : ", start   
    for edge in myEdges:
     #   print "Edge.getDestination: ", edge.getDestination()
      #  print "edge: ", edge
        if edge.getDestination()==end:
            return edge
    raise ValueError("edge not found")
    return None
def getTotalDistance(graph, path):
    totalDistance=0
    i=0
    while i < len(path)-1:
        myEdge = getEdge(graph,path[i],path[i+1])
        totalDistance+=myEdge.getTotalDistance()
    return totalDistance;
    
def DFS(graph, start, end,maxTotal,maxOutdoors,curTotal=0,curOut=0,path = [],allToEndPaths=[],level=0):
    level+=1
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    #print "current path: ", path
    path = path + [start]
    #print 'updated dfs path:', path
    if start == end:
        #print "*Found End path: ", path
        #print "curTotal: ",curTotal
        pathAndLength=(path,curTotal)
        
        allToEndPaths.append(pathAndLength)
        
    #print "for node in graph children of start: ", start
    #print "children of ",start, " : ",graph.childrenOf(start)
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            #print "-------for level:",level,"---------"
            #print "child node is : ",node
            myEdge = getEdge(graph,start,node)
            myEdgeTotalDist=myEdge.getTotalDistance()
     #       print "cur total before updte: ", curTotal
      #      print "---->edge: ", myEdge
       #     print "---->myEdgeTotalDist: ",myEdgeTotalDist
            #print "level: ", level
            #print "edge start: ", start," end:",node
            myEdgeOutDist=myEdge.getOutdoorDistance()
            
            
            curOutdoor = myEdgeOutDist+curOut
            #print "curOutdoor: ",curOutdoor
            if curTotal+myEdgeTotalDist < maxTotal and curOutdoor+myEdgeOutDist < maxOutdoors :
                newTotal=curTotal+myEdgeTotalDist
        
                #print "curTotal after update: ", newTotal
                newOutDoor=curOutdoor+myEdgeOutDist
                
                #print "go deeper"
                #print "current path: ", path
            #else:
             #   print "over maxTotal or maxOutDoors"
             #   raise ValueError('Duplicate node')
             #if curTotal <= bestPath length
                #if level > 4:
                    #raise ValueError("test")
                DFS(graph,node,end,maxTotal,maxOutdoors,newTotal,newOutDoor,path,allToEndPaths,level)
                
    
    
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):  
    
    allPaths=[]  
    DFS(digraph,start, end,maxTotalDist,maxDistOutdoors,0,0,[],allPaths);
    #print "all Paths: ", allPaths
    minPath=[]
    minPathLength=0
    for pathAndLength in allPaths:
        #print "pathAndLength: ", pathAndLength
        if minPath==[]:
            minPath=pathAndLength[0]
            minPathLength=pathAndLength[1]
        else:
            length = pathAndLength[1]
            if length < minPathLength:
                minPath=pathAndLength[0]
            #print "minpath: ", minPath
            #print "minPathLength: ",minPathLength
            #print "pathAndLength[0]: ",pathAndLength[0]
            #print "pathAndLength[1]: ",pathAndLength[1]
            #raise ValueError("done")
    return minPath    
   # paths=DFS(digraph,start,end,maxTotalDist,maxDistOutdoors)
    
    
    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
"""
mitMap = load_map("mit_map.txt")
print isinstance(mitMap,Digraph)   
print isinstance(mitMap,WeightedDigraph)
nodes = mitMap.nodes
print nodes
edges = mitMap.edges
print edges    

shortest  =bruteForceSearch(digraph,32,56,500,400)
"""
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    
        #Test cases
    mitMap = load_map("mit_map.txt")
    LARGE_DIST = 1000000
    """print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges
    """
    
    
    
    #Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    #     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    #     print "DFS: ", dfsPath1
    #     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)
    """
    #Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    #dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    
    
#     Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)
    

# Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)
    
#     Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr
    """
