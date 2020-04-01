import os
from Chromosome import Chromosome
from GA import GA


# read the network details
def readNet(fileName):
    network = {}
    matrix = []

    input = open(fileName, "r");

    network["numberOfNodes"] = int(input.readline())

    for i in range(network["numberOfNodes"]):
        line = input.readline().split(",")
        matrix.append([int(x) for x in line])

    network["matrix"] = matrix
    network["startNode"] = int(input.readline()) - 1
    network["endNode"] = int(input.readline()) - 1

    return network

def fcEval(chromosome):
    repres = chromosome.repres
    matrix = chromosome.problParam["matrix"]
    fitnes = 0.0

    for i in range(len(repres) - 1):
        fitnes = fitnes + matrix[repres[i]][repres[i+1]]

    return fitnes

def main():
    network = readNet("input1.txt")

    gaParameters = {"populationSize": 10, "numberOfGenerations": 1000}

    problemParameters = {'function': fcEval,
                         'numberOfNodes': network["numberOfNodes"],
                         'matrix': network["matrix"],
                         'startNode': network["startNode"],
                         'endNode': network["endNode"]}

    globalBestChromosome = Chromosome(problemParameters)

    ga = GA(gaParameters, problemParameters)
    print("ga done")
    ga.initialisation()
    print("initialisation done")
    ga.evaluation()
    print("evaluation done")

    generation = 0
    while (generation < gaParameters["numberOfGenerations"]):
        generation += 1
        #ga.oneGeneration()
        ga.oneGenerationElitism()
        #ga.oneGenerationSteadyState()

        bestChromosom = ga.bestChromosome()

        if bestChromosom.fitness < globalBestChromosome.fitness:
            globalBestChromosome = bestChromosom

        print("------ gen: " + str(generation) + "--------")
        print('Local  Best fit = ' + str(bestChromosom.fitness))
        print('Local  worst fit: ', ga.worstChromosome()[0].fitness)
        print('Global Best fit: ', globalBestChromosome.fitness)
        print()

    path = globalBestChromosome.repres
    path = [x + 1 for x in path]
    print(path)



main()
