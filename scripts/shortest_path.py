#!/usr/bin/env python
from graph_func import *

from heapq import heappush, heappop


# Takes a Graph and two Point objects with (x, y)-coordinates for start and end point
#
# If there is a path from the start Point to the end Point:
#     Returns the shortest path between them as an array of tuples of (x, y)-coordinates
# Otherwise:
#     Returns None
def shortestPath(graph, start, end):

    # Used to specify search range for finding closest point
    search_range = 20
    nodes = graph.nodes.values()

    # Finding start resp. end Node:

    start_node = graph.getNode(start.x, start.y)

    # If the coordinates for the start point does Not exactly match a Node in the graph
    if not start_node:

        # Selecting all Nodes which are in range from the start point
        nodes = getAllInRangeX(getAllInRangeY(nodes, start, search_range), start, search_range)
        # Returning None if No Node is in range
        if not nodes:
            return None
        # Finding the two Nodes which are closest to the start point, x-wise resp. y-wise
        closest_x = getClosestX(nodes, start)
        closest_y = getClosestY(nodes, start)
        # Selecting the Node which is closest to the start point
        dx = Node(start.x, start.y).getEdgeLength(closest_x)
        dy = Node(start.x, start.y).getEdgeLength(closest_y)
        start_node = closest_x if dx <= dy else closest_y

    end_node = graph.getNode(end.x, end.y)

    # If the coordinates for the end point does Not exactly match a Node in the graph
    if not end_node:

        # Selecting all Nodes which are in range from the end point
        nodes = getAllInRangeX(getAllInRangeY(nodes, end, search_range), end, search_range)
        # Returning None if No Node is in range
        if not nodes:
            return None
        # Finding the two Nodes which are closest to the end point, x-wise resp. y-wise
        closest_x = getClosestX(nodes, end)
        closest_y = getClosestY(nodes, end)
        # Selecting the Node which is closest to the end point
        dx = Node(end.x, end.y).getEdgeLength(closest_x)
        dy = Node(end.x, end.y).getEdgeLength(closest_y)
        end_node = closest_x if dx <= dy else closest_y

    result = findShortestPath(graph, start_node, end_node)

    try:
        path, l, a = result
        return path
    except ValueError:
        return result


def kShortestPaths(graph, start, end, k):
    start_node = graph.getNode(start.x, start.y)
    end_node = graph.getNode(end.x, end.y)
    path_heap = []
    paths = []
    paths_ = []

    graph.resetGraph()
    heappush(path_heap, (0, [(start_node.x, start_node.y)]))

    while path_heap and end_node.count < k:
        cost, path = heappop(path_heap)
        last_node = graph.getNode(path[-1][0], path[-1][1])
        last_node.count += 1

        if last_node == end_node:
            paths.append((path, cost))

        elif last_node.count <= k:
            for out_edge in last_node.out_edges:
                if (out_edge.x, out_edge.y) not in path:
                    new_path = []
                    for coord in path:
                        new_path.append(coord)
                    new_path.append((out_edge.x, out_edge.y))
                    new_cost = cost + last_node.getEdgeLength(out_edge)
                    heappush(path_heap, (new_cost, new_path))


    paths_ = map(lambda (path, cost): path, paths)
    return paths_


    
# Takes a Graph, and two Point objects with (x, y)-coordinates for start and end point
#
# The given start and end Points have to exactly match Nodes in the given Graph
#
# If given paramaters are invalid:
#     Returns None
# If there is at least one alternative path between the given start and end points:
#     Returns an array of alternative paths between given start and end points
# Otherwise:
#     Returns []
def altPaths(graph, start, end):
    start_node = graph.getNode(start.x, start.y)
    end_node = graph.getNode(end.x, end.y)
    paths = []

    # Returning None if the given start and end Points do Not exactly match Nodes in the given Graph
    if not start_node or not end_node:
        return None

    p, length, alt = findShortestPath(graph, start_node, end_node)

    # Going through all first-level alternatives
    for node in alt:
        try:
            path_1, length_1, alt_1 = findShortestPath(graph, start_node, node)
        except ValueError:
            path_1 = []
        try:
            path_2, length_2, alt_2 = findShortestPath(graph, node, end_node)
        except ValueError:
            path_2 = []

        # Only moving forward if an alternative path could be created via this Node
        if path_1 and path_2:
            paths.append((path_1[:-1] + path_2, length_1 + length_2))

            # Going through all second-level alternatives
            for node_2 in alt_2:
                try:
                    path_21, length_21, alt_21 = findShortestPath(graph, node, node_2)
                except ValueError:
                    path_21 = []
                try:
                    path_22, length_22, alt_22 = findShortestPath(graph, node_2, end_node)
                except ValueError:
                    path_22 = []

                # Only moving forward if an alternative path could be created via this Node
                if path_21 and path_22:
                    path = (path_21[:-1] + path_22, length_21 + length_22)
                    paths.append((path_1[:-1] + path[0], length_1 + path[1]))

                    # Going through all third-level alternatives
                    for node_3 in alt_22:
                        try:
                            path_31, length_31, alt_31 = findShortestPath(graph, node_2, node_3)
                        except ValueError:
                            path_31 = []
                        try:
                            path_32, length_32, alt_32 = findShortestPath(graph, node_3, end_node)
                        except ValueError:
                            path_32 = []

                        # Only moving forward if an alternative path could be created via this Node
                        if path_31 and path_32:
                            path = (path_31[:-1] + path_32, length_31 + length_32)
                            paths.append((path_1[:-1] + path_21[:-1] + path[0], length_1 + length_21 + path[1]))

    # Making sure the paths are in order, sorted by length
    paths = sorted(paths, key=lambda tup: tup[1])
    paths = map(lambda path: path[0], paths)

    # Removing duplicates
    no_dub = []
    for path in paths:
        if path not in no_dub:
            no_dub.append(path)

    return no_dub


