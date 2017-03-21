#!/usr/bin/env python
from os.path import dirname, abspath
from math import sqrt, radians
from enum import Enum
import matplotlib.pyplot as plt


# For representing a Point in a coordinate system
class Point:

    # Takes (x, y)-coordinates for a Point
    def __init__(self, x, y):
        self.x = x
        self.y = y


# For representing a Directed Graph
# A Graph object consists of:
#     a list of Node objects
class Graph:

    # Takes an array of Node objects, which make up the Graph (optional)
    def __init__(self, nodes=None):
        self.nodes = nodes if nodes else []

    # String representation of a Graph object
    def __str__(self):
        to_str = ""
        for node in self.nodes[:-1]:
            to_str += "%s\n" % (node)
        if len(self.nodes) > 0:
            to_str += "%s" % (self.nodes[-1])
        return to_str

    # Takes another Graph object
    # Adds all Nodes from that Graph to this Graph (without creating duplicates)
    def addGraph(self, graph):
        for node in graph.nodes:
            self.addNode(node)

    # Takes a Node object
    # Adds that Node to this Graph (without creating duplicates)
    def addNode(self, node):
        current_node = self.getNode(node.x, node.y)
        if current_node:
            for e in node.out_edges:
                self.addNode(e)
                current_node.addOutEdge(e)
        else:
            self.nodes.append(node)

    # Takes (x, y)-coordinates for a Node
    # If there is a Node object with given coordinates in this Graph:
    #     Returns that Node object
    # Otherwise:
    #     Reurns None 
    def getNode(self, x, y):
        for node in self.nodes:
            if node.x == x and node.y == y:
                # Node object found
                return node
        # Node object Not found
        return None


# For representing a Node
# A Node object consists of:
#     (x, y)-coordinates for this Node
#     a list of references to other Node objects, to which there is an out-edge from this Node
class Node:

    # Takes (x, y)-coordinates for this Node
    # and an array of Node objects, to which there is an out-edge from this Node (optional)
    def __init__(self, x, y, out_edges=None):
        self.x = x
        self.y = y
        self.out_edges = out_edges if out_edges else []

    # String representation of a Node object
    def __str__(self):
        to_str = "(%s, %s) [" % (self.x, self.y)
        for node in self.out_edges[:-1]:
            to_str += "(%s, %s) " % (node.x, node.y)
        if len(self.out_edges) > 0:
            to_str += "(%s, %s)" % (self.out_edges[-1].x, self.out_edges[-1].y)
        to_str += "]"
        return to_str

    # Adds an outgoing edge from this Node to the given Node object (without creating duplicates)
    def addOutEdge(self, node):
        out_edge = self.getOutEdge(node.x, node.y)
        if not out_edge:
            self.out_edges.append(node)

    # Takes (x,y)-coordinates for a Node
    # If there is a Node object with given coordinates in the out-edges from this Node:
    #     Returns that Node object
    # Otherwise:
    #     Reurns None 
    def getOutEdge(self, x, y):
        for node in self.out_edges:
            if node.x == x and node.y == y:
                # Node object found
                return node
        # Node object Not found
        return None

    # Returns the length of an edge between this Node and the given Node object
    def getEdgeLength(self, to_node):
        return sqrt((to_node.x - self.x)**2 + (to_node.y - self.y)**2)


# Takes a path (relative to current directory) to a text file containing a Graph representation
# The textfile should be in the format specified in 'example_graph.txt'
#
# If parsing was completed without syntax errors:
#     Returns a Graph object with all nodes in its nodelist
# Otherwise:
#     Returns None
def readFileToGraph(path):
    graph = Graph()
    current_node = None
    dirpath = dirname(abspath(__file__))
    line_counter = 0

    # Variables for validation of syntax
    begin = False
    valid = False

    # Opening the file, parsing the lines one by one
    with open(dirpath + path, "r") as file:
        for line in file:
            # Line counter, for debugging of input file
            line_counter += 1
            # Removing whitespaces and tabs
            line = line.replace(" ", "")
            line = line.replace("\t", "")

            # Ignoring comments and empty lines
            if not line.startswith("#") and not line.startswith("\n"):

                # Start of node declaration
                if line == "NODE\n":
                    if not begin:
                        begin = True
                    else:
                        print "Syntax error on line %s in '%s'" % (line_counter, path)
                        return None

                # End of node declaration
                elif line == "ENDNODE\n":
                    if begin and current_node:
                        begin = False
                        valid = False
                        current_node = None
                    else:
                        print "Syntax error on line %s in '%s'" % (line_counter, path)
                        return None

                # Coordinates for current Node and its out-edges (connected Nodes)
                elif line[0].isdigit():

                    # Validating syntax
                    if begin:
                        # Removing newline characters and splitting line on list separator ';'
                        array = line.replace("\n", "").split(";")

                        # Out-edges
                        if current_node:
                            for elem in array:
                                elem = elem.split(",")
                                valid = True if len(elem) == 2 and elem[0].isdigit() and elem[1].isdigit() else False
                                # Break on Syntax error
                                if not valid:
                                    break

                                (x, y) = (int(elem[0]), int(elem[1]))
                                # If the connected Node is not already in the node-list, create a new Node object for it
                                outedge = graph.getNode(x, y)
                                if not outedge:
                                    outedge = Node(x, y)
                                    graph.addNode(outedge)
                                current_node.addOutEdge(outedge)

                        # Current Node
                        elif len(array) == 1:
                            elem = array[0].split(",")
                            valid = True if len(elem) == 2 and elem[1].isdigit() else False
                            # Break on Syntax error
                            if not valid:
                                break

                            (x, y) = (int(elem[0]), int(elem[1]))
                            # If the current Node is not already in the node-list, create a new Node object for it
                            current_node = graph.getNode(x, y)
                            if not current_node:
                                current_node = Node(x, y)
                                graph.addNode(current_node)

                        # Syntax error
                        else:
                            valid = False

                    # Syntax error
                    if not valid:
                        print "Syntax error on line %s in '%s'" % (line_counter, path)
                        return None

                # Syntax error
                else:
                    print "Syntax error on line %s in '%s'" % (line_counter, path)
                    return None

        return graph


