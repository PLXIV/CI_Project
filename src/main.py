from map import Map
from drawer import display
import threading

if __name__ == "__main__":

    map = Map(rows=32, cols=32, n_intersections=20)
    map.grid.generate(seed=120)
    print(map.grid)
    print(map.grid.intersections)

    t = threading.Thread(target=display, args=[map])
    t.start()

    t.join()