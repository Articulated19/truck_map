#!/usr/bin/env python
# license removed for brevity
from map_func import *

import rospy
from std_msgs.msg import Int8
import numpy as np


SUB_TOPIC = "handle_obstacle"
PUBLISH_TOPIC = "map_updated"

SCALE = 10  # Map img is in scale 1:10


class ObstacleHandler:

    def __init__(self, map_obj):
        self.map = map_obj

        # Ros topics
        self.sub = rospy.Subscriber(SUB_TOPIC, Int8, self.handleObstacle)
        self.pub = rospy.Publisher(PUBLISH_TOPIC, Int8, queue_size=10)
        rospy.loginfo("Subscribing to topic '%s'", SUB_TOPIC)
        rospy.loginfo("Publishing on topic '%s'", PUBLISH_TOPIC)


    # Activates/deactivates Obstacle with given index on the 'map' of this handler
    def handleObstacle(self, data):
        index = int(str(data.data))

        # Checking if there is an obstacle in 'obstacles' that corresponds with given index,
        # only proceeding if there is
        try:
            obstacle = self.map.obstacles[index]
        except IndexError:
            print "There is no obstacle with index '%s'" % (index)
            return

        # If the obstacle is active: Deactivating it
        if obstacle.active:
            # Removing obstacle from the map matrix
            self.map.removeObstacle(index)
            print "Obstacle '%s' was deactivated" % (index)
            self.pub.publish(index)

        # If the obstacle is inactive: Activating it
        else:
            # Adding obstacle to the map matrix
            self.map.addObstacle(index)
            print "Obstacle '%s' was activated" % (index)
            self.pub.publish(index)


if __name__ == "__main__":
    rospy.init_node("obstacles", anonymous=True)
    map_obj = Map()
    handler_obj = ObstacleHandler(map_obj)

    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


# rosrun truck_map obstacle_node.py
# rostopic echo map_updated
