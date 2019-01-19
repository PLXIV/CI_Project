from collections import defaultdict
from queue import Queue


def set_shortest_paths(roads):
    in_borders = [road for road in roads if len(road.parents) == 0]
    out_borders = [road for road in roads if len(road.children) == 0]
    destinations = defaultdict(dict)
    dependencies = defaultdict(list)
    parent = defaultdict(lambda: None)
    visited = defaultdict(lambda: False)

    # Fill unreachable
    for origin in out_borders:
        for destination in roads:
            destinations[origin][destination] = None

    for origin in roads:
        for destination in in_borders:
            destinations[origin][destination] = None

    # Fill diagonal
    for road in roads:
        destinations[road][road] = road

    # Explore tree
    for border in in_borders:
        queue = Queue()
        queue.put(border)
        while not queue.empty():
            curr = queue.get()
            for child in curr.children:
                if not visited[child]:
                    parent[child] = curr
                    visited[child] = True
                    queue.put(child)
                    __save_path(parent, child, destinations)
                else:
                    dependencies[child].append(curr)
                    __save_path_dependency(parent, curr, child, destinations)

    __copycat(parent, dependencies, destinations)
    for road in roads:
        road.destinations = defaultdict(lambda: None)
        for k, v in destinations[road].items():
            road.destinations[k] = v


def __copycat(parent, dependencies, destinations):
    for key in dependencies.keys():
        for dependency in dependencies[key]:
            __resolve(parent, dependency, key, destinations)


def __resolve(parent, origin, child, destinations):
    curr = origin
    last = child

    while curr is not None:
        for destination in destinations[child]:
            if destination not in destinations[curr]:
                destinations[curr][destination] = last
        last = curr
        curr = parent[curr]


def __save_path(parent, child, destinations):
    last = child
    curr = child

    while parent[curr] is not None:
        curr = parent[curr]
        destinations[curr][child] = last
        last = curr


def __save_path_dependency(parent, other_parent, child, destinations):
    last = child
    curr = other_parent

    destinations[curr][child] = last
    while parent[curr] is not None:
        curr = parent[curr]
        destinations[curr][child] = last
        last = curr