# Help function for 'shortestPath'
# Takes a Graph and two Nodes for start and end point
#
# If the start Node is the same as the end Node:
#     Returns []
# If there is a path from the start Node to the end Node:
#     Returns a tuple with the shortest path between them as an array of tuples of (x, y)-coordinates,
#     the length of the path, and an array of nodes used for creating alternate paths
# Otherwise:
#     Returns None
def findShortestPath(graph, start_node, end_node):
    if start_node == end_node:
        return []

    graph.resetGraph()
    path = []

    start_node.distance = 0
    current_node = start_node

    # Repeating until the end Node has been visited
    # (or until we know that there is no path from the start Node to the end Node)
    while not end_node.visited:

        # Checking if there are any more Nodes that can be visited,
        # returning None if there aren't any (since that means that the end Node can't be reached)
        if current_node.distance == INF:
            return None

        # Going through all unvisited out-edges from 'current_node'
        # Calculating the distance to each such Node from the start point, via 'current_node',
        # and updating their 'distance' value if this distance is smaller than the current value
        for out_edge in current_node.out_edges:
            if not out_edge.visited:
                edge_length = current_node.getEdgeLength(out_edge)
                new_distance = current_node.distance + edge_length

                if new_distance < out_edge.distance:
                    out_edge.distance = new_distance

        # Removing 'current_node' from the unvisited set
        # (it is now considered visited, and will never be checked again)
        current_node.visited = True

        # Selecting the unvisited Node that has the smallest 'distance' as the new 'current_node'
        smallest_node = None
        smallest_distance = INF
        for node in graph.nodes.values():
            if not node.visited and node.distance < smallest_distance:
                smallest_node = node
                smallest_distance = node.distance

        current_node = smallest_node

    # Backtracing to construct the path
    current_node = end_node
    path.insert(0, (current_node.x, current_node.y))

    # For creating alternative paths
    alternatives = []

    # Repeating until start Node is reached
    while current_node != start_node:

        # Going through all in-edges, to find the Node which preceeds 'current_node'
        for node in current_node.in_edges:
            edge_length = node.getEdgeLength(current_node)
            if (node.distance + edge_length) == current_node.distance:

                # If this is a point where we can go more than one way, adding the alternative Node to 'alternatives'
                if len(node.out_edges) > 1:
                    for out_edge in node.out_edges:
                        if out_edge != current_node:
                            alternatives.append(out_edge)

                current_node = node
                path.insert(0, (current_node.x, current_node.y))
                break

    return path, end_node.distance, alternatives


