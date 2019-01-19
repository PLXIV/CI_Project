# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 23:20:09 2019

@author: PauL
"""
from cell import CellType
import queue

def search_bfs(grid, start_p, final_p):

    dict_path = {}
    dict_path[start_p] =  None
    found = False
    
    childrens = queue.Queue()
    childrens.put(start_p)
    visited_nodes = []

    while (found == False and not childrens.empty()):
        current_node  = childrens.get()
        if current_node is final_p:
            found = True
        
        if current_node.children:
            for i in current_node.children:
                if not i in visited_nodes:
                    childrens.put(i)
                    dict_path[i] = current_node
            visited_nodes.append(current_node)

    if not found:
        path = None
        previous = None
    else:
        path = []
        previous = current_node
        while(current_node != start_p):
            previous = current_node
            current_node = dict_path[current_node]
            path.append(current_node)   
         
    return path, previous
        
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
        if i % 2 == 0 or i == 0 or i == (max_roads -1):
            print('\rCalculating BFS: {:d} {:d} {:.1f}, {:.1f} skipped'.format(i, max_roads, 100.0 * i * max_roads / total, 100.0 * skipped / total), end='    ')

        for posible_destination in all_roads:
            if current_road != posible_destination:
                if not posible_destination in all_destinations[current_road].keys():

                    path, previous = search_bfs(grid, current_road, posible_destination)
                    all_destinations[current_road][posible_destination] = previous
                    if path:
                        for node in range(len(path)-1,0,-1):
                            for next_node in range(len(path)-2,-1,-1):
                                if not path[next_node] in all_destinations[path[node]].keys():
                                    all_destinations[path[node]][path[next_node]] = path[next_node -1]
                else:
                    skipped += 1
            else:
                all_destinations[current_road][posible_destination] = None
    
    for current_road in all_roads:     
        current_road.destinations = all_destinations[current_road]
        if len(all_roads) != len(current_road.destinations.keys()):
            print(len(current_road.destinations.keys()))
    print(len(all_roads))