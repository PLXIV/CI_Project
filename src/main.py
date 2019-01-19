from city import City
from view.drawer import Drawer
from GA.Population import Population
import threading
import numpy as np
from time import sleep
from random import choice

def run_genetics(city):
    number_of_lights = len(city.grid.roads_with_lights)
    steps = 200
    a = Population(generation_id=0, pop_size=10, dna_size=steps*number_of_lights, elitism_n=2,
                   truncation_percentage=0.33, cross_over_points=3,
                   crossover_probability=0.9, mutation_probability=0.01, multiprocessing = False)
   
    fitness_ = []
    for gene in a.genes:
        lights_gene = gene.gene
        lights_gene = np.reshape(lights_gene, [number_of_lights, steps]).T
        
        for i in range(steps):
            # print(i)
            lights = lights_gene[i,:]
            city.step(lights)
            sleep(0.05)
        fitness = city.cars_despawned
        fitness_.append(fitness)
        city.clean()
        print('clean')
#        print('fitness:',finess)
    print(fitness_)


if __name__ == "__main__":

    
    # City
    city = City(rows=70, cols=70, n_intersections=30)
    city.grid.generate(seed=27367)

    # Graphics
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)

    # Run
    t = threading.Thread(target=run_genetics, args=[city])
    t.start()
    drawer.run()
    t.join()



