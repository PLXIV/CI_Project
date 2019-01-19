from city import City
from view.drawer import Drawer
from GA.Population import Population
import threading
import numpy as np
from time import sleep, time
from random import choice
from multiprocessing import Pool
from datetime import timedelta

PROCESSES = 8
ENABLE_MULTIPROCESSING = True


def generate_args(city, population, number_of_lights, n_simulations, steps_simulation):
    args = []
    for g in population.genes:
        args.append([city.clone(), g.gene, number_of_lights, n_simulations, steps_simulation])
    return  args

def run_genetics(city):

    number_of_lights = len(city.grid.roads_with_lights)
    steps_generations = 40
    steps_simulation = 200
    n_simulations = 5
    population = Population(generation_id=0, pop_size=20, dna_size=steps_simulation*number_of_lights, elitism_n=100,
                   truncation_percentage=0.33, cross_over_points=50,
                   crossover_probability=0.9, mutation_probability=0.005, multiprocessing=False)
   
    for generation in range(steps_generations):
        print('step: ', generation)
        args = generate_args(city, population, number_of_lights, n_simulations, steps_simulation)
        if ENABLE_MULTIPROCESSING:
            pool = Pool(PROCESSES)
            scores = pool.starmap(run_gene, args)
            pool.close()
            for i, s in enumerate(scores):
                population.genes[i].score = s
        else:
            for gene in population.genes:  
                gene.score = run_gene(gene)
        best_performance, best_gene = population.update_genes()
        


#city, gene, number_of_lights, n_simulations, steps_simulation
def run_gene(city, gene, number_of_lights, n_simulations, steps_simulation):
    average_fitness = []
    for single_simulation in range(n_simulations):
        lights_gene = gene
        lights_gene = np.reshape(lights_gene, [number_of_lights, steps_simulation]).T
        for i in range(steps_simulation):
            lights = lights_gene[i,:]
            city.step(lights)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()
    return np.mean(average_fitness)

if __name__ == "__main__":

    init = time()
    
    # City
    city = City(rows=100, cols=100, n_intersections=15)
    city.grid.generate(seed=13011)

    city_time = time() - init

    # Graphics
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)

    # Run
    t = threading.Thread(target=run_genetics, args=[city])
    t.start()
    drawer.run()
    t.join()
    total_time = time() - init

    print('Time spent on generating the city:', timedelta(seconds=city_time), '\n Total time of the simulation:', timedelta(seconds=total_time))




