#!/usr/bin/env python
from shortest_path import *

import warnings
import _tkinter
from math import sin, cos, radians
import matplotlib.pyplot as plt


GRAPH_PATH = '/graph.txt'
ALT_PATHS = 50  # Maximum number of alternative paths to search for


class VehicleState:

    def __init__(self, x, y, theta1, theta2):
        self.x = x              # x, y coordinates in cm
        self.y = y
        self.theta1 = theta1    # angles in radians
        self.theta2 = theta2


class RefPath:

    def __init__(self):
        self.graph = readFileToGraph(GRAPH_PATH)
        self.path = []
        self.alt_paths = ([], 0, 0)
        self.indexes = []


    # Takes a VehicleState object, and an array of tuples of (x, y)-coordinates (assumed to be in cm)
    #
    # Calculates the shortest path from vehicle position to the first coordinate point,
    # and from each coordinate point to the next
    #
    # If a path could be created:
    #     Returns a reference path in the form of an array of tuples of (x, y)-coordinates (in cm),
    #     and an array with indexes for the points on the path which coincide with the start point,
    #     and the given (x, y)-coordinates
    # Otherwise:
    #     Returns [], []
    def getRefPath(self, vehicle_state, pts):

        # Finding the Node (in valid direction) which is closest to the vehicle, to use as a start point
        start_point = getClosestToVehicle(self.graph, vehicle_state)
        # Returns [], [] if the vehicle is too far away from a valid start point
        if not start_point:
            print "== ERROR: The vehicle is too far away from a valid path"
            return [], []

        self.path = []
        self.alt_paths = ([], 0, 0)
        self.indexes = []

        # Adding 'start_point' first in 'pts'
        pts.insert(0, (start_point.x, start_point.y))

        # If at least one coordinate point was given
        if len(pts) > 1:
            # Adding start point to path
            self.path.append((start_point.x, start_point.y))
            self.indexes.append(0)

            # Calculating shortest path between the points
            for point in pts[1:]:
                path = shortestPath(self.graph, start_point, Point(point[0], point[1]))
                if path != None:
                    self.path += path[1:]
                    self.indexes.append(len(self.path)-1)
                    start_point = Point(self.path[-1][0], self.path[-1][1])

                # If the given coordinate points were not in range of any Nodes
                else:
                    self.path = []
                    self.indexes = []
                    print "== ERROR: Reference path out of range for %s" % str(point)
                    break

        # Printing status msg
        if self.path == []:
            print "[] returned"
        else:
            print "Path returned"
            #print "Path:", self.path

        return self.path, self.indexes


    # Takes a path (as returned by getRefPath()),
    # and indexes for the start resp. end point for the segment which should be replaced
    #
    # If the given parameters are invalid:
    #     Returns None
    # If there is at least one alternative path between the given start and end points:
    #     Returns an array of paths, sorted in increasing order of length,
    #     with the segement between given start and end points replaced with each of the alternative paths found
    # Otherwise:
    #     Returns []
    def getAltPaths(self, path, start_index, end_index):

        # Checking validity of given indexes
        try:
            start_point = Point(*path[start_index])
            end_point = Point(*path[end_index])
        except IndexError:
            print "ERROR: Index out of bounds"
            return None

        alt_paths = altPaths(self.graph, start_point, end_point, ALT_PATHS)

        if alt_paths:
            for i, alt in enumerate(alt_paths):
                alt_paths[i] = path[:start_index] + alt + path[end_index+1:]
        else:
            alt_paths = []
            print "No alternative path found"
        
        self.path = path
        self.alt_paths = (alt_paths, start_index, end_index)
        return alt_paths


    # Takes a path (as returned by getRefPath()),
    # indexes for the start resp. end point for the segment which should be replaced,
    # and a number (>= 1) specifying which alternative path to use
    # ('nth'=1 for the first alternative path, 'nth'=2 for the second, etc.)
    #
    # If the given parameters are invalid:
    #     Returns None
    # If there is a nth alternative path between the given start and end points:
    #     Returns the given path, with the segement between given start and end points replaced with an alternative path
    # Otherwise:
    #     Returns []
    def getAltPath(self, path, start_index, end_index, nth):

        # Checking validity of given 'nth'-value
        if nth < 1:
            print "ERROR: Invalid value for parameter 'nth'"
            return None

        alt = self.alt_paths

        # If the complete set of alternative paths have already been computed for the given parameters,
        if path == self.path and alt[0] and start_index == alt[1] and end_index == alt[2]:
            alt_paths = alt[0]
        else:
            alt_paths = self.getAltPaths(path, start_index, end_index)

        try:
            return alt_paths[nth-1]
        except IndexError:
            print "There is no '%s'-alternative path" % nth
            return []


# Main, used for testing
if __name__ == '__main__':

    COORDS = [(101, 765), (358, 535)]

    refpath_obj = RefPath()
    vehicle_state = VehicleState(237, 869, radians(180), 0)
    
    path, indexes = refpath_obj.getRefPath(vehicle_state, COORDS)

    for i in range(1, 100):
        alt = refpath_obj.getAltPath(path, indexes[1], indexes[2], i)

        # Plotting graph
        plt.axis('scaled')
        plt.xlim( (0, 490) )
        plt.ylim( (965, 0) )
        plotGraph(refpath_obj.graph, 'b')

        # Plotting path
        xs = map(lambda x: x[0], alt)
        ys = map(lambda x: x[1], alt)
        plt.plot(xs, ys, '-r', linewidth=3.0)

        plt.show()
        next_alt = refpath_obj.getAltPath(path, indexes[1], indexes[2], i+1)
        if not next_alt: break
