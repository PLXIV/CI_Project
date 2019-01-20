import numpy as np
from ga.population import Population
from multiprocessing import Pool
from city.city import City
from time import time
from datetime import timedelta
from math import ceil


def __generate_args(cities, population, light_duration, sim_per_individual, sim_steps):
    args = []
    for i, individual in enumerate(population.genes):
        cities[i].clean()
        args.append([cities[i], individual.gene, sim_per_individual, sim_steps, light_duration])

    return args


def __generate_cities(map, hyperparameters, simulation):
    max_pop_size = Population.max_pop_size(hyperparameters['pop_size'],
                                           hyperparameters['elitism_n'],
                                           hyperparameters['truncation_percentage'])

    print('Maximum population size:', max_pop_size)
    return [City.generate(map['size'], map['size'], map['intersections'], simulation['max_cars'], simulation['max_cars_spawn'], map['seed']) for _ in range(max_pop_size)]


def run_genetics(map, hyperparameters, simulation):
    init = time()

    cities = __generate_cities(map, hyperparameters, simulation)
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

    best_performance_steps = []
    while population.generation_id < hyperparameters['max_generations'] \
        and not population.convergence_criteria():

        # Print information
        print('Step: {:3d}'.format(population.generation_id), end=' ')
        init = time()

        # Generate arguments to run individuals
        args = __generate_args(cities,
                               population,
                               simulation['light_duration_steps'],
                               hyperparameters['sim_per_individual'],
                               simulation['sim_steps'])

        # Run all individuals
        if hyperparameters['multiprocessing']:
            pool = Pool(hyperparameters['processes'])
            scores = pool.starmap(__run_gene, args)
            pool.close()
            for i, score in enumerate(scores):
                population.genes[i].score = score
        else:
            for i, gene in enumerate(population.genes):
                gene.score = __run_gene(cities[i], gene,
                                        hyperparameters['sim_per_individual'],
                                        simulation['sim_steps'],
                                        simulation['light_duration_steps'])

        # Update genes
        best_performance, _, pop_size = population.update_genes()
        best_performance_steps.append(best_performance)

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
    name = generate_filename(simulation, map, hyperparameters)
    np.save('../data/{:d}_best_{:s}.npy'.format(int(time()), name), best_gene)
    np.savetxt('../data/{:d}_fitness_{:s}.txt'.format(int(time()), name), np.array(best_performance_steps), delimiter="\n", fmt="%s")
    return best_performance, best_gene, best_performance_steps

def __run_gene(city, gene, sim_per_individual, sim_steps, light_duration):
    average_fitness = []

    for single_simulation in range(sim_per_individual):
        city.run(gene, sim_steps, light_duration, sim_time=0)
        fitness = city.cars_despawned
        average_fitness.append(fitness)
        city.clean()

    return np.mean(average_fitness)

def generate_filename(sim, map, ga):
    return '{:d}_{:d}_{:d}_{:d}_{:d}_{:d}_{:d}_{:s}_{:d}_{:d}_{:d}_{:d}_{:f}_{:d}_{:f}_{:f}_{:d}'.format(
        sim['sim_steps'],
        sim['light_duration_steps'],
        sim['max_cars'],
        sim['max_cars_spawn'],
        map['size'],
        map['intersections'],
        map['seed'],
        ga['crossover_type'],
        ga['max_generations'],
        ga['sim_per_individual'],
        ga['pop_size'],
        ga['elitism_n'],
        ga['truncation_percentage'],
        ga['crossover_points'],
        ga['crossover_probability'],
        ga['mutation_probability'],
        ga['spread_mutation'],
    ).replace(".", "+")