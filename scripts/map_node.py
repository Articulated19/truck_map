#!/usr/bin/env python
# license removed for brevity
import rospy
#from std_msgs.msg import Int64
from truck_map.msg import Line
from truck_map.srv import GetMap
from graph import *


MAP_PATH = "/map.png"

PUBLISH_TOPIC = "map_updated"
MAP_SERVICE = "get_map"


class MapNode:

    def __init__(self):
        #self.map = Map(MAP_PATH)

        #self.pub = rospy.Publisher(PUBLISH_TOPIC, Int64, queue_size=10)
        serv1 = rospy.Service(MAP_SERVICE, GetMap, self.handleGetMap)

        rospy.loginfo("Waiting for request on services '%s'", MAP_SERVICE)


    def handleGetMap(self, req):
        rospy.loginfo("Returning graph after request on service '%s'", MAP_SERVICE)
        l1 = Line()
        l2 = Line()
        l1.line = [4, 6]
        l2.line = [5, 3] 
        arr = [[l1, l2]]
        return arr


if __name__ == '__main__':
    rospy.init_node('map', anonymous=True)
    MapNode()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
