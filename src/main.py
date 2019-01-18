from city import City
from view.drawer import Drawer
from bfs import generate_bfs_matrix
import threading
                
if __name__ == "__main__":

    # City
    city = City(rows=20, cols=20, n_intersections=4)
    city.grid.generate(seed=12)
  
    start_p = city.grid.get(1,4)
    final_p = city.grid.get(1,11)
    
    destinations = generate_bfs_matrix(city.grid)
   
    
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)
    drawer.run()
    #t = threading.Thread(target=drawer.run, args=[])
    #t.start()

    #t.join()
