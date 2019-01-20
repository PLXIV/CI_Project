# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 14:49:45 2019

@author: PauL
"""

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
FOLDER = '../data/'

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
    max_sim_steps = 250
    max_generations = 250
    num_sim = 15
    light_duration_list = [10,20]

    #GA hyperparameters 
    pop_sizes = [60]
    elitism_n = [20,40,60]
    truncation_percentages = [0.1, 0.2, 0.3]
    cr_points = [10,20,30,40]
    mutation_probabilities= [0.001, 0.01, 0.1]
    spreading = [0]


    # Run
    for sz in pop_sizes:
        for light_duration in light_duration_list:
            for eli in elitism_n:
                for tr_p in truncation_percentages:
                    for c_p in cr_points:
                        for m_p in mutation_probabilities:
                            for s in spreading:
                                ga_hyperparameters = {
                                'pop_size':sz,
                                'elitism_n':eli,
                                'truncation_percentage':tr_p,
                                'cross_over_points':c_p,
                                'crossover_probability':0.9, 
                                'mutation_probability':m_p,
                                'spread_mutation': s}
                                
                                best_performance, best_gene, best_performance_historical = run_genetics(rows, cols, n_intersections, seed, ga_hyperparameters, light_duration, max_generations, max_sim_steps, num_sim)
                                print('Finished training, best performance:', best_performance)
                            
                                np.save(FOLDER+ str(sz) + '_popsize_'+ str(light_duration) + '_light_' + str(eli) + '_elitism_' + str(tr_p) + '_tr_percentage_' + str(c_p)+\
                                        '_cr_points_' + str(m_p) + '_mut_prob_' + str(s) + '_spread_' +'.npy',[best_performance_historical, best_gene])


    # Show best
    if GRAPHICS:
        options = [False] # QUIT`x
        city = City(rows, cols, n_intersections, seed)
        drawer = Drawer(fps_target=30, city=city, width=800, height=800, options=options)
        sim = threading.Thread(target=run_city, args=[city, best_gene, max_sim_steps, light_duration, options])
        sim.start()
        drawer.run()
        sim.join()

    total_time = time() - init

    print('\n Total time of the simulation:', timedelta(seconds=total_time))




