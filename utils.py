import numpy as np

n = 10
r = np.random.uniform(0.5, 1, size=(n + 1, n + 1))
r = np.array(r, dtype='float64')


def increment():
    global n
    global r
    n = n + 10
    r = np.random.uniform(0.5, 1, size=(n + 1, n + 1))
    r = np.array(r, dtype='float64')


class Genotype:
    """
    Genotype modelling R. Watson's 2 module problem
    """

    def __init__(self):
        """
        initialises the i and j building blocks, the mutation rate m, and the fitness f
        """
        self.i = np.random.randint(2, size=n)
        self.j = np.random.randint(2, size=n)
        self.m = 1 / (2 * n)
        self.f = fitness(self)

    def __str__(self):
        return str(self.get_genotype())

    def init_from_genotype(self, g: np.ndarray):
        """
        :param g: numpy array of the genotypes bitstring to initialise with
        :return: correctly initialised Genotype object
        """
        size = g.shape[0]
        if size % 2 != 0:
            print("Genotype must be of even length")
            return
        size = size // 2
        self.i = g[0:size]
        self.j = g[size:size * 2]
        self.f = fitness(self)
        return self

    def get_genotype(self):
        return np.concatenate([self.i, self.j])


def fitness(g: Genotype):
    """
    calculates the fitness according to R. Watson's simple 2 module problem
    casting to python 64-bit ints and floats from numpy default dtypes
    :param g: Genotype to measure fitness
    :return: the fitness of g
    """
    i = int(sum(g.i))
    j = int(sum(g.j))
    r_ = float(r[j][i])
    f = r_ * (2 ** i + 2 ** j)
    return float(f)


def swap_islanders(islands: list[list[Genotype]]):
    """
    swaps a randomly chosen islander from each island when called
    will swap islanders such that the number of islanders per island is always constant

    :param islands: list of the islands containing the islanders
    :return: the islands with the islanders swapped
    """
    copy = islands.copy()
    swaps = [None for _ in islands]
    islands_left = [a for a in range(len(islands))]

    for i in range(len(islands)):
        choices = islands_left.copy()
        if i in choices:
            choices.remove(i)

        if len(choices) > 2:
            choice = np.random.choice(choices)
            swaps[i] = choice
            islands_left.remove(choice)
        elif len(choices) == 2:
            a, b = choices
            if swaps[a] is None and swaps[b] is None:
                choice = np.random.choice(choices)
                swaps[i] = choice
                islands_left.remove(choice)
            elif swaps[a] is not None:
                choice = b
                swaps[i] = choice
                islands_left.remove(choice)
            elif swaps[b] is not None:
                choice = a
                swaps[i] = choice
                islands_left.remove(choice)
            else:
                print("ERROR in islander swapping")
        elif len(choices) == 1:
            swaps[i] = choices[0]

    islanders = [np.random.choice(island) for island in copy]

    for i in range(len(islands)):
        copy[swaps[i]].append(islanders[i])
        copy[i].remove(islanders[i])
    return copy


def fitness_proportionate_select_elitist(pop: list[Genotype], crossover_type: str):
    """
    fitness proportionate selection, or "roulette wheel" selection. selects a population of individuals from the
    original population in proportion to their fitness
    elitism: retains fittest individual from each generation
    :param crossover_type: type of crossover to perform
    :param pop: list of genotypes to select from
    :return: list of selected genotypes
    """
    elite = max(pop, key=lambda gene: gene.f)

    total_fitness = sum([p.f for p in pop])

    probs = [p.f / total_fitness for p in pop]

    pop1 = np.random.choice(pop, size=len(pop), p=probs).tolist()
    temp = []

    if crossover_type is not None:
        pop2 = np.random.choice(pop, size=len(pop), p=probs).tolist()
        for i in range(len(pop)):
            temp.append(crossover(pop1[i], pop2[i], crossover_type))
    else:
        temp = pop1

    pop = [mutate(p) for p in temp]

    worst = np.random.choice(pop)

    pop.remove(worst)
    pop.append(elite)

    return pop


