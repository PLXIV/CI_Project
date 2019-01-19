from city import City
from view.drawer import Drawer
from GA.Population import Population
import threading
import numpy as np
from time import sleep
from random import choice

def run_genetics(city):
    number_of_lights = len(city.grid.roads_with_lights)
    steps_generations = 100
    steps_simulation = 100
    population = Population(generation_id=0, pop_size=200, dna_size=steps_simulation*number_of_lights, elitism_n=40,
                   truncation_percentage=0.33, cross_over_points=1000,
                   crossover_probability=0.9, mutation_probability=0.01, multiprocessing = False)
   
    for generation in range(steps_generations):
        print(len(population.genes))
        for gene in population.genes:  
            tmp_fit = []
            for single_simulation in range(10):
                lights_gene = gene.gene
                lights_gene = np.reshape(lights_gene, [number_of_lights, steps_simulation]).T
                for i in range(steps_simulation):
                    lights = lights_gene[i,:]
                    city.step(lights)
                fitness = city.cars_despawned
                tmp_fit.append(fitness)
                city.clean()
            gene.score = np.mean(tmp_fit)

        scores = population.get_scores()
        best_performance = max(scores)
        best_gene = population.genes[scores.argmax()]
        population.truncation()
        population.crossover()
        population.elitism()
        population.mutation()
        population.new_generation()
        print(best_performance)
        print(best_gene)
        print('-'*10)


if __name__ == "__main__":

    
    # City
    city = City(rows=20, cols=20, n_intersections=4)
    city.grid.generate(seed=27367)



    # Graphics
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)

    # Run
    t = threading.Thread(target=run_genetics, args=[city])
    t.start()
    drawer.run()
    t.join()



