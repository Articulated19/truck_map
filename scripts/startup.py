#!/usr/bin/env python
from graph_func import *
from map_func import *

import matplotlib.pyplot as plt
from PIL import Image
from os.path import dirname, abspath

from graphpoints import *


IMG_PATH = "/map.png"
GRAPH_PATH = "/graph.txt"
SCALE = 10


class Start:

    def __init__(self):
        dirpath = dirname(abspath(__file__))
        map_img = Image.open(dirpath + IMG_PATH)

        self.map_img = map_img.resize((map_img.size[0]*SCALE, map_img.size[1]*SCALE), Image.ANTIALIAS)
        self.graph = readFileToGraph(GRAPH_PATH)

    def plot(self):
        xlim = self.map_img.size[0]
        ylim = self.map_img.size[1]

        # Graph settings
        plt.axis('scaled')
        plt.xlim( (0, xlim) )
        plt.ylim( (ylim, 0) )

        plt.xlabel('x-axis')
        plt.ylabel('y-axis')
        plt.title('Start')

        # Displaying map image
        plt.imshow(self.map_img)
        # Plotting graph
        plotGraph(self.graph, "b")

        plt.show()


if __name__ == '__main__':
    start = Start()
    start.plot()
