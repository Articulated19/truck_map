#!/usr/bin/env python
from os.path import dirname, abspath
from math import sqrt


# For representing a Node
# A Node object consists of:
#     x, y coordinates for this Node
#     a list of references to other Node objects, to which there is an out-edge from this Node
class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.out_edges = []

    # String representation of a Node object
    def __str__(self):
        to_str = "(" + str(self.x) + ", " + str(self.y) + ") ["
        for n in self.out_edges:
            to_str += "(" + str(n.x) + ", " + str(n.y) + ")"
        to_str += "]"
        return to_str

    # Adds an outgoing edge from this Node to the given Node object
    def addOutEdge(self, node):
        self.out_edges.append(node)

    # Returns the length of an edge between this Node and the given Node object
    def getEdgeLength(self, to_node):
        return sqrt((to_node.x - self.x)**2 + (to_node.y - self.y)**2)


# Takes an array of Node objects and (x,y)-coordinates for a Node
# If there is a Node object with given coordinates in the given array: Returns Node object
# Otherwise returns: None 
def getNodeFromList(nodelist, (x, y)):
    for node in nodelist:
        if node.x == x and node.y == y:
            return node
    return None


# Takes a path (relative to current directory) to a file containing a graph representation
# If parsing was completed without syntax errors: Returns an array of Node objects
# Otherwise: Returns an empty array
def readFileToNodes(path):
    nodes = []
    current_node = None
    dirpath = dirname(abspath(__file__))
    line_counter = 0

    # Variables for validation of syntax
    begin = False
    valid = False

    # Opening the file, parsing the lines one by one
    with open(dirpath + path, 'r') as file:
        for line in file:
            # Line counter, for debugging of input file
            line_counter += 1
            line = line.replace(' ', '')

            # Ignoring comments and empty lines
            if not line.startswith('#') and not line.startswith('\n'):

                # Start of node declaration
                if line == 'NODE\n':
                    if not begin:
                        begin = True
                    else:
                        print 'Syntax error on line ' + str(line_counter)
                        return []

                # End of node declaration
                elif line == 'ENDNODE\n':
                    if begin and current_node:
                        begin = False
                        valid = False
                        current_node = None
                    else:
                        print 'Syntax error on line ' + str(line_counter)
                        return []

                # Coordinates for current Node and its out-edges (connected Nodes)
                elif line[0].isdigit():

                    # Validating syntax
                    if begin:
                        # Removing newline characters and splitting line on list separator ';'
                        array = line.replace('\n', '').split(';')

                        # Out-edges
                        if current_node:
                            for elem in array:
                                elem = elem.split(',')
                                valid = True if len(elem) == 2 and elem[0].isdigit() and elem[1].isdigit() else False
                                if not valid:
                                    break
                                (x, y) = (int(elem[0]), int(elem[1]))
                                # If the connected Node is not already in the node-list, create a new Node object for it
                                outedge = getNodeFromList(nodes, (x, y))
                                if not outedge:
                                    outedge = Node(x, y)
                                    nodes.append(outedge)
                                current_node.addOutEdge(outedge)

                        # Current Node
                        elif len(array) == 1:
                            array = array[0].split(',')
                            valid = True if len(array) == 2 and array[1].isdigit() else False
                            if not valid:
                                break
                            (x, y) = (int(array[0]), int(array[1]))
                            # If the current Node is not already in the node-list, create a new Node object for it
                            current_node = getNodeFromList(nodes, (x, y))
                            if not current_node:
                                current_node = Node(x, y)
                                nodes.append(current_node)

                        # Syntax error
                        else:
                            valid = False

                    # Syntax error
                    if not valid:
                        print 'Syntax error on line ' + str(line_counter)
                        return []

                # Syntax error
                else:
                    print 'Syntax error on line ' + str(line_counter)
                    return []

        return nodes


# Takes a list of Node objects and a filename
# Stores the Node data in a file with given filename
def saveNodesToFile(nodelist, filename):
    with open(filename, 'w') as file:

        for node in nodelist:
            file.write('NODE\n')
            file.write('    ' + str(node.x) + ',' + str(node.y) + '\n')

            for out_edge in node.out_edges[:1]:
                file.write('    ' + str(out_edge.x) + ',' + str(out_edge.y))
            for out_edge in node.out_edges[1:]:
                file.write(' ; ' + str(out_edge.x) + ',' + str(out_edge.y))

            if node.out_edges:
                file.write('\n')
            file.write('ENDNODE\n\n')
