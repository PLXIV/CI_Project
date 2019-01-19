from city import City
import threading
from time import time
from datetime import timedelta
from GA.optimize import run_genetics
import sys
from time import sleep

if __name__ == "__main__":
    from view.drawer import Drawer

def run_city(city, options):
    while not options[0]:
        city.step()
        sleep(0.1)

if __name__ == "__main__":

    init = time()

    sys.setrecursionlimit(10000)
    # City parameters
    rows = 30
    cols = 30
    n_intersections = 15
    seed = 13011
    options = [False] # QUIT

    # Graphics
    city = City(rows, cols, n_intersections, seed)
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, options=options)

    # Run
    #ga  = threading.Thread(target=run_genetics, args=[rows, cols, n_intersections, seed])
    sim = threading.Thread(target=run_city, args=[city, options])
    sim.start()
    #ga.start()
    drawer.run()
    sim.join()
    #ga.join()

    total_time = time() - init

    print('\n Total time of the simulation:', timedelta(seconds=total_time))




