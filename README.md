# BuildingBlocks

An implementation and extension of R.Watson's A Simple Two-Module Problem to Exemplify Building-Block Assembly Under Crossover

There are 2 main files: utils.py, and main.py.

##utils.py

Utils contains all the necessary components for the re-implementation.

###do_sim

performs a simulation on the selected group of islands
    :param k: for k-tournament selection
    :param selection: method of parent selection
    :param pop: islands containing islanders
    :param crossover_type: type of crossover to perform
    :param show_landscape: shows 2d representation of where the best performing genotype lies on the fitness landscape
    :param show_best_genotype: shows the bit string of the best genotype
    :return: returns the best performing genotype after the simulation and the number of generations it took
