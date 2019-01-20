import numpy as np
from ga.population import Population
from multiprocessing import Pool
from city.city import City
from time import time
from datetime import timedelta
from math import ceil


def generate_args(cities, population, light_duration, sim_per_individual, sim_steps):
    args = []
    for i, individual in enumerate(population.genes):
        cities[i].clean()
        args.append([cities[i], individual.gene, sim_per_individual, sim_steps, light_duration])

    return args


def generate_cities(map, hyperparameters, simulation):
    max_pop_size = Population.max_pop_size(hyperparameters['pop_size'],
                                           hyperparameters['elitism_n'],
                                           hyperparameters['truncation_percentage'])

    print('Maximum population size:', max_pop_size)
    return [City.generate(map['size'], map['size'], map['intersections'], simulation['max_cars'], simulation['max_cars_spawn'], map['seed']) for _ in range(max_pop_size)]


def run_genetics(map, hyperparameters, simulation):
    init = time()

    cities = generate_cities(map, hyperparameters, simulation)
    number_of_lights = len(cities[0].grid.roads_with_lights)
    lights_steps = ceil(simulation['sim_steps'] / simulation['light_duration_steps']) + 1  # Todo +1 should not be needed
    dna_size = lights_steps * number_of_lights

    population = Population(pop_size=hyperparameters['pop_size'],
                            dna_size=dna_size,
                            elitism_n=hyperparameters['elitism_n'],
                            truncation_percentage=hyperparameters['truncation_percentage'],
                            crossover_type=hyperparameters['crossover_type'],
                            crossover_points=hyperparameters['crossover_points'],
                            crossover_probability=hyperparameters['crossover_probability'],
                            mutation_probability=hyperparameters['mutation_probability'],
                            spread_mutation=hyperparameters['spread_mutation'],
                            objects_codified=number_of_lights,
                            multiprocessing=False)

    while population.generation_id < hyperparameters['max_generations'] \
        and not population.convergence_criteria():

        # Print information
        print('Step: {:3d}'.format(population.generation_id), end=' ')
        init = time()

        # Generate arguments to run individuals
        args = generate_args(cities,
                             population,
                             simulation['light_duration_steps'],
                             hyperparameters['sim_per_individual'],
                             simulation['sim_steps'])

        # Run all individuals
        if hyperparameters['multiprocessing']:
            pool = Pool(hyperparameters['processes'])
            scores = pool.starmap(run_gene, args)
            pool.close()
            for i, score in enumerate(scores):
                population.genes[i].score = score
        else:
            for i, gene in enumerate(population.genes):
                gene.score = run_gene(cities[i], gene,
                                      hyperparameters['sim_per_individual'],
                                      simulation['sim_steps'],
                                      simulation['light_duration_steps'])

        # Update genes
        best_performance, _, pop_size = population.update_genes()

        # Print information
        print('| New pop size: {:3d} | Fitness: [Best step: {:3.2f}, Best all: {:3.2f}] | Gene size {:d} | Took {:s}'
              .format(pop_size,
                      best_performance,
                      population.best_historical_performance,
                      dna_size,
                      str(timedelta(seconds=(time() - init)))))

    best_performance = population.best_historical_performance
    best_gene = population.best_historical_individual

    print('Done !, took', timedelta(seconds=(time() - init)), 'Saving best...')
    np.save('../data/{:d}_best_of_{:d}_generations.npy'.format(int(time()), hyperparameters['max_generations']), best_gene)
    return best_performance, best_gene


def run_gene(city, gene, sim_per_individual, sim_steps, light_duration):
    average_fitness = []

    for single_simulation in range(sim_per_individual):
        city.run(gene, sim_steps, light_duration, sim_time=0)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()

    return np.mean(average_fitness)