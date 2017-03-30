#!/usr/bin/env python
from graph_func import *
from map_func import *

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


    # Takes a VehicleState object, and an array of tuples of (x, y)-coordinates (assumed to be in cm)
    #
    # Calculates the shortest path from vehicle position to the first coordinate point,
    # and from each coordinate point to the next
    #
    # Returns a reference path in the form of an array of tuples of (x, y)-coordinates (in cm)
    def getRefPath(self, vehicle_state, pts):

        # Finding the Node (in valid direction) which is closest to the vehicle, to use as a start point
        # Returns [] if the vehicle is too far away from a valid start point
        start_point = getClosestToVehicle(self.graph, vehicle_state)
        if not start_point:
            print "== ERROR: The vehicle is too far away from a valid path"
            return []

        self.path = []

        # Adding 'start_point' first in 'pts'
        pts.insert(0, (start_point.x, start_point.y))

        # If at least one coordinate point was given
        if len(pts) > 1:
            # Adding start point to path
            self.path.append((start_point.x, start_point.y))

            # Calculating shortest path between the points
            for point in pts[1:]:
                path = shortestPath(self.graph, start_point, Point(point[0], point[1]))
                if path != None:
                    self.path += path[1:]
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

        return self.path


# Main, used for testing
if __name__ == '__main__':

    COORDS_VALID = [
        (255.0520833333332, 339.2578125000000),
        (317.8776041666666, 716.210937),
        (260.078125, 856.9401041666667)
    ]

    COORDS_INVALID = [
        (270.1302083333332, 339.2578125000000),
        (320.390625, 515.1692708333333),
        (413.3723958333332, 686.0546875)  # This point is out of range
    ]

    refpath_obj = RefPath()
    vehicle_state = VehicleState(400, 163, radians(90), 0)

    # INVALID PATH
    """
    path = refpath_obj.getRefPath(vehicle_state, COORDS_INVALID)
    """

    # VALID PATH
    
    path = refpath_obj.getRefPath(vehicle_state, COORDS_VALID)

    # Plotting graph
    plt.axis('scaled')
    plt.xlim( (0, 490) )
    plt.ylim( (965, 0) )
    plotGraph(refpath_obj.graph, 'b')

    # Plotting path
    xs = map(lambda x: x[0], path)
    ys = map(lambda x: x[1], path)
    plt.plot(xs, ys, '-r', linewidth=3.0)

    plt.show()
