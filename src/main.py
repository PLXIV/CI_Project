from city import City
import threading
from time import time
from datetime import timedelta

from GA.optimize import run_genetics
import sys
from time import sleep
import numpy as np
import pickle as pkl
from math import ceil

GRAPHICS = False

if __name__ == "__main__":
    from view.drawer import Drawer

def run_city(city, best_gene, max_sim_steps, light_duration, options):
    lights_steps = ceil(max_sim_steps / light_duration)
    lights_gene = best_gene.gene
    lights_gene = np.reshape(lights_gene, [len(city.grid.roads_with_lights), lights_steps]).T
    i = 0

    while not options[0] and i < max_sim_steps:
        lights = lights_gene[ceil(i / light_duration), :]
        city.step(lights)
        i += 1
        sleep(0.1)

if __name__ == "__main__":

    init = time()

    sys.setrecursionlimit(10000)
    # City parameters
    rows = 30
    cols = 30
    n_intersections = 5
    seed = 13011
    light_duration = 5

    # Sim parameters
    max_sim_steps = 200
    max_generations = 500
    num_sim = 20

    #GA hyperparameters
    ga_hyperparameters = {
    'pop_size':26,
    'elitism_n':100,
    'truncation_percentage':0.33,
    'cross_over_points':10,
    'crossover_probability':0.9, 
    'mutation_probability':0.005,
    'spread_mutation': 0}
    
    # Run
    best_performance, best_gene = run_genetics(rows, cols, n_intersections, seed, ga_hyperparameters, light_duration, max_generations, max_sim_steps, num_sim)
    print('Finished training, best performance:', best_performance)
    np.save('../data/best_' + str(max_generations)+'_generations.npy',best_gene)

    # Show best
    if GRAPHICS:
        options = [False] # QUIT
        city = City(rows, cols, n_intersections, seed)
        drawer = Drawer(fps_target=30, city=city, width=800, height=800, options=options)
        sim = threading.Thread(target=run_city, args=[city, best_gene, max_sim_steps, light_duration, options])
        sim.start()
        drawer.run()
        sim.join()

    total_time = time() - init

    print('\n Total time of the simulation:', timedelta(seconds=total_time))




