#!/usr/bin/env python
from graph_func import *

import warnings
import _tkinter
from math import sin, cos, radians
import matplotlib.pyplot as plt


GRAPH_PATH = '/graph.txt'


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
        self.indexes = []


    # Takes a VehicleState object, and an array of tuples of (x, y)-coordinates (assumed to be in cm)
    #
    # Calculates the shortest path from vehicle position to the first coordinate point,
    # and from each coordinate point to the next
    #
    # Returns a reference path in the form of an array of tuples of (x, y)-coordinates (in cm),
    # and an array with indexes for the points on the path which coincide with the start point,
    # and the given (x, y)-coordinates
    def getRefPath(self, vehicle_state, pts):

        # Finding the Node (in valid direction) which is closest to the vehicle, to use as a start point
        # Returns [] if the vehicle is too far away from a valid start point
        start_point = getClosestToVehicle(self.graph, vehicle_state)
        if not start_point:
            print "== ERROR: The vehicle is too far away from a valid path"
            return []

        self.path = []
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
                    print "== ERROR: Reference path out of range for %s" % str(point)
                    break

        # Printing status msg
        if self.path == []:
            print "[] returned"
        else:
            print "Path returned"
            print "Path:", self.path

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
    def getAltPath(self, path, start_index, end_index):

        try:
            start_point = Point(*path[start_index])
            end_point = Point(*path[end_index])
        except IndexError:
            print "ERROR: Index out of bounds"
            return None

        alt_paths = altPaths(self.graph, start_point, end_point)

        if alt_paths:
            for i, alt in enumerate(alt_paths):
                alt_paths[i] = path[:start_index] + alt + path[end_index+1:]

            return alt_paths
        else:
            print "No alternative path found"
            return []


# Main, used for testing
if __name__ == '__main__':

    COORDS_VALID = [
        (255.0520833333332, 339.2578125000000),
        (317.8776041666666, 716.210937),
        (260.078125, 856.9401041666667)
    ]

    COORDS_VALID_2 = [(101, 765), (358, 535)]

    COORDS_INVALID = [
        (270.1302083333332, 339.2578125000000),
        (320.390625, 515.1692708333333),
        (413.3723958333332, 686.0546875)  # This point is out of range
    ]


    refpath_obj = RefPath()
    vehicle_state = VehicleState(400, 163, radians(90), 0)
    vehicle_state_2 = VehicleState(237, 869, radians(180), 0)

    # INVALID PATH
    """
    path = refpath_obj.getRefPath(vehicle_state, COORDS_INVALID)
    """

    # VALID PATH
    
    path, indexes = refpath_obj.getRefPath(vehicle_state_2, COORDS_VALID_2)
    alt_paths = refpath_obj.getAltPath(path, indexes[1], indexes[2])
    alt_paths.insert(0, path)

    for alt in alt_paths:
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
