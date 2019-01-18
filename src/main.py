from city import City
from view.drawer import Drawer
import threading

if __name__ == "__main__":

    # City
    city = City(rows=30, cols=30, n_intersections=12)
    city.grid.generate(seed=120)
    print(city.grid)
    print(city.grid.intersections)

    # Window
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)
    drawer.run()
    #t = threading.Thread(target=drawer.run, args=[])
    #t.start()

    #t.join()