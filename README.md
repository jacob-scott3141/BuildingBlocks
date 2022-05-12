# BuildingBlocks

Recreation of "A Simple Two-Module Problem to Exemplify Building-Block Assembly Under Crossover" https://www.richardawatson.com/_files/ugd/395d71_7c48238c3ab84bbb90fd49ee8dc105ba.pdf

# BuildingBlocks

An implementation and extension of R.Watson's A Simple Two-Module Problem to Exemplify Building-Block Assembly Under Crossover

There are 2 main files: utils.py, and main.py.

# main.py

### get_data

performs a simulation on the two-module problem, given the size n of genes, number of iterations, crossover type, and selection method.
saves this data to a csv file.

### format_data

reads a csv file of the saved data into variables which can then be plotted with matplotlib.

# utils.py

Utils contains all the necessary components for the re-implementation.

## class Genotype methods

Genotype modelling R. Watson's 2 module problem

### init_from_genotype

initialises genotype from an array rather than random values

    :param g: numpy array of the genotypes bitstring to initialise with
    :return: correctly initialised Genotype object
    
## utils methods

### fitness

calculates the fitness according to R. Watson's simple 2 module problem, casting to python 64-bit ints and floats from numpy default dtypes

    :param g: Genotype to measure fitness
    :return: the fitness of g

### do_sim

performs a simulation on the selected group of islands.

    :param k: for k-tournament selection
    :param selection: method of parent selection
    :param pop: islands containing islanders
    :param crossover_type: type of crossover to perform
    :param show_landscape: shows 2d representation of where the best performing genotype lies on the fitness landscape
    :param show_best_genotype: shows the bit string of the best genotype
    :return: returns the best performing genotype after the simulation and the number of generations it took

### find_max

find the highest point in the fitness landscape

### crossover

one point crossover between 2 genotypes

    :param crossover_type: type of crossover to perform
    :param g1: 1st genotype
    :param g2: 2nd genotype
    :return: child Genotype object
    
### mutate

mutates a genotype g according to its rate g.m

    :param g: genotype to mutate
    :return: mutated Genotype object
    
### swap_islanders

swaps a randomly chosen islander from each island when called. will swap islanders such that the number of islanders per island is always constant

    :param islands: list of the islands containing the islanders
    :return: the islands with the islanders swapped
    
### fitness_proportionate_select_elitist

fitness proportionate selection, or "roulette wheel" selection. selects a population of individuals from theoriginal population in proportion to their fitness. elitism: retains fittest individual from each generation

    :param crossover_type: type of crossover to perform
    :param pop: list of genotypes to select from
    :return: list of selected genotypes
