#!/usr/bin/env python
from nodes import readFileToNodes, saveNodesToFile

if __name__ == '__main__':
    # n1 = Node(1, 2)
    # n2 = Node(2, 2)
    # n3 = Node(0, 2)
    # n1.addOutEdge(n2)
    # n1.addOutEdge(n3)
    # print "n1: " + str(n1)
    # print n1.getEdgeLength(n2)
    # n2.x = 5
    # print "n1: " + str(n1)
    # print n1.getEdgeLength(n2)

    nodes = readFileToNodes('/graph.txt')
    for node in nodes:
        print node
    saveNodesToFile(nodes, 'test.txt')

