#!/usr/bin/env python
import numpy as np
import cv2
import matplotlib.pyplot as plt
from os.path import dirname, abspath
from math import ceil


IMG_PATH = '/map.png'
SCALE = 10  # Map img is in scale 1:10


# For representing an obstacle on the track
#
# All measurements (including coordinates) are in cm
class Obstacle:

    def __init__(self, x, y, width, height, padding):
        self.x = x  # Lower left corner
        self.y = y  # Lower left corner
        self.width = width
        self.height = height
        self.padding = padding

        self.matrix_backup = []
        self.active = False


# All measurements (including coordinates) are in cm
OBSTACLES = [
        Obstacle(178, 375, 20, 31, 2),
        Obstacle(202, 436, 14, 22, 2),
        Obstacle(147, 686, 100, 100, 1),
        Obstacle(288, 844, 40, 35, 3)
    ]


class Map:

    def __init__(self):
        self.matrix = readImgToMatrix(IMG_PATH)
        self.scale = SCALE
        self.obstacles = OBSTACLES


    def getMapAndScale(self):
        return (self.matrix, self.scale)


    # Takes an Index value
    # Adds the corresponding Obstacle from 'obstacles' to the 'matrix' of this Map
    #
    # If an Obstacle was added:
    #     Returns True
    # If given index is out of bounds, or the corresponding Obstacle is already activated:
    #     Returns False
    def addObstacle(self, index):

        # Checking the validity of the given index
        try:
            obstacle = self.obstacles[index]
        except IndexError:
            print "Obstacle index out of bounds"
            return False

        # If given obstacle is already active, there is no need to add it again
        if obstacle.active:
            return False

        height = int(ceil(obstacle.height))
        width = int(ceil(obstacle.width))
        padding = int(ceil(obstacle.padding))
        (x, y) = (int(obstacle.x), int(obstacle.y))

        # Going through all rows in the matrix
        for i in range(height):
            row = []

            # Going through all elements on each row
            for j in range(width):

                # For storing the old element value in 'matrix_backup' of given obstacle
                row.insert(j, self.matrix[y-i][x+j])

                # If there is padding, adding a grey frame with padding width above and below the obstacle
                if i+1 <= padding or padding > (height-1 - i):
                    self.matrix[y-i][x+j] = 2
                # If there is padding, adding a grey frame with padding width to the left and right of the obstacle
                elif j+1 <= padding or padding > (width-1 - j):
                    self.matrix[y-i][x+j] = 2
                # Adding non-padding area
                else:
                    self.matrix[y-i][x+j] = 0

            # Storing the old element values in 'matrix_backup' of given obstacle
            obstacle.matrix_backup.insert(i, row)
            
        obstacle.active = True
        return True


    # Takes an Index value
    # Removes the corresponding Obstacle from 'obstacles' from the 'matrix' of this Map
    #
    # If an Obstacle was removed:
    #     Returns True
    # If given index is out of bounds, or the corresponding Obstacle is already deactivated:
    #     Returns False
    def removeObstacle(self, index):
        try:
            obstacle = self.obstacles[index]
        except IndexError:
            print "Obstacle index out of bounds"
            return False

        # If given obstacle is Not active, there is no need to reset the matrix
        if not obstacle.active:
            return False

        height = int(ceil(obstacle.height))
        width = int(ceil(obstacle.width))
        padding = int(ceil(obstacle.padding))
        (x, y) = (int(obstacle.x), int(obstacle.y))


        # Using 'matrix_backup' of given obstacle to remove the obstacle
        # and reset the affected section of the matrix:

        # Going through all rows in the matrix
        for i in range(height):

            # Going through all elements on each row
            for j in range(width):
                self.matrix[y-i][x+j] = obstacle.matrix_backup[i][j]

        # Clearing 'backup' of given obstacle
        obstacle.matrix_backup = []
        obstacle.active = False
        return True


    # Takes (x, y)-coordinates for an element
    #
    # Coordinates are assumed to be in cm
    #
    # If given coordinates are valid for the given matrix:
    #     Returns the value of element at given index,
    #     with respect to the scale of the matrix
    # If given coordinates are out of bounds:
    #     Returns None 
    def getValue(self, x, y):
        (ix, iy) = (int(x), int(y))
        try:
            return self.matrix[iy][ix]
        except IndexError:
            print "Map element index out of bounds"
            return None


    # Takes (x, y)-coordinates
    #
    # Coordinates are assumed to be in cm
    #
    # If there is an Obstacle at given position:
    #     Returns the index of that obstacle
    # Otherwise:
    #     Returns None
    def getObstacle(self, x, y):
        (ix, iy) = (int(x), int(y))

        for index, o in enumerate(self.obstacles):
            if ix in range(o.x, o.x + o.width) and iy in range(o.y - (o.height-1), o.y+1):
                # Obstacle found
                return index

        # No obstacle found
        return None


# Takes a path (relative to current directory) to a an image file containing a Map representation
# The file should be in '.png'-format
#
# Returns an array of rows, where each row is an array of elements
def readImgToMatrix(path):
    dirpath = dirname(abspath(__file__))
    matrix = np.asarray(cv2.imread(dirpath + path, 0), dtype=np.uint8).tolist()

    # Going through all elements, adjusting their value to match [0, 1, 2]
    # Where:
    #     0 = Black
    #     1 = White
    #     2 = Grey
    for row in range(len(matrix)):
        for elem in range(len(matrix[row])):
            # Not black
            if matrix[row][elem] != 0:
                # White
                if matrix[row][elem] == 255:
                    matrix[row][elem] = 1
                # Grey
                else:
                    matrix[row][elem] = 2

    #plt.imshow(matrix)
    #plt.show()
    return matrix
