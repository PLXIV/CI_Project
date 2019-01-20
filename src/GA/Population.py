# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 00:08:21 2019

@author: PauL
"""

from GA.Gene import *
import numpy as np
import random
from scipy.spatial import distance
from time import time
from datetime import timedelta
from itertools import starmap
from multiprocessing import Pool
import queue

PROCESSES = 6


class Population(object):

    def __init__(self,
                 generation_id=0, pop_size=100, dna_size=10, elitism_n=2,
                 truncation_percentage=0.33, cross_over_points=3,
                 crossover_probability=0.9, mutation_probability=0.01, 
                 spread_mutation = 0, objects_codified = 2,
                 multiprocessing = True):

        self.generation_id = generation_id
        self.pop_size = pop_size
        self.dna_size = dna_size
        
        self.multiprocessing = multiprocessing
        self.spread_mutation = spread_mutation
        self.genes = self._initPopulation()
        self.elitism_n = elitism_n
        self.crossover_points = cross_over_points
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.offspring = []
        self.truncation_size = int(pop_size * truncation_percentage)
        self.objects_codified = objects_codified
        if self.truncation_size % 2 != 0:
            self.truncation_size -= 1
        self.number_of_saved_performances = 100
        self.best_performances = queue.Queue(self.number_of_saved_performances)
        self.best_individuals = queue.Queue(self.number_of_saved_performances)
        self.best_historical_individual = None
        self.best_historical_performance = 0

    def max_pop_size(self):
        no_truncated = self.pop_size - self.truncation_size
        return no_truncated + min(self.elitism_n, no_truncated)

    def update_genes(self):
        scores = self.get_scores()
        best_performance = max(scores)
        best_gene = self.genes[scores.argmax()]
        self.truncation()
        #self.crossover_objects()
        self.crossover_regular()
        self.mutation()
        self.elitism()
        self.new_generation()

        self.actualize_performance(best_performance, best_gene)
        if best_performance > self.best_historical_performance:
            self.best_historical_performance = best_performance
            self.best_historical_individual = best_gene.gene

        return best_performance, best_gene, len(self.genes)

    def do_cycle(self):
        self.run_population()
        scores = self.get_scores()
        best_performance = max(scores)
        best_gene = self.genes[scores.argmax()]        
        self.truncation()
        #self.crossover_objects()
        self.crossover_regular
        self.mutation()
        self.elitism()
        self.new_generation()

        return [best_performance, best_gene]

    def convergence_criteria(self):
        best_per_array = np.array(self.best_performances.queue)
        best_indiv_array = np.array(self.best_individuals.queue)

        if self.best_performances.full() and np.all(best_per_array[0] == best_per_array):
            print('Converged due to repeating the best performance')
            return True
        if self.best_individuals.full() and np.all(best_indiv_array[0,:] == best_indiv_array):
            print('Converged due to repeating the best individual')
            return True

        if self.best_performances.full() and np.all(self.best_historical_performance > best_per_array+1):
            print('Converged due to no improvement')
            return True
        return False

    def actualize_performance(self, performance, individual):
        if self.best_performances.full():
            self.best_performances.get()
        if self.best_individuals.full():
            self.best_individuals.get()
        self.best_performances.put(performance)
        self.best_individuals.put(individual.gene)


    def get_scores(self):
        return np.array([g.score for g in self.genes])

    def _initPopulation(self):
        population = []
        for g in range(self.pop_size):
            population.append(Gene(dna_size=self.dna_size, spread_mutation=self.spread_mutation))
        return population

    def mutation(self):
        for g in range(len(self.offspring)):
            self.offspring[g].mutation(self.mutation_probability)

    @staticmethod
    def compute_score(gen):
        target = np.zeros(400)
#        a = 0
#        for i in range(1, 2 * 10 ** 3):
#            a = np.math.factorial(i)
        return 1 - distance.hamming(target, gen.gene)

    @staticmethod
    def assignate_score_to_gene(score, gen):
        gen.score = score
        print(gen.score, score)

    def run_population(self):
        if self.multiprocessing:            
            pool = Pool(PROCESSES)
            scores = pool.map(self.compute_score,self.genes)
            pool.close()
            for i, s in enumerate(scores):
                self.genes[i].score = s
        else:
             for g in range(len(self.genes)):
                self.genes[g].score = self.compute_score(self.genes[g])

    def elitism(self):
        scores = self.get_scores()
        performance = scores.argsort()[::-1]
        elite = performance[0:self.elitism_n]
        for i in elite:
            self.offspring.append(self.genes[i])

    def truncation(self):
        scores = self.get_scores()
        performance = scores.argsort()[::-1]
        get_best = performance[:self.pop_size - self.truncation_size]
        self.genes = np.array(self.genes)[get_best]


    def check_genes(self, cuts, cut_index, genInfo1, genInfo2, i, j):
        if cuts[cut_index] == j:
            if genInfo1 == i:
                genInfo1 = i + 1
                genInfo2 = i
            else:
                genInfo1 = i
                genInfo2 = i + 1
            if cut_index < self.crossover_points - 1:
                cut_index += 1

        return genInfo1, genInfo2, cut_index
            

    def crossover_objects(self):
        assert(self.dna_size % self.objects_codified == 0)
        len_object =  self.dna_size/self.objects_codified
        np.random.shuffle(self.genes)
        for i in range(0, len(self.genes), 2):
            genInfo1 = i
            genInfo2 = i + 1
            newGen1 = []
            newGen2 = [] 
            for j in range(self.objects_codified):
                start_obj = int(len_object*j)
                end_obj = int(len_object*(j+1))
                cuts = random.sample(range(start_obj+1, end_obj-1), self.crossover_points)
                cuts.sort()
                cut_index = 0
                for z in range(start_obj, end_obj, 1):
                    genInfo1, genInfo2, cut_index = self.check_genes(cuts, cut_index, genInfo1, genInfo2, i, j)
                    newGen1.append(self.genes[genInfo1].gene[z])
                    newGen2.append(self.genes[genInfo2].gene[z])
                    
            self.offspring.append(Gene(dna_size=self.dna_size, spread_mutation=self.spread_mutation, gene=newGen1))
            self.offspring.append(Gene(dna_size=self.dna_size, spread_mutation=self.spread_mutation, gene=newGen2))
            

    def crossover_regular(self):
        np.random.shuffle(self.genes)
        for i in range(0, len(self.genes), 2):
            genInfo1 = i
            genInfo2 = i + 1
            newGen1 = []
            newGen2 = []
            cuts = random.sample(range(1, self.dna_size - 1), self.crossover_points)
            cuts.sort()
            cut_index = 0
            for j in range(self.dna_size):
                genInfo1, genInfo2, cut_index = self.check_genes(cuts, cut_index, genInfo1, genInfo2, i, j)
                newGen1.append(self.genes[genInfo1].gene[j])
                newGen2.append(self.genes[genInfo2].gene[j])
            self.offspring.append(Gene(dna_size=self.dna_size, spread_mutation=self.spread_mutation, gene=newGen1))
            self.offspring.append(Gene(dna_size=self.dna_size, spread_mutation=self.spread_mutation, gene=newGen2))

    def new_generation(self):
        self.genes = np.copy(self.offspring)
        self.offspring = []
        self.generation_id += 1

    def __repr__(self):
        ret = 'Population (Generation ' + str(self.generation_id) + '): \n'
        ret += '(Population size: ' + str(self.pop_size) + ', DNA size: ' + str(self.dna_size) + ',\n'
        ret += 'Mutation probability: ' + str(self.mutation_probability) + ')\n'
        for g in self.genes:
            ret += str(g) + '\n'
        return ret


if __name__ == "__main__":
    init = time()
    a = Population(generation_id=0, pop_size=10, dna_size=400, elitism_n=2,
                   truncation_percentage=0.33, cross_over_points=2,
                   crossover_probability=0.9, mutation_probability=0.1,
                   spread_mutation= 0, objects_codified = 4,
                   multiprocessing = False)

    results = []
    for i in range(100):
        results.append(a.do_cycle())
    print('total time:', timedelta(seconds=(time() - init)))
