from city import City
from view.drawer import Drawer
import threading
import queue

#def name_conversor(row, col):
#    return str(row) + ('-') + str(col)

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

    path = queue.Queue()
    #print('start', start_p.col, start_p.row)
    previous = current_node
    while(current_node != start_p):
        previous = current_node
        current_node = dict_path[current_node]
        path.put(current_node)            
        # print(current_node.col, current_node.row)
    #print(previous.col, previous.row)
    #print('end',final_p.col, final_p.row)
    return path, previous
        
        
    
    


if __name__ == "__main__":

    # City
    city = City(rows=20, cols=20, n_intersections=5)
    city.grid.generate(seed=120)
    #print(city.grid)
    #print(city.grid.intersections)
    start_p = city.grid.get(1,12)
    final_p = city.grid.get(1,5)
    
    path, current_node =search_bfs(city.grid, start_p, final_p)
    
    # Window
#    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)
#    drawer.run()
#    t = threading.Thread(target=drawer.run, args=[])
#    t.start()

#    t.join()
     