def mutate(g: Genotype):
    """
    mutates a genotype g according to its rate g.m
    :param g: genotype to mutate
    :return: mutated Genotype object
    """
    gen = g.get_genotype()

    for i in range(gen.shape[0]):
        if np.random.uniform() < g.m:
            gen[i] = 1 - gen[i]
    return Genotype().init_from_genotype(gen)


def crossover(g1: Genotype, g2: Genotype, crossover_type: str):
    """
    one point crossover between 2 genotypes
    :param crossover_type: type of crossover to perform
    :param g1: 1st genotype
    :param g2: 2nd genotype
    :return: child Genotype object
    """
    g1 = g1.get_genotype()
    g2 = g2.get_genotype()

    if g1.shape != g2.shape:
        print("Genotype shapes do not match")
        return

    size = g1.shape[0]

    if crossover_type == 'one point':
        crossover_point = np.random.randint(size + 1)
        ret = Genotype().init_from_genotype(np.concatenate([g1[0:crossover_point], g2[crossover_point:size]]))
    elif crossover_type == 'uniform':
        crossover_points = np.random.rand(size)
        ret = np.empty(size, dtype=int)
        for i in range(size):
            if crossover_points[i] < 0.5:
                ret[i] = g1[i]
            else:
                ret[i] = g2[i]
        ret = Genotype().init_from_genotype(ret)
    return ret


def make_islands(num_islands, num_islanders):
    return [[Genotype() for _ in range(num_islanders)] for _ in range(num_islands)]


def do_sim(pop: list[list[Genotype]], crossover_type=None,
           show_landscape=False, show_best_genotype=False):
    """
    performs a simulation on the selected group of islands
    :param pop: islands containing islanders
    :param crossover_type: type of crossover to perform
    :param show_landscape: shows 2d representation of where the best performing genotype lies on the fitness landscape
    :param show_best_genotype: shows the bit string of the best genotype
    :return: returns the best performing genotype after the simulation and the number of generations it took
    """
    num_iters = 0

    while True:
        a, b, f = find_max()
        test = pop.copy()
        test = np.array(test).flatten()

        print(f"epoch {num_iters} at size {n}")

        best = max(test, key=lambda gene: gene.f)

        if show_best_genotype:
            print(best, best.f)

            print(a, b, f)

        if show_landscape:
            i = sum(best.i)
            j = sum(best.j)

            for _ in range(n - i):
                print("-" * n)
            print("-" * (j - 1) + "#" + "-" * (n - j))
            for _ in range(i):
                print("-" * n)

        if np.all(best.get_genotype()) or best.f >= f:
            print(best)
            print(num_iters)
            return best, num_iters
        elif num_iters > 5000:
            tmp = r.tolist()
            for line in tmp:
                print(line)
            return best, -1

        pop = [fitness_proportionate_select_elitist(p, crossover_type) for p in pop]
        pop = swap_islanders(pop)
        num_iters += 1
        print()


def find_max():
    """
    find the highest point in the fitness landscape
    :return:
    """
    global r
    global n
    max_f = 0, 0, 0

    for i in range(n+1):
        for j in range(n+1):
            r_ = float(r[j][i])
            f = r_ * (2 ** i + 2 ** j)
            if max_f[2] < f:
                max_f = i, j, f

    return max_f


def rated_swap_islanders(islands: list[list[Genotype]], rate):
    copy = islands.copy()

    for i in range(len(islands)):
        island = islands[i]

        for j in range(len(island)):
            if np.random.uniform() < rate:
                choices = [a for a in range(len(islands))]
                choices.remove(i)
                island_index = np.random.choice(choices)
                islander_index = np.random.choice(len(islands[island_index]))

                copy[i][j] = islands[island_index][islander_index]
                copy[island_index][islander_index] = islands[i][j]

            else:
                copy[i][j] = islands[i][j]

    return copy
