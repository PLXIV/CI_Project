from city import City
from view.drawer import Drawer
import threading

if __name__ == "__main__":

    # City
    city = City(rows=12, cols=12, n_intersections=1)
    city.grid.generate()
    #print(city.grid)
    #print(city.grid.intersections)

    # Window
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)
    drawer.run()
    #t = threading.Thread(target=drawer.run, args=[])
    #t.start()

    #t.join()