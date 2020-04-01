
from Chromosome import Chromosome

from random import randint


class GA:
    def __init__(self, param=None, problParam=None):
        self.__param = param
        self.__problParam = problParam
        self.__population = []

    @property
    def population(self):
        return self.__population

    def initialisation(self):
        for _ in range(0, self.__param["populationSize"]):
            c = Chromosome(self.__problParam)
            self.__population.append(c)

    def evaluation(self):
        for c in self.__population:
            c.fitness = self.__problParam['function'](c)

    def bestChromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if (c.fitness < best.fitness):
                best = c
        return best

    def worstChromosome(self):
        worst = self.__population[0]
        pos = -1
        index = -1
        for c in self.__population:
            index += 1
            if (c.fitness > worst.fitness):
                worst = c
                pos = index
        return worst, pos

    def selection(self):
        pos1 = randint(0, self.__param["populationSize"] - 1)
        pos2 = randint(0, self.__param["populationSize"] - 1)
        if (self.__population[pos1].fitness < self.__population[pos2].fitness):
            return pos1
        else:
            return pos2

    def oneGeneration(self):
        newPop = []
        for _ in range(self.__param["populationSize"]):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def oneGenerationElitism(self):
        newPop = [self.bestChromosome()]
        for _ in range(self.__param["populationSize"] - 1):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            off.fitness = self.__problParam["function"](off)
            worst, pos = self.worstChromosome()
            if (off.fitness < worst.fitness):
                newPop.append(off)
                self.__population[pos] = off
            else:
                newPop.append(worst)

        self.__population = newPop
        self.evaluation()


    def oneGenerationSteadyState(self):
        for _ in range(self.__param["populationSize"]):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            off.fitness = self.__problParam['function'](off)
            worst = self.worstChromosome()
            if (off.fitness < worst.fitness):
                worst = off
