import seaborn as sns
import matplotlib.pyplot as plt
from random import choice
from city.city import City
import numpy as np
import sys
import json
sns.set()

CONFIGURATION = 'configuration.json'
GENE_FILE = '../data/1547994434_best_of_10_generations.npy'
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
    plt.savefig(save_file)
    print('Done !')

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

    print('Running city with all lights green...')
    run_simulations(city,
                    green_individual,
                    data['simulation']['sim_steps'],
                    data['simulation']['light_duration_steps'],
                    label='All green',
                    title='Fitness Values of the Simulation With Green Traffic Lights',
                    save_file='../data/fitness_green_lights.png')

    print('Running city with random lights...')
    run_simulations(city,
                    random_individual,
                    data['simulation']['sim_steps'],
                    data['simulation']['light_duration_steps'],
                    label='Random',
                    title='Fitness Values of the Simulation With Random Traffic Lights',
                    save_file='../data/fitness_random_lights.png')

    print('Running city with genetic algorithm lights...')
    run_simulations(city,
                    best_individual,
                    data['simulation']['sim_steps'],
                    data['simulation']['light_duration_steps'], 
                    label='Genetic',
                    title='Fitness Values of the Simulation Genetic Traffic Lights',
                    save_file='../data/fitness_genetic_lights.png')
