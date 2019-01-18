from Gene import *
import numpy as np
import random
from scipy.spatial import distance
from time import time
from datetime import timedelta
from itertools import starmap
from multiprocessing import Pool

PROCESSES = 4


class Population(object):

    def __init__(self,
                 generation_id=0, pop_size=100, dna_size=10, elitism_n=2,
                 truncation_percentage=0.33, cross_over_points=3,
                 crossover_probability=0.9, mutation_probability=0.01):

        self.generation_id = generation_id
        self.pop_size = pop_size
        self.dna_size = dna_size

        self.genes = self._initPopulation()
        self.elitism_n = elitism_n
        self.crossover_points = cross_over_points
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.offspring = []
        self.truncation_size = int(pop_size * truncation_percentage)
        if self.truncation_size % 2 != 0:
            self.truncation_size -= 1

    def do_cycle(self):
        self.run_population()
        scores = self.get_scores()
        best_performance = max(scores)
        best_gene = self.genes[scores.argmax()]
        self.truncation()
        self.crossover()
        self.elitism()
        self.mutation()
        self.new_generation()
        return [best_performance, best_gene]

    def get_scores(self):
        return np.array([g.score for g in self.genes])

    def _initPopulation(self):
        population = []
        for g in range(self.pop_size):
            population.append(Gene(dna_size=self.dna_size))
        return population

    def mutation(self):
        for g in range(len(self.offspring)):
            self.offspring[g].mutation(self.mutation_probability)

    @staticmethod
    def compute_score(gen):
        target = np.zeros(10)
        a = 0
        for i in range(1, 2 * 10 ** 3):
            a = np.math.factorial(i)
        return 1 - distance.hamming(target, gen.gene)

    @staticmethod
    def assignate_score_to_gene(score, gen):
        gen.score = score
        print(gen.score, score)

    def run_population(self):
        pool = Pool(PROCESSES)
        scores = pool.map(self.compute_score,self.genes)
        pool.close()
        for i, s in enumerate(scores):
            self.genes[i].score = s
        # for g in range(len(self.genes)):
        #    self.genes[g].score = self.compute_score(self.genes[g].gene)

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

    def crossover(self):
        np.random.shuffle(self.genes)
        for i in range(0, len(self.genes), 2):
            genInfo1 = i
            genInfo2 = i + 1
            cuts = random.sample(range(1, self.dna_size - 1), self.crossover_points)
            cuts.sort()
            cut_index = 0
            cuts = [2, 4, 6]
            newGen1 = []
            newGen2 = []
            for j in range(self.dna_size):
                if cuts[cut_index] == j:
                    if genInfo1 == i:
                        genInfo1 = i + 1
                        genInfo2 = i
                    else:
                        genInfo1 = i
                        genInfo2 = i + 1

                    if cut_index < self.crossover_points - 1:
                        cut_index += 1

                newGen1.append(self.genes[genInfo1].gene[j])
                newGen2.append(self.genes[genInfo2].gene[j])

            self.offspring.append(Gene(dna_size=self.dna_size, gene=newGen1))
            self.offspring.append(Gene(dna_size=self.dna_size, gene=newGen2))

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
    a = Population(generation_id=0, pop_size=10, dna_size=10, elitism_n=2,
                   truncation_percentage=0.33, cross_over_points=3,
                   crossover_probability=0.9, mutation_probability=0.01)

    results = []
    for i in range(100):
        results.append(a.do_cycle())
    print('total time:', timedelta(seconds=(time() - init)))
