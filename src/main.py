from city import City
import threading
from time import time
from datetime import timedelta

from GA.optimize import run_genetics
import sys
from time import sleep
import numpy as np
import pickle as pkl

GRAPHICS = False

if __name__ == "__main__":
    from view.drawer import Drawer

def run_city(city, best_gene, max_sim_steps, options):
    lights_gene = best_gene.gene
    lights_gene = np.reshape(lights_gene, [len(city.grid.roads_with_lights), max_sim_steps]).T
    i = 0

    while not options[0] and i < max_sim_steps:
        lights = lights_gene[i, :]
        city.step(lights)
        i += 1
        sleep(0.1)

if __name__ == "__main__":

    init = time()

    sys.setrecursionlimit(10000)
    # City parameters
    rows = 30
    cols = 30
    n_intersections = 15
    seed = 13011

    # Sim parameters
    max_sim_steps = 200
    max_generations = 500
    num_sim = 5

    # Run
    best_performance, best_gene = run_genetics(rows, cols, n_intersections, seed, max_generations, max_sim_steps, num_sim)
    print('Finished training, best performance:', best_performance)
    np.save('../data/best_' + str(max_generations)+'_generations.npy',best_gene)

    # Show best
    if GRAPHICS:
        options = [False] # QUIT
        city = City(rows, cols, n_intersections, seed)
        drawer = Drawer(fps_target=30, city=city, width=800, height=800, options=options)
        sim = threading.Thread(target=run_city, args=[city, best_gene, max_sim_steps, options])
        sim.start()
        drawer.run()
        sim.join()

    total_time = time() - init

    print('\n Total time of the simulation:', timedelta(seconds=total_time))




