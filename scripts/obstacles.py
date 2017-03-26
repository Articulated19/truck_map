#!/usr/bin/env python
from map_func import *

from os.path import dirname, abspath
from PIL import Image


IMG_PATH = "/map.png"


class ObstacleHandler:

    def __init__(self, map_obj):
        dirpath = dirname(abspath(__file__))
        map_img = Image.open(dirpath + IMG_PATH)

        self.map = map_obj
        self.map_img = map_img.resize((map_img.size[0]*SCALE, map_img.size[1]*SCALE), Image.ANTIALIAS)

        # To handle user input
        self.ax = None
        self.fig = None


    # Handler for 'key_press_event'
    def onKeyPress(self, event):
        if event.key.isdigit():
            self.map.addObstacle(event.key)
        # Enter (accepting path)
        #if event.key == "enter":


    # Lets user activate/deactivate obstacles on the 'map' of this handler
    def handleObstacles(self):
        xlim = self.map_img.size[0]
        ylim = self.map_img.size[1]

        self.fig = plt.figure()
        self.ax = plt.axes()

        # Graph settings
        plt.axis("scaled")
        plt.xlim( (0, xlim) )
        plt.ylim( (ylim, 0) )
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        plt.title("handleObstacles()")

        # Displaying map image
        plt.imshow(self.map_img)

        print ("=====\nRed obstacles are activated, Blue obstacles are deactivated\n" +
               "Press the corresponding number key, to activate/deactivate an obstacle")

        self.fig.canvas.mpl_connect("key_press_event", self.onKeyPress)

        plt.show()


# Main, used for testing
if __name__ == "__main__":
    map_obj = Map()
    handler_obj = ObstacleHandler(map_obj)

    handler_obj.handleObstacles()

    #plt.imshow(tmap.matrix)
    #plt.show()

    #tmap.addObstacle(tmap.obstacles[0])
    #plt.imshow(tmap.matrix)
    #plt.show()

    #tmap.removeObstacle(OBSTACLES[0])
    #plt.imshow(tmap.matrix)
    #plt.show()
