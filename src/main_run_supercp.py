from city.city import City
import threading
from time import time
from datetime import timedelta

from ga.optimize import run_genetics
import sys
from time import sleep
import numpy as np
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
    
    max_sim_steps_list =  [50,100,150,200]
    max_generations_list = [50,100,200,300,400,700]
    num_sim = 20

    #ga hyperparameters
    pop_sizes = [20,40,60,80]
    elitism_n = [5,10,20,40]
    truncation_percentages = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    cr_points = [10,20,30,40]
    mutation_probabilities= [0.001,0.005, 0.01, 0.05, 0.1]
    spreading = [0,1,2]

    sz = pop_sizes[0]
    eli = elitism_n[0]
    tr_p = truncation_percentages[0]
    c_p = cr_points[0]
    m_p = mutation_probabilities[0]
    s = spreading[0]


    
    # Run
    for max_sim_steps in max_sim_steps_list:
        for max_generations in max_generations_list:
            for sz in pop_sizes:
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
                                    np.save( FOLDER+'best_'+ str(max_generations)+'_generations.npy',best_gene)
                                
                                    np.save(FOLDER+'best_'+ str(max_sim_steps)+'_sim_steps_' + str(max_generations)+'_generations_' + str(sz) + '_popsize_'+ str(eli) + '_elitism_' + str(tr_p) + '_tr_percentage_' + str(c_p)+\
                                            '_cr_points_' + str(m_p) + '_mut_prob_' + str(s) + '_spread_' +'.npy',best_performance_historical)


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