# Takes a Graph and a filename
# Stores the Graph data in a file with given filename,
# in a format that can be re-read by using 'readFileToGraph(path_to_savefile)'
def saveGraphToFile(graph, filename):
    with open(filename, "w") as file:

        for node in graph.nodes:
            file.write("NODE\n")
            file.write("    %s,%s\n" % (node.x, node.y))

            for out_edge in node.out_edges[:1]:
                file.write("    %s,%s" % (out_edge.x, out_edge.y))
            for out_edge in node.out_edges[1:]:
                file.write(" ; %s,%s" % (out_edge.x, out_edge.y))

            if node.out_edges:
                file.write("\n")
            file.write("ENDNODE\n\n")


# Takes an array of Point objects
# Returns a Directed Graph, with an edge from each Point to the next one in the array
def pointsToGraph(points):
    graph = Graph()

    # Creating Node objects for all points
    for point in points:
        graph.addNode(Node(point.x, point.y))
    
    # Creating an edge from each Node to the next one in the array
    for i in range(len(points)-1):
        current_node = graph.getNode(points[i].x, points[i].y)
        next_node = graph.getNode(points[i+1].x, points[i+1].y)
        current_node.addOutEdge(next_node)

    return graph


# Takes a Graph, two Points with (x, y)-coordinates for start and end point, 
# and vehicle angle (in degrees)
# Returns the shortest path between start and end point
def shortestPath(graph, start, end, theta):

    # Returns an array with all Nodes that are in range (set by 'limit') x-wise from given Point
    def getAllInRangeX(nodes, limit, point):
        node_list = []
        for node in nodes:
            # Ignoring all nodes that are not in range x-wise
            if node.x >= point.x-limit and node.x <= point.x+limit:
                node_list.append(node)
        return node_list

    # Returns an array with all Nodes that are in range (set by 'limit') y-wise from given Point
    def getAllInRangeY(nodes, limit, point):
        node_list = []
        for node in nodes:
            # Ignoring all nodes that are not in range y-wise
            if node.y >= point.y-limit and node.y <= point.y+limit:
                node_list.append(node)
        return node_list


    # Used to specify search range for finding closest point
    limit = 150
    # Normalizing theta:
    theta = theta % 360

    # Connecting start and end point to the Graph, in an optimal way
    # Vehicle direction: bottom-to-top
    if theta > 45 and theta <= 135:
        # Hitta alla inom limit i x-led, sen narmast under i y-led
        print 'bottom-to-top'
    # Vehicle direction: right-to-left
    elif theta > 135 and theta <= 225:
        # Hitta alla inom 20 i y-led, sen narmast over i x-led
        print 'right-to-left'
    # Vehicle direction: top-to-bottom
    elif theta > 225 and theta <= 315:
        #Hitta alla inom 20 i x-led, sen narmast over i y-led
        print 'top-to-bottom'
    # Vehicle direction: left-to-right
    elif theta > 315 or theta <=45:
        # Hitta alla inom 20 i y-led, sen narmast under i x-led
        print 'left-to-right'

        return nearest_node


# For plotting a Graph
def plotGraph(graph):
    print "Plotting graph"

    # Graph settings
    plt.axis('scaled')
    plt.xlim( (0, 5000) )
    plt.ylim( (9000, 0) )

    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.title('Graph')

    ax = plt.axes()
    plt.grid(True)

    # Plotting all egraph edges
    for node in graph.nodes:
        for out_edge in node.out_edges:
            dx = out_edge.x - node.x
            dy = out_edge.y - node.y
            ax.arrow(node.x, node.y, dx, dy, head_width=60, head_length=60, fc='b', ec='b')
    #plt.show()
