import utils as u
import matplotlib.pyplot as plt
import numpy as np


def get_data(n: int, iterations: int, crossover: str, file_to_write: str, selection: str, k=2):
    s = []
    g = []
    with open(file_to_write, 'a', buffering=1) as f:
        for i in range(n):
            for _ in range(iterations):
                islands = u.make_islands(50, 200)
                _, iters = u.do_sim(islands,
                                    crossover_type=crossover, show_best_genotype=True, selection=selection, k=k)
                if iters != -1:
                    f.write(f"{(i + 1) * 10}, {iters}\n")
                    g.append(iters)
                    s.append((i + 1) * 10)
            u.increment()
    u.reset()
    return s, g


def format_data(file: str):
    s = []
    g = []

    with open(file, 'r') as f:
        gens = []
        current_size = 10

        for line in f:
            size, gen = line.split(", ")

            if int(size) > current_size:
                g.append(gens)
                s.append(current_size)
                gens = []
                current_size = int(size)

            gens.append(int(gen.strip()))
        g.append(gens)
        s.append(current_size)
    return s, g


if __name__ == '__main__':
    #
    # get_data(6, 20, 'one point', "2block5.csv", "tournament", k=2)
    # get_data(6, 20, 'one point', "2block6.csv", "tournament", k=4)
    # get_data(6, 20, 'one point', "2block7.csv", "tournament", k=6)
    # get_data(6, 20, 'one point', "2block4.csv", "random")
    #
    # g1 = u.Genotype().init_from_genotype(np.zeros(20, dtype=int))
    # g2 = u.Genotype().init_from_genotype(np.ones(20, dtype=int))
    # u.crossover(g1, g2, 'uniform')

    sizes, generations = format_data('2block1.csv')

    data1 = {
        'x': [s*2 for s in sizes],
        'y': [sum(g)/len(g) for g in generations],
        'yerr': [[sum(g)/len(g) - min(g) for g in generations], [max(g) - sum(g)/len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations],
        'label': "2 block Roulette"
    }

    sizes, generations = format_data('2block2.csv')

    data2 = {
        'x': [s*2 for s in sizes],
        'y': [sum(g) / len(g) for g in generations],
        'yerr': [[sum(g)/len(g) - min(g) for g in generations], [max(g) - sum(g)/len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations],
        'label': "2 block Rank"
    }

    sizes, generations = format_data('3block1.csv')

    data3 = {
        'x': [s*3 for s in sizes],
        'y': [sum(g) / len(g) for g in generations],
        'yerr': [[sum(g) / len(g) - min(g) for g in generations], [max(g) - sum(g) / len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations],
        'label': "3 block Roulette"
    }

    sizes, generations = format_data('3block2.csv')

    data4 = {
        'x': [s*3 for s in sizes],
        'y': [sum(g) / len(g) for g in generations],
        'yerr': [[sum(g) / len(g) - min(g) for g in generations], [max(g) - sum(g) / len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations],
        'label': "3 block Rank"
    }

    sizes, generations = format_data('4block1.csv')

    data5 = {
        'x': [s*4 for s in sizes],
        'y': [sum(g) / len(g) for g in generations],
        'yerr': [[sum(g) / len(g) - min(g) for g in generations], [max(g) - sum(g) / len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations],
        'label': "4 block Roulette"
    }

    sizes, generations = format_data('4block2.csv')

    data6 = {
        'x': [s*4 for s in sizes],
        'y': [sum(g) / len(g) for g in generations],
        'yerr': [[sum(g) / len(g) - min(g) for g in generations], [max(g) - sum(g) / len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations],
        'label': "4 block Rank"
    }

    for data in [data1, data2, data3, data4, data5, data6]:
        print(data['yerr'])
        plt.errorbar(x=data['x'], y=data['y'], yerr=data['yerr'],
                     fmt='--o', alpha=0.9, capsize=3, capthick=1, label=data['label'])
        data = {
            'x': data['x'],
            'y1': data['ymin'],
            'y2': data['ymax']}
        # plt.fill_between(**data, alpha=.25)



    #plt.yscale("log")
    plt.xlabel("genotype length")
    plt.ylabel("generations to peak")
    plt.legend()
    plt.show()
