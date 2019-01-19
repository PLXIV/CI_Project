# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 23:20:09 2019

@author: PauL
"""
from cell import CellType
import queue

def backtrack_bfs(curr_node, dict_path, start_p):
    path = []
    previous = curr_node
    while curr_node != start_p:
        previous = curr_node
        curr_node = dict_path[curr_node]
        path.insert(0, curr_node)
    return path, previous

def search_bfs(start_p, final_p):

    dict_path = {}
    dict_path[start_p] = None
    next_nodes = queue.Queue()
    next_nodes.put(start_p)
    visited_nodes = []

    while not next_nodes.empty():
        current_node = next_nodes.get()
        if current_node is final_p:
            return backtrack_bfs(current_node, dict_path, start_p)
        
        if current_node.children:
            for child in current_node.children:
                if not child in visited_nodes:
                    next_nodes.put(child)
                    dict_path[child] = current_node
            visited_nodes.append(current_node)

    return None, None
        
def generate_bfs_dictionaries(grid):
    all_roads = []
    for i in range(grid.rows):
        for j in range(grid.cols):
            if (grid.get(i,j).type == CellType.Road):
                all_roads.append(grid.get(i,j))

    max_roads = len(all_roads)
    total = max_roads * max_roads

    all_destinations = {}
    for current_road in all_roads:
        all_destinations[current_road] = {}

    skipped = 0
    for i, current_road in enumerate(all_roads):

        for posible_destination in all_roads:
            if current_road != posible_destination:
                if not posible_destination in all_destinations[current_road].keys():

                    path, previous = search_bfs(current_road, posible_destination)
                    all_destinations[current_road][posible_destination] = previous
                    print(current_road)
                    print(posible_destination)
                    print(previous)
                    print(path)
                    if path:
                        for node in range(len(path) - 1):
                            for next_node in range(1, len(path)):
                                if not path[next_node] in all_destinations[path[node]].keys():
                                    all_destinations[path[node]][path[next_node]] = path[next_node -1]
                else:
                    skipped += 1
            else:
                all_destinations[current_road][posible_destination] = None

        if i % 2 == 0 or i == 0 or i == (max_roads - 1):
            print('\rCalculating BFS: {:.1f}%, {:.1f}% skipped'.format(100.0 * (i + 1) * max_roads / total, 100.0 * skipped / total), end='    ')
    
    for current_road in all_roads:     
        current_road.destinations = all_destinations[current_road]
        if len(all_roads) != len(current_road.destinations.keys()):
            print(len(current_road.destinations.keys()))
    print(len(all_roads))