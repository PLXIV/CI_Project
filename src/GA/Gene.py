import numpy as np

class Gene(object):

    def __init__(self,id = 0, dna_size=10, spread_mutation = 0, gene = None):
        self.id = id
        self.dna_size = dna_size
        self.score = 0.0
        self.spread_mutation = spread_mutation

        if not gene:
            self.gene = self._initGene()
        else:
            self.gene = np.array(gene)
            
    def _initGene(self):
        return np.random.randint(2, size=self.dna_size)

    def mutation(self, mutation_probability):    
        for i in range(self.dna_size):
            mute = np.random.random()
            if(mute<=mutation_probability):
                self.gene[i] = int(not(self.gene[i]))
                if self.spread_mutation > 0:
                    for j in range(1,self.spread_mutation+1, 1):     
                        if (i-j>=0):
                            self.gene[i-j] = int(not(self.gene[i-j]))
                        if (i+j< self.dna_size):
                            self.gene[i-j] = int(not(self.gene[i+j]))                           
                                
    def __repr__(self):
        return 'Gene: ' + str(self.gene)

