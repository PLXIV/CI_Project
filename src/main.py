from city import City
from view.drawer import Drawer
from GA.Population import Population
import threading
import numpy as np
from time import sleep
from random import choice
from multiprocessing import Pool

PROCESSES = 8
ENABLE_MULTIPROCESSING = True

def run_genetics(city):

    number_of_lights = len(city.grid.roads_with_lights)
    steps_generations = 100
    steps_simulation = 200
    n_simulations = 10
    population = Population(generation_id=0, pop_size=20, dna_size=steps_simulation*number_of_lights, elitism_n=100,
                   truncation_percentage=0.33, cross_over_points=50,
                   crossover_probability=0.9, mutation_probability=0.005, multiprocessing = False)
   
    for generation in range(steps_generations):
        cities = [city for i in population.genes]
        lights = [number_of_lights for i in population.genes]
        simulations = [n_simulations for i in population.genes]
        steps = [steps_simulation for i in population.genes]
        args = [cities, population.genes, lights, simulations, steps]
        if ENABLE_MULTIPROCESSING:
            pool = Pool(PROCESSES)
            scores = pool.starmap(run_gene, zip(args))
            pool.close()
            for i, s in enumerate(scores):
                population.genes[i].score = s
        else:
            for gene in population.genes:  
                gene.score = run_gene(gene)
        best_performance, best_gene = population.update_genes()


#city, gene, number_of_lights, n_simulations, steps_simulation
def run_gene(city, gene, number_of_lights, n_simulations, steps_simulation):
#    average_fitness = []
#    for single_simulation in range(args[3]):
#        lights_gene = args[1]
#        lights_gene = np.reshape(lights_gene, [args[2], args[4]]).T
#        for i in range(args[4]):
#            lights = lights_gene[i,:]
#            args[0].step(lights)
#        fitness = args[0].cars_despawned
#        average_fitness.append(fitness)
#        args[0].clean()
#    return np.mean(average_fitness)
    return np.random.rand()

if __name__ == "__main__":
    
    # City
    city = City(rows=20, cols=20, n_intersections=5)
    city.grid.generate(seed=13011)

    # Graphics
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)

    # Run
    t = threading.Thread(target=run_genetics, args=[city])
    t.start()
    drawer.run()
    t.join()



