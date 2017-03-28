#!/usr/bin/env python
from map_func import *

from os.path import dirname, abspath
from PIL import Image


IMG_PATH = '/map.png'


class ObstacleHandler:

    def __init__(self):
        dirpath = dirname(abspath(__file__))

        self.map_img = Image.open(dirpath + IMG_PATH)
        self.map = Map()

        # For plotting
        self.ax = None


    # Handler for 'key_press_event'
    def onKeyPress(self, event):
        if event.key.isdigit():
            if event.key == '0':
                index = 9
            else:
                index = int(event.key)-1

            # Checking if there is an obstacle in 'obstacles' that corresponds with given number,
            # only proceeding if there is
            try:
                obstacle = self.map.obstacles[index]
            except IndexError:
                print "There is no obstacle with identifier '%s'" % (index+1)
                return

            # If the obstacle is active: Deactivating it
            if obstacle.active:
                # Removing obstacle from the map matrix
                self.map.removeObstacle(index)
                print "Obstacle '%s' was deactivated" % (index+1)

                # Updating obstacle plot
                obstacle.plot.remove()
                obstacle.text.remove()
                obstacle.plot = self.ax.add_patch(obstacle.deactivated_patch)
                obstacle.text = self.ax.text(obstacle.text_x, obstacle.text_y, str(index+1),
                                             verticalalignment='top', color='blue', fontweight='bold')
                plt.draw()

            # If the obstacle is inactive: Activating it
            else:
                # Adding obstacle to the map matrix
                self.map.addObstacle(index)
                print "Obstacle '%s' was activated" % (index+1)

                # Updating obstacle plot
                obstacle.plot.remove()
                obstacle.text.remove()
                obstacle.plot = self.ax.add_patch(obstacle.activated_patch)
                obstacle.text = self.ax.text(obstacle.text_x, obstacle.text_y, str(index+1),
                                             verticalalignment='top', color='red', fontweight='bold')
                plt.draw()


    # Lets user activate/deactivate obstacles on the 'map' of this handler
    #
    # Returns an array of Booleans, with an element for each Obstacle in 'obstacles'
    # with True if Obstacle at corresponding index should be activated, and False if it should be inactivated
    def handleObstacles(self):
        xlim = self.map_img.size[0]
        ylim = self.map_img.size[1]

        fig = plt.figure()
        self.ax = plt.axes()

        # Graph settings
        plt.axis('scaled')
        plt.xlim( (0, xlim) )
        plt.ylim( (ylim, 0) )
        plt.xlabel('-axis')
        plt.ylabel('y-axis')
        plt.title('handleObstacles()')

        # Displaying map image
        img_plot = plt.imshow(self.map_img)
        # Displaying all obstacles
        for i, obstacle in enumerate(self.map.obstacles):
            if obstacle.active:
                if obstacle.plot:
                    obstacle.plot.remove()
                obstacle.plot = self.ax.add_patch(obstacle.activated_patch)
                obstacle.text = self.ax.text(obstacle.text_x, obstacle.text_y, str(i+1),
                                             verticalalignment='top', color='red', fontweight='bold')
            else:
                if obstacle.plot:
                    obstacle.plot.remove()
                obstacle.plot = self.ax.add_patch(obstacle.deactivated_patch)
                obstacle.text = self.ax.text(obstacle.text_x, obstacle.text_y, str(i+1),
                                             verticalalignment='top', color='blue', fontweight='bold')

        print ("=====\nRed obstacles are activated, Blue obstacles are deactivated\n" +
               "Press the corresponding number key, to activate/deactivate an obstacle\n=====")

        fig.canvas.mpl_connect('key_press_event', self.onKeyPress)
        plt.show()

        active_or_not = map(lambda o: o.active, self.map.obstacles)
        return active_or_not


# Main, used for testing
if __name__ == '__main__':
    handler_obj = ObstacleHandler()
    result = handler_obj.handleObstacles()

    print result
