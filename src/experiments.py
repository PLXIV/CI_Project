import seaborn as sns
import matplotlib.pyplot as plt
from random import choice
from city import City
import numpy as np
sns.set()

from time import time, sleep
from datetime import timedelta

def run_all_green(city,steps_simulation,n_simulations):
    print('begin green')
    average_fitness = []
    number_of_lights = len(city.grid.roads_with_lights)
    all_fitness = []
    for single_simulation in range(n_simulations):
        print('Simulation:', single_simulation)
        for i in range(steps_simulation):
            lights = [True for i in range(number_of_lights)]
            city.step(lights)
            # sleep(0.1)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()
        all_fitness.append(fitness)
    sns.distplot(all_fitness,label='All green')
    plt.xlabel('Fitness value')
    plt.ylabel('Proportion')
    plt.title('Fitness Values of the Simulation')
    plt.legend()
    plt.savefig('../data/fitness_all.png')
    print('ended simulation')


def run_all_random(city,steps_simulation,n_simulations):
    print('begin random')
    average_fitness = []
    number_of_lights = len(city.grid.roads_with_lights)
    all_fitness = []
    for single_simulation in range(n_simulations):
        print('Simulation:', single_simulation)
        for i in range(steps_simulation):
            lights = [choice([True, False]) for i in range(number_of_lights)]
            city.step(lights)
            # sleep(0.1)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()
        all_fitness.append(fitness)
    sns.distplot(all_fitness,label='Random')
    plt.xlabel('Fitness value')
    plt.ylabel('Proportion')
    plt.title('Fitness Values of the Simulation With Random Traffic Lights')
    plt.savefig('../data/fitness_random_lights.png')
    print('ended simulation')


def run_all_genetic(city,steps_simulation,n_simulations):
    print('begin genetics')
    average_fitness = []
    all_fitness = []
    best_individual = np.load('../data/best_500_generations.npy')
    lights_gene = np.reshape(best_individual, [len(city.grid.roads_with_lights), max_sim_steps]).T

    for single_simulation in range(n_simulations):

        for i in range(steps_simulation):
            lights = lights_gene[i, :]
            city.step(lights)
            # sleep(0.1)
        fitness = city.cars_despawned
        print('Simulation:', single_simulation, 'fitness:',fitness)
        average_fitness.append(fitness)
        city.clean()
        all_fitness.append(fitness)
    sns.distplot(all_fitness,label='Genetic')
    plt.xlabel('Fitness value')
    plt.ylabel('Proportion')
    plt.title('Fitness Values of the Simulation Genetic Traffic Lights')
    plt.savefig('../data/fitness_genetic_lights.png')
    print('ended simulation')


if __name__ == "__main__":

    init = time()

    # City parameters
    rows = 30
    cols = 30
    n_intersections = 15
    seed = 13011

    # Sim parameters
    max_sim_steps = 200
    num_sim = 500

    city = City(rows, cols, n_intersections, seed)

    # Run
    run_all_genetic(city, max_sim_steps,num_sim)
    city.clean()
    run_all_random(city, max_sim_steps,num_sim)
    city.clean()
    run_all_green(city, max_sim_steps,num_sim)