import numpy as np
from GA.Population import Population
from multiprocessing import Pool
from city import City
from time import time
from datetime import timedelta
from math import ceil

PROCESSES = 6
ENABLE_MULTIPROCESSING = True

def generate_args(cities, number_of_lights, population, num_sim, max_sim_steps, lights_steps, light_duration):
    args = []
    for i, g in enumerate(population.genes):
        cities[i].clean()
        args.append([cities[i], g.gene, number_of_lights, num_sim, max_sim_steps, lights_steps, light_duration])
    return args

def run_genetics(rows, cols, n_intersections, seed, light_duration=1, max_generations=40, max_sim_steps=200, num_sim=5):
    dummy = City(rows, cols, n_intersections, seed)
    number_of_lights = len(dummy.grid.roads_with_lights)
    lights_steps = ceil(max_sim_steps / light_duration) + 1

    population = Population(generation_id=0, pop_size=26, dna_size=lights_steps * number_of_lights, elitism_n=100,
                            truncation_percentage=0.33, cross_over_points=10,
                            crossover_probability=0.9, mutation_probability=0.005,
                            spread_mutation= 0, objects_codified = 2, multiprocessing=False)

    print('Maximum population size: ', population.max_pop_size())
    cities = [City(rows, cols, n_intersections, seed) for _ in range(population.max_pop_size())]

    best_gene = []
    best_performance = 0
    for generation in range(max_generations):
        init = time()
        print('Step:', generation, end=' ')
        args = generate_args(cities, number_of_lights, population, num_sim, max_sim_steps, lights_steps, light_duration)
        if ENABLE_MULTIPROCESSING:
            pool = Pool(PROCESSES)
            scores = pool.starmap(run_gene, args)
            pool.close()
            for i, s in enumerate(scores):
                population.genes[i].score = s
        else:
            for gene in population.genes:
                gene.score = run_gene(gene)

        best_performance, best_gene, pop_size = population.update_genes()
        print('| New pop size:', pop_size, '| Best fitness:', best_performance, '| Took', timedelta(seconds=(time() - init)))
    return best_performance, best_gene


# city, gene, number_of_lights, n_simulations, steps_simulation
def run_gene(city, gene, number_of_lights, num_sim, max_sim_steps, lights_steps, light_duration):
    average_fitness = []
    for single_simulation in range(num_sim):
        lights_gene = gene
        lights_gene = np.reshape(lights_gene, [number_of_lights, lights_steps]).T
        for i in range(max_sim_steps):
            lights = lights_gene[ceil(i / light_duration), :]
            city.step(lights)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()
    return np.mean(average_fitness)