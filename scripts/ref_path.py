#!/usr/bin/env python
from graph_func import *
from map_func import *

import matplotlib.pyplot as plt
from pylab import ginput
from PIL import Image

from os.path import dirname, abspath
import warnings
import _tkinter
import gc
from math import sin, cos, radians

#import time


IMG_PATH = "/map.png"
GRAPH_PATH = "/graph.txt"
SCALE = 10



START = Point(766, 3317)
END = Point(1193, 3342)



class VehicleState:

    def __init__(self, x, y, theta_1, theta_2=0):
        self.x = x
        self.y = y
        self.theta_1 = theta_1
        self.theta_2 = theta_2


class RefPath:

    def __init__(self):
        dirpath = dirname(abspath(__file__))
        map_img = Image.open(dirpath + IMG_PATH)

        self.map_img = map_img.resize((map_img.size[0]*SCALE, map_img.size[1]*SCALE), Image.ANTIALIAS)
        self.graph = readFileToGraph(GRAPH_PATH)
        self.path = []

        # To handle user input
        self.keypress = False

    # Handler for 'key_press_event'
    def onKeyPress(self, event):
        # Enter (accepting path)
        if event.key == "enter":
            self.keypress = True
            plt.close()
        # Backspace (discarding path)
        elif event.key == "backspace":
            self.keypress = True
            self.path = None
            plt.close()
            print "Path discarded\n====="

    # Handler for 'close_event'
    def onExit(self, event):
        if not self.keypress:
            self.path = []

    # Takes a VehicleState object,
    # and an array of tuples of (x, y)-coordinates (optional)
    # Lets user input destination and calculates the shortest path to that destination
    # Returns a reference path in the form of an array of tuples of (x, y)-coordinates
    def getRefPath(self, vehicle_state, pts=None):
        theta = vehicle_state.theta_1
        vx, vy = vehicle_state.x, vehicle_state.y
        dx = 300 * cos(radians(theta))
        dy = -300 * sin(radians(theta))

        # Finding the Node (in valid direction) which is closest to the vehicle,
        # to use as a start point
        # If the vehicle is too far away from a valid start point,
        # returns []
        start_point = getClosestToVehicle(self.graph, vehicle_state)
        if not start_point:
            print "The vehicle is too far away from a valid path"
            return []

        print ("Left click on the image to select points\n" +
              "Right click to undo the last point\n" +
              "Middle button to create the path")

        xlim = self.map_img.size[0]
        ylim = self.map_img.size[1]

        fig = plt.figure()
        ax = plt.axes()

        # Graph settings
        plt.axis("scaled")
        plt.xlim( (0, xlim) )
        plt.ylim( (ylim, 0) )
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.title("getRefPath()")

        # Displaying map image
        plt.imshow(self.map_img)
        # Plotting graph
        plotGraph(self.graph, "b")
        # Plotting vehicle position and direction
        plt.plot(vx, vy, "ob", markersize=10)
        ax.arrow(vx, vy, dx, dy, linewidth=2, head_width=100, head_length=120, fc="b", ec="b")
        # Plotting start point
        plt.plot(start_point.x, start_point.y, "or", markersize = 5)

        key_handler = None
        valid = False
        # Repeating until a valid path is created
        while not valid:
            fig.canvas.mpl_connect("close_event", self.onExit)
            fig.canvas.mpl_disconnect(key_handler)
            self.path = []
            self.keypress = False

            # If 'pts' was Not given as an argument
            if not pts:
                # Gathering input
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    try:
                        pts = ginput(n=0, timeout=0, mouse_add=1, mouse_pop=3, mouse_stop=2)
                    except _tkinter.TclError:
                        return []

            # Adding 'start_point' to 'pts'
            pts.insert(0, (start_point.x, start_point.y))

            # If at least one point was inputted
            if len(pts) > 1:
                valid = True
                start = pts[0]

            # Calculating shortest path between the points
            for point in pts[1:]:
                path = shortestPath(self.graph, Point(start[0], start[1]), Point(point[0], point[1]))
                if path:
                    self.path += path
                    start = point

                # If the given points were not in range of any Nodes,
                # setting 'valid' to False to let user retry
                else:
                    valid = False
                    print "=====\nA path could not be created, please input new points"
                    break

            # If a valid path was created,
            # letting user decide whether to keep or discard the path
            if valid:
                # Plotting the path
                xs = map(lambda x: x[0], self.path)
                ys = map(lambda x: x[1], self.path)
                plt.plot(xs, ys, "-r", linewidth=2.0)
                key_handler = fig.canvas.mpl_connect("key_press_event", self.onKeyPress)
                print "=====\nPress 'Enter' to keep the path, and 'Backspace' to discard"
                plt.show()

            pts = None

        return self.path


# Takesa RefPath object and a  a VehicleState object
# Lets user input destination and calculates the shortest path to that destination
# Returns a reference path in the form of an array of tuples of (x, y)-coordinates
def getRefPath(refpath_obj, vehicle_state):
    path = None

    # Repeats until user is satisfied with the path
    while path == None:
        path = refpath_obj.getRefPath(vehicle_state)

    if path == []:
        print "[] returned"
    else:
        print "Path returned"

    return path


if __name__ == "__main__":
    refpath_obj = RefPath()
    vehicle_state = VehicleState(2770, 1430, -90)
    
    getRefPath(refpath_obj, vehicle_state)

    del refpath_obj
    gc.collect()    
