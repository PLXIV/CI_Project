from view.drawer import Drawer
from city.city import City
import numpy as np
import threading
import json
import sys


CONFIGURATION = 'configuration.json'
GENE_FILE = '../data/1547994434_best_of_10_generations.npy'


def run_city(city, gene, sim_steps, light_duration, options):
    city.run(gene, sim_steps, light_duration, sim_time=0.3, options=options)


if __name__ == '__main__':

    with open(CONFIGURATION) as f:
        data = json.load(f)

    if 'simulation' not in data or 'map' not in data or 'ga' not in data:
        print('Configuration does not contain all parameters')
        sys.exit(0)

    # City
    print('Check that all parameters are ok !')
    city = City.generate(rows=data['map']['size'],
                         cols=data['map']['size'],
                         n_intersections=data['map']['intersections'],
                         max_cars=data['simulation']['max_cars'],
                         max_cars_spawn=data['simulation']['max_cars_spawn'],
                         seed=data['map']['seed'])
    gene = np.load(GENE_FILE)

    # Drawer
    options = [False] # QUIT
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, options=options)

    # RUN
    sim = threading.Thread(target=run_city,
                           args=[city,
                                 gene,
                                 data['simulation']['sim_steps'],
                                 data['simulation']['light_duration_steps'],
                                 options])
    sim.start()
    drawer.run()
    sim.join()