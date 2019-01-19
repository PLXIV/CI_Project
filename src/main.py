from city import City
from view.drawer import Drawer
from GA.Population import Population
import threading
import numpy as np
from time import sleep, time
from random import choice
from multiprocessing import Pool
from datetime import timedelta
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()
import sys

sys.setrecursionlimit(5500)
PROCESSES = 4

ENABLE_MULTIPROCESSING = True


def generate_args(city, population, number_of_lights, n_simulations, steps_simulation):
    args = []
    for g in population.genes:
        args.append([city.clone(), g.gene, number_of_lights, n_simulations, steps_simulation])
    return args


def run_genetics(city):
    number_of_lights = len(city.grid.roads_with_lights)

    steps_generations = 40
    steps_simulation = 200
    n_simulations = 5
    population = Population(generation_id=0, pop_size=20, dna_size=steps_simulation * number_of_lights, elitism_n=100,
                            truncation_percentage=0.33, cross_over_points=50,
                            crossover_probability=0.9, mutation_probability=0.005, multiprocessing=False)
    init = time()
    for generation in range(steps_generations):
        init_step = time()
        if population.convergence_criteria():
            break
        print('Genreation', generation)

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
        print('\n Ttime on this step',
              timedelta(seconds=time() - init_step))

    print(population.best_historical_performance)
    print('Ended simulation')
    print('\n Total time of the simulation:',
          timedelta(seconds=time() - init))


# city, gene, number_of_lights, n_simulations, steps_simulation
def run_gene(city, gene, number_of_lights, n_simulations, steps_simulation):
    average_fitness = []
    for single_simulation in range(n_simulations):
        lights_gene = gene
        lights_gene = np.reshape(lights_gene, [number_of_lights, steps_simulation]).T
        for i in range(steps_simulation):
            lights = lights_gene[i, :]
            city.step(lights)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()
    return np.mean(average_fitness)


def run_all_green(city):
    steps_simulation = 200
    n_simulations = 50
    average_fitness = []
    number_of_lights = len(city.grid.roads_with_lights)
    all_fitness = []
    for single_simulation in range(n_simulations):
        for i in range(steps_simulation):
            lights = [True for i in range(number_of_lights)]
            city.step(lights)
            # sleep(0.1)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()
        all_fitness.append(fitness)
    sns.distplot(all_fitness)
    plt.xlabel('Fitness value')
    plt.ylabel('Proportion')
    plt.title('Fitness Values of the Simulation Without Traffic Lights')
    plt.savefig('../data/fitness_only_green.png')
    print('ended simulation')


def run_all_random(city):
    steps_simulation = 200
    n_simulations = 50
    average_fitness = []
    number_of_lights = len(city.grid.roads_with_lights)
    all_fitness = []
    for single_simulation in range(n_simulations):
        for i in range(steps_simulation):
            lights = [choice([True, False]) for i in range(number_of_lights)]
            city.step(lights)
            # sleep(0.1)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()
        all_fitness.append(fitness)
    sns.distplot(all_fitness)
    plt.xlabel('Fitness value')
    plt.ylabel('Proportion')
    plt.title('Fitness Values of the Simulation With Random Traffic Lights')
    plt.savefig('../data/fitness_random_lights.png')
    print('ended simulation')


if __name__ == "__main__":
    init = time()

    # City

    city = City(rows=30, cols=30, n_intersections=15)

    city.grid.generate(seed=13011)

    city_time = time() - init

    # Graphics
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)

    # Run
    # t = threading.Thread(target=run_genetics, args=[city])
    t = threading.Thread(target=run_all_random, args=[city])
    t = threading.Thread(target=run_all_green, args=[city])
    t.start()
    drawer.run()
    t.join()
    total_time = time() - init

    print('Time spent on generating the city:', timedelta(seconds=city_time), '\n Total time of the simulation:',
          timedelta(seconds=total_time))