# Takes a Graph and a VehicleState object
#
# If there is a Node with an out-edge in the right Direction (with respect to theta):
#     Returns the closest Node which has an out-edge in the right Direction
# Otherwise:
#     Returns None
def getClosestToVehicle(graph, vehicle_state):

    # Used to specify search range for finding closest point
    search_range = 100

    # Normalizing theta
    theta = degrees(vehicle_state.theta1) % 360
    pos = Point(vehicle_state.x, vehicle_state.y)
    nodes = graph.nodes.values()

    # Vehicle angle: bottom-to-top
    if theta > 225 and theta <= 315:
        # Selecting all Nodes which are in range from the vehicle
        nodes = getAllInRangeX(getAllInRangeY(nodes, pos, search_range, 0), pos, search_range)
        # Selecting all Nodes which have an out-edge upwards from vehicle position
        nodes = getAllInRightDir(nodes, pos, Direction.up)

    # Vehicle angle: right-to-left
    elif theta > 135 and theta <= 225:
        # Selecting all Nodes which are in range from the vehicle
        nodes = getAllInRangeX(getAllInRangeY(nodes, pos, search_range), pos, search_range, 0)
        # Selecting all Nodes which have an out-edge to the left from vehicle position
        nodes = getAllInRightDir(nodes, pos, Direction.left)

    # Vehicle angle: top-to-bottom
    elif theta > 45 and theta <= 135:
        # Selecting all Nodes which are in range from the vehicle
        nodes = getAllInRangeX(getAllInRangeY(nodes, pos, 0, search_range), pos, search_range)
        # Selecting all Nodes which have an out-edge downwards from vehicle position
        nodes = getAllInRightDir(nodes, pos, Direction.down)

    # Vehicle angle: left-to-right
    elif theta > 315 or theta <=45:
        # Selecting all Nodes which are in range from the vehicle
        nodes = getAllInRangeX(getAllInRangeY(nodes, pos, search_range), pos, 0, search_range)
        # Selecting all Nodes which have an out-edge to the right from vehicle position
        nodes = getAllInRightDir(nodes, pos, Direction.right)

    # Returning None if No Node is in range
    if not nodes:
        return None
        
    # Finding the two Nodes which are closest to the vehicle, x-wise resp. y-wise
    closest_x = getClosestX(nodes, pos)
    closest_y = getClosestY(nodes, pos)
    # Selecting the Node which is closest to the vehicle:
    dx = Node(pos.x, pos.y).getEdgeLength(closest_x)
    dy = Node(pos.x, pos.y).getEdgeLength(closest_y)
    start_node = closest_x if dx <= dy else closest_y

    return start_node


# Takes an array of Node objects, Point object and range limits to the left resp. to the right
#
# Returns an array with all Nodes that are in range (set by given limits) x-wise from given Point
def getAllInRangeX(nodes, point, range_left, range_right=None):
    range_right = range_right if range_right != None else range_left
    node_list = []
    for node in nodes:

        # Selecting all Nodes that are in range x-wise
        if node.x >= point.x-range_left and node.x <= point.x+range_right:
            node_list.append(node)

    return node_list


# Takes an array of Node objects, Point object and range limits above resp. below
#
# Returns an array with all Nodes that are in range (set by given 'limit') y-wise from given Point
def getAllInRangeY(nodes, point, range_above, range_below=None):
    range_below = range_below if range_below != None else range_above
    node_list = []
    for node in nodes:

        # Selecting all Nodes that are in range y-wise
        if node.y >= point.y-range_above and node.y <= point.y+range_below:
            node_list.append(node)

    return node_list


# Takes an array of Node objects and a Point object
#
# Returns the Node that is (x-wise) closest to given Point
def getClosestX(nodes, point):
    closest_node = None
    closest_dist = float('inf')

    for node in nodes:
        dist = abs(point.x - node.x)

        # If no Node can be closer
        if dist == 0:
            return node
        elif dist < closest_dist:
            closest_dist = dist
            closest_node = node

    return closest_node


# Takes an array of Node objects and a Point object
#
# Returns the Node that is (y-wise) closest to given Point
def getClosestY(nodes, point):
    closest_node = None
    closest_dist = float('inf')
    
    for node in nodes:
        dist = abs(point.y - node.y)

        # If no Node can be closer
        if dist == 0:
            return node
        elif dist < closest_dist:
            closest_dist = dist
            closest_node = node

    return closest_node


Direction = Enum('Direction', 'up down left right')


# Takes an array of Node objects, a Point object and a Direction
#
# Returns an array with all Nodes that have an out-edge in the given Direction
def getAllInRightDir(nodes, point, direction):
    node_list = []
    for node in nodes:

        # Selecting all Nodes that have an out-edge in the right direction
        if hasOutEdgeInRightDir(node, direction):
            node_list.append(node)

    return node_list


# Takes a Node and a Direction
#
# If given Node has an out-edge in given Direction:
#     Returns True
# Otherwise:
#     Returns False
def hasOutEdgeInRightDir(node, direction):

    # Used to specify minimum difference between given Node and an out-edge-node,
    # (x-wise resp. y-wise) for the edge to be considered as going in a specific Direction
    min_offset = 5

    # Going through all out-edges,
    # returning True as soon as we find one that goes in the given Direction
    for out_edge in node.out_edges:

        if direction == Direction.up:
            # If given Node has an out-edge upwards
            if (node.y - out_edge.y) > min_offset:
                return True

        elif direction == Direction.down:
            # If given Node has an out-edge downwards
            if (node.y - out_edge.y) < -min_offset:
                return True

        elif direction == Direction.left:
            # If given Node has an out-edge to the left
            if (node.x - out_edge.x) > min_offset: 
                return True

        elif direction == Direction.right:
            # If given Node has an out-edge to the right
            if (node.x - out_edge.x) < -min_offset:
                return True 

    # No out-edge in the given Direction
    return False