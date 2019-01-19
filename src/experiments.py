import seaborn as sns
import matplotlib.pyplot as plt
from random import choice
from city import City

sns.set()

from time import time, sleep
from datetime import timedelta

def run_all_green(city,steps_simulation,n_simulations):

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


def run_all_random(city,steps_simulation,n_simulations):
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
    sns.distplot(all_fitness)
    plt.xlabel('Fitness value')
    plt.ylabel('Proportion')
    plt.title('Fitness Values of the Simulation With Random Traffic Lights')
    plt.savefig('../data/fitness_random_lights.png')
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
    num_sim = 5

    city = City(rows, cols, n_intersections, seed)

    # Run
    run_all_random(city, max_sim_steps,num_sim)
