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
    print('Calculating BFS: 0 of {:d}'.format(max_roads), end='')

    for i, current_road in enumerate(all_roads):
        if i % 2 == 0 or i == 0 or i == max_roads:
            print('\rCalculating BFS: {:d} of {:d}'.format(i, max_roads), end='    ')

        destinations = {}
        for posible_destination in all_roads:
            if current_road != posible_destination:
                _, previous = search_bfs(grid, current_road, posible_destination)
                destinations[posible_destination] = previous
            else:
                destinations[posible_destination] = None
        
        current_road.destinations = destinations