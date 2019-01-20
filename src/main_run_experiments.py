import seaborn as sns
import matplotlib.pyplot as plt
from random import choice
from city.city import City
from ga.optimize import generate_filename
from time import time
import numpy as np
import sys
import json
sns.set()

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

CONFIGURATION = 'configuration.json'
GENE_FILE = '../data/1548007123_best_500_10_100_8_30_15_13011_regular_500_20_26_100_0+330000_10_0+900000_0+005000_0.npy'
SIMULATIONS = 500

def run_simulations(city, gene, sim_steps, light_duration_steps, label, title, save_file):
    average_fitness = []
    all_fitness = []

    for sim in range(SIMULATIONS):
        print('\rSimulation: {:4d} of {:d}'.format(sim, SIMULATIONS), end='')
        city.run(gene, sim_steps, light_duration_steps, sim_time=0)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        all_fitness.append(fitness)
        city.clean()

    sns.distplot(all_fitness,label=label)
    plt.xlabel('Fitness value')
    plt.ylabel('Proportion')
    plt.title(title)
    plt.legend()
    plt.savefig(save_file)
    print('\nDone !')

if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    with open(CONFIGURATION) as f:
        data = json.load(f)

    if 'simulation' not in data or 'map' not in data or 'ga' not in data:
        print('Configuration does not contain all parameters')
        sys.exit(0)

    city = City.generate(rows=data['map']['size'],
                         cols=data['map']['size'],
                         n_intersections=data['map']['intersections'],
                         max_cars=data['simulation']['max_cars'],
                         max_cars_spawn=data['simulation']['max_cars_spawn'],
                         seed=data['map']['seed'])

    # Run
    best_individual = np.load(GENE_FILE)
    green_individual = [True for _ in range(len(best_individual))]
    random_individual = [choice([True, False]) for _ in range(len(best_individual))]
    name = generate_filename(data['simulation'], data['map'], data['ga'])

    print('Running city with all lights green...')
    run_simulations(city,
                    green_individual,
                    data['simulation']['sim_steps'],
                    data['simulation']['light_duration_steps'],
                    label='All green',
                    title='Fitness Values of the Simulation With Green Traffic Lights',
                    save_file='../data/{:d}_fitness_green_lights_{:s}.png'.format(int(time()), name))

    print('Running city with random lights...')
    run_simulations(city,
                    random_individual,
                    data['simulation']['sim_steps'],
                    data['simulation']['light_duration_steps'],
                    label='Random',
                    title='Fitness Values of the Simulation With Random Traffic Lights',
                    save_file='../data/{:d}_fitness_random_lights_{:s}.png'.format(int(time()), name))

    print('Running city with genetic algorithm lights...')
    run_simulations(city,
                    best_individual,
                    data['simulation']['sim_steps'],
                    data['simulation']['light_duration_steps'],
                    label='Genetic',
                    title='Fitness Values of the Simulation Genetic Traffic Lights',
                    save_file='../data/{:d}_fitness_genetic_lights_{:s}.png'.format(int(time()), name))
