from map import Map
from drawer import display
import threading

if __name__ == "__main__":

    map = Map(rows=20, cols=20, n_intersections=10)
    map.grid.generate()
    print(map.grid)
    print(map.grid.intersections)

    t = threading.Thread(target=display, args=[map])
    t.start()

    t.join